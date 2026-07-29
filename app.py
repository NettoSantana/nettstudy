# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\app.py
# Data e hora do último recode: 29/07/2026 16:15 -03:00
# Motivo da alteração: criar a base funcional inicial do NettStudy com autenticação, sessões e dashboards.

import os
from functools import wraps
from typing import Any, Callable

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from config import Config
from database import buscar_usuario_por_login, inicializar_banco


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    inicializar_banco(app.config["DATABASE_PATH"])
    registrar_contexto(app)
    registrar_rotas(app)
    registrar_erros(app)
    return app


def login_obrigatorio(perfil: str | None = None) -> Callable:
    def decorador(funcao: Callable) -> Callable:
        @wraps(funcao)
        def protegida(*args: Any, **kwargs: Any):
            if not session.get("usuario_id"):
                flash("Faça login para continuar.", "aviso")
                return redirect(url_for("login"))
            if perfil and session.get("perfil") != perfil:
                flash("Este acesso não pertence ao seu perfil.", "erro")
                return redirect(url_for("portal"))
            return funcao(*args, **kwargs)
        return protegida
    return decorador


def registrar_contexto(app: Flask) -> None:
    @app.context_processor
    def contexto_global() -> dict[str, Any]:
        return {
            "nome_produto": "NettStudy",
            "usuario_logado": session.get("nome"),
            "perfil_logado": session.get("perfil"),
        }


def registrar_rotas(app: Flask) -> None:
    @app.get("/")
    def inicio():
        return render_template("portal.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identificador = request.form.get("identificador", "").strip().lower()
            senha = request.form.get("senha", "")
            usuario = buscar_usuario_por_login(app.config["DATABASE_PATH"], identificador)
            if not usuario or not check_password_hash(usuario["senha_hash"], senha):
                flash("Login ou senha inválidos.", "erro")
                return render_template("login.html", identificador=identificador), 401
            session.clear()
            session.update(usuario_id=usuario["id"], nome=usuario["nome"], perfil=usuario["perfil"])
            destino = "dashboard_responsavel" if usuario["perfil"] == "responsavel" else "dashboard_aluno"
            return redirect(url_for(destino))
        return render_template("login.html")

    @app.get("/sair")
    def sair():
        session.clear()
        flash("Você saiu do NettStudy.", "sucesso")
        return redirect(url_for("inicio"))

    @app.get("/portal")
    def portal():
        return render_template("portal.html")

    @app.get("/responsavel")
    @login_obrigatorio("responsavel")
    def dashboard_responsavel():
        aluno = {
            "nome": "João",
            "ano_escolar": "5º ano",
            "sequencia": 4,
            "pontos": 280,
            "progresso_dia": 67,
            "atividades": [
                {"nome": "Português", "status": "Concluída", "progresso": 100},
                {"nome": "Matemática", "status": "Em andamento", "progresso": 60},
                {"nome": "Leitura", "status": "Pendente", "progresso": 0},
            ],
        }
        return render_template("dashboard_responsavel.html", aluno=aluno)

    @app.get("/aluno")
    @login_obrigatorio("aluno")
    def dashboard_aluno():
        missao = [
            {"nome": "Português", "descricao": "10 questões", "concluida": True},
            {"nome": "Matemática", "descricao": "10 questões", "concluida": False},
            {"nome": "Leitura", "descricao": "3 páginas e resumo", "concluida": False},
        ]
        return render_template("dashboard_aluno.html", missao=missao, pontos=280, sequencia=4)

    @app.get("/pwa-instalar")
    def pwa_instalar():
        return render_template("pwa_instalar.html")

    @app.get("/health")
    def health():
        return jsonify(status="ok", produto="NettStudy", ambiente=app.config["APP_ENV"])


def registrar_erros(app: Flask) -> None:
    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template("portal.html", erro="Página não encontrada."), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        return jsonify(erro="Erro interno do servidor.", status=500), 500


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=app.config["DEBUG"])
