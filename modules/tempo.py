# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\tempo.py
# Data e hora do último recode: 18/08/2026 00:01 -03:00
# Motivo da alteração: centralizar toda leitura de data e hora no fuso global configurado pela aplicação.

from datetime import date, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from config import Config


NOME_FUSO_HORARIO_APP = (Config.APP_FUSO or "").strip()

if not NOME_FUSO_HORARIO_APP:
    raise RuntimeError("APP_FUSO não pode ficar vazio.")

try:
    FUSO_HORARIO_APP = ZoneInfo(NOME_FUSO_HORARIO_APP)
except (ZoneInfoNotFoundError, ValueError) as erro:
    raise RuntimeError(f"APP_FUSO inválido: {NOME_FUSO_HORARIO_APP}") from erro


def agora_app() -> datetime:
    return datetime.now(FUSO_HORARIO_APP)


def data_app() -> date:
    return agora_app().date()


def data_iso_app() -> str:
    return data_app().isoformat()
