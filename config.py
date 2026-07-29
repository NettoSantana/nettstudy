# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\config.py
# Data e hora do último recode: 29/07/2026 16:15 -03:00
# Motivo da alteração: centralizar configurações de ambiente e banco do NettStudy.

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
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = APP_ENV == "production"
