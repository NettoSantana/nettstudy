# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\app.py
# Data e hora do último recode: 30/07/2026 14:40 -03:00
# Motivo da alteração: adicionar o cadastro público de responsável e aluno em um único fluxo.

import os
from functools import wraps
from typing import Any, Callable

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from config import Config
from database import (
    buscar_aluno_por_usuario,
    buscar_responsavel_por_usuario,
    buscar_usuario_por_login,
    cadastrar_familia,
    inicializar_banco,
    listar_alunos_do_responsavel,
)


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

            usuario = buscar_usuario_por_login(
                app.config["DATABASE_PATH"],
                identificador,
            )

            if not usuario or not check_password_hash(
                usuario["senha_hash"],
                senha,
            ):
                flash("Login ou senha inválidos.", "erro")
                return render_template(
                    "login.html",
                    identificador=identificador,
                ), 401

            session.clear()
            session.update(
                usuario_id=usuario["id"],
                nome=usuario["nome"],
                perfil=usuario["perfil"],
            )

            destino = (
                "dashboard_responsavel"
                if usuario["perfil"] == "responsavel"
                else "dashboard_aluno"
            )

            return redirect(url_for(destino))

        return render_template("login.html")

    @app.route("/novo-cadastro", methods=["GET", "POST"])
    def novo_cadastro():
        if session.get("usuario_id"):
            destino = (
                "dashboard_responsavel"
                if session.get("perfil") == "responsavel"
                else "dashboard_aluno"
            )
            return redirect(url_for(destino))

        dados = {
            "nome_responsavel": "",
            "email_responsavel": "",
            "telefone_responsavel": "",
            "parentesco": "Responsável",
            "nome_aluno": "",
            "nome_exibicao_aluno": "",
            "ano_escolar": "",
            "usuario_aluno": "",
        }

        if request.method == "POST":
            dados = {
                "nome_responsavel": request.form.get(
                    "nome_responsavel",
                    "",
                ).strip(),
                "email_responsavel": request.form.get(
                    "email_responsavel",
                    "",
                ).strip().lower(),
                "telefone_responsavel": request.form.get(
                    "telefone_responsavel",
                    "",
                ).strip(),
                "parentesco": request.form.get(
                    "parentesco",
                    "Responsável",
                ).strip(),
                "nome_aluno": request.form.get(
                    "nome_aluno",
                    "",
                ).strip(),
                "nome_exibicao_aluno": request.form.get(
                    "nome_exibicao_aluno",
                    "",
                ).strip(),
                "ano_escolar": request.form.get(
                    "ano_escolar",
                    "",
                ).strip(),
                "usuario_aluno": request.form.get(
                    "usuario_aluno",
                    "",
                ).strip().lower(),
            }

            senha_responsavel = request.form.get(
                "senha_responsavel",
                "",
            )
            confirmar_senha = request.form.get(
                "confirmar_senha",
                "",
            )
            pin_aluno = request.form.get(
                "pin_aluno",
                "",
            ).strip()
            confirmar_pin = request.form.get(
                "confirmar_pin",
                "",
            ).strip()

            if senha_responsavel != confirmar_senha:
                flash(
                    "A confirmação da senha do responsável não confere.",
                    "erro",
                )
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            if pin_aluno != confirmar_pin:
                flash(
                    "A confirmação do PIN do aluno não confere.",
                    "erro",
                )
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            try:
                cadastro = cadastrar_familia(
                    caminho_banco=app.config["DATABASE_PATH"],
                    nome_responsavel=dados["nome_responsavel"],
                    email_responsavel=dados["email_responsavel"],
                    senha_responsavel=senha_responsavel,
                    telefone_responsavel=dados["telefone_responsavel"],
                    nome_aluno=dados["nome_aluno"],
                    nome_exibicao_aluno=dados["nome_exibicao_aluno"],
                    ano_escolar=dados["ano_escolar"],
                    usuario_aluno=dados["usuario_aluno"],
                    pin_aluno=pin_aluno,
                    parentesco=dados["parentesco"],
                )
            except ValueError as erro:
                flash(str(erro), "erro")
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            session.clear()
            session.update(
                usuario_id=cadastro["usuario_responsavel_id"],
                nome=dados["nome_responsavel"],
                perfil="responsavel",
            )

            flash(
                "Cadastro criado com sucesso. Bem-vindo ao NettStudy!",
                "sucesso",
            )
            return redirect(url_for("dashboard_responsavel"))

        return render_template(
            "novo_cadastro.html",
            dados=dados,
        )

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
        usuario_id = int(session["usuario_id"])

        responsavel = buscar_responsavel_por_usuario(
            app.config["DATABASE_PATH"],
            usuario_id,
        )

        alunos = listar_alunos_do_responsavel(
            app.config["DATABASE_PATH"],
            usuario_id,
        )

        aluno = None

        if alunos:
            aluno_registrado = alunos[0]
            aluno = {
                "id": aluno_registrado["id"],
                "nome": aluno_registrado["nome_exibicao"],
                "nome_completo": aluno_registrado["nome_completo"],
                "ano_escolar": aluno_registrado["ano_escolar"] or "Não informado",
                "parentesco": aluno_registrado["parentesco"] or "Responsável",
                "principal": bool(aluno_registrado["principal"]),
                "sequencia": 0,
                "pontos": 0,
                "progresso_dia": 0,
                "atividades": [
                    {
                        "nome": "Português",
                        "status": "Pendente",
                        "progresso": 0,
                    },
                    {
                        "nome": "Matemática",
                        "status": "Pendente",
                        "progresso": 0,
                    },
                    {
                        "nome": "Leitura",
                        "status": "Pendente",
                        "progresso": 0,
                    },
                ],
            }

        return render_template(
            "dashboard_responsavel.html",
            responsavel=responsavel,
            alunos=alunos,
            aluno=aluno,
        )

    @app.get("/aluno")
    @login_obrigatorio("aluno")
    def dashboard_aluno():
        usuario_id = int(session["usuario_id"])

        aluno = buscar_aluno_por_usuario(
            app.config["DATABASE_PATH"],
            usuario_id,
        )

        if not aluno:
            session.clear()
            flash(
                "O cadastro do aluno não foi encontrado. Entre novamente.",
                "erro",
            )
            return redirect(url_for("login"))

        missao = [
            {
                "nome": "Português",
                "descricao": "10 questões",
                "concluida": False,
            },
            {
                "nome": "Matemática",
                "descricao": "10 questões",
                "concluida": False,
            },
            {
                "nome": "Leitura",
                "descricao": "3 páginas e resumo",
                "concluida": False,
            },
        ]

        return render_template(
            "dashboard_aluno.html",
            aluno=aluno,
            missao=missao,
            pontos=0,
            sequencia=0,
        )

    @app.get("/pwa-instalar")
    def pwa_instalar():
        return render_template("pwa_instalar.html")

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            produto="NettStudy",
            ambiente=app.config["APP_ENV"],
        )


def registrar_erros(app: Flask) -> None:
    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template(
            "portal.html",
            erro="Página não encontrada.",
        ), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        return jsonify(
            erro="Erro interno do servidor.",
            status=500,
        ), 500


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=app.config["DEBUG"],
    )
