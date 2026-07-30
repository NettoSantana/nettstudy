# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\config.py
# Data e hora do último recode: 30/07/2026 20:15 -03:00
# Motivo da alteração: configurar recuperação de acesso e validação de e-mail.

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "troque-esta-chave-no-ambiente")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    DATABASE_PATH = os.getenv("NETTSTUDY_DB_PATH", str(BASE_DIR / "data" / "nettstudy.db"))
    BASE_URL = os.getenv("NETTSTUDY_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM = os.getenv("RESEND_FROM", "NettStudy <noreply@nettsan.ia.br>")
    RECUPERACAO_TOKEN_MINUTOS = int(os.getenv("RECUPERACAO_TOKEN_MINUTOS", "30"))
    VALIDACAO_EMAIL_HORAS = int(os.getenv("VALIDACAO_EMAIL_HORAS", "24"))
    VALIDACAO_EMAIL_REENVIO_SEGUNDOS = int(os.getenv("VALIDACAO_EMAIL_REENVIO_SEGUNDOS", "60"))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = APP_ENV == "production"
