# Caminho completo: C:\\Users\\vlula\\OneDrive\\Área de Trabalho\\Projetos Backup\\NETTSTUDY\\app.py
# Data e hora do último recode: 29/07/2026 16:12 -03:00
# Motivo da alteração: criar a base inicial executável do projeto NettStudy em Flask.

import os
from pathlib import Path
from typing import Final

from flask import Flask, jsonify, render_template


BASE_DIR: Final[Path] = Path(__file__).resolve().parent
DATA_DIR: Final[Path] = BASE_DIR / "data"
DEFAULT_DATABASE_PATH: Final[Path] = DATA_DIR / "nettstudy.db"


def create_app() -> Flask:
    """Cria e configura a aplicação Flask do NettStudy."""
    app = Flask(__name__)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-change-this-secret-key"),
        DATABASE_PATH=os.getenv(
            "NETTSTUDY_DB_PATH",
            str(DEFAULT_DATABASE_PATH),
        ),
        JSON_AS_ASCII=False,
    )

    registrar_rotas(app)
    registrar_erros(app)

    return app


def registrar_rotas(app: Flask) -> None:
    """Registra somente as rotas iniciais do projeto."""

    @app.get("/")
    def inicio():
        return render_template(
            "portal.html",
            nome_produto="NettStudy",
            mensagem="Aprender, praticar e evoluir.",
        )

    @app.get("/login")
    def login():
        return render_template(
            "login.html",
            nome_produto="NettStudy",
        )

    @app.get("/portal")
    def portal():
        return render_template(
            "portal.html",
            nome_produto="NettStudy",
            mensagem="Escolha como deseja acessar.",
        )

    @app.get("/responsavel")
    def dashboard_responsavel():
        return render_template(
            "dashboard_responsavel.html",
            nome_produto="NettStudy",
        )

    @app.get("/aluno")
    def dashboard_aluno():
        return render_template(
            "dashboard_aluno.html",
            nome_produto="NettStudy",
        )

    @app.get("/pwa-instalar")
    def pwa_instalar():
        return render_template(
            "pwa_instalar.html",
            nome_produto="NettStudy",
        )

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            produto="NettStudy",
            ambiente=os.getenv("FLASK_ENV", "production"),
        )


def registrar_erros(app: Flask) -> None:
    """Padroniza respostas básicas de erro."""

    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return (
            jsonify(
                erro="Página não encontrada.",
                status=404,
            ),
            404,
        )

    @app.errorhandler(500)
    def erro_interno(_erro):
        return (
            jsonify(
                erro="Erro interno do servidor.",
                status=500,
            ),
            500,
        )


app = create_app()


if __name__ == "__main__":
    porta = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"

    app.run(
        host="0.0.0.0",
        port=porta,
        debug=debug,
    )
