# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\database.py
# Data e hora do último recode: 29/07/2026 16:15 -03:00
# Motivo da alteração: criar e acessar o banco SQLite inicial do NettStudy.

import sqlite3
from pathlib import Path
from typing import Any

from werkzeug.security import generate_password_hash

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    identificador TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('responsavel', 'aluno')),
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def conectar(caminho_banco: str) -> sqlite3.Connection:
    Path(caminho_banco).parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco(caminho_banco: str) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA)
        total = conexao.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()["total"]
        if total == 0:
            conexao.executemany(
                "INSERT INTO usuarios (nome, identificador, senha_hash, perfil) VALUES (?, ?, ?, ?)",
                [
                    ("Responsável Demo", "responsavel@nettstudy.local", generate_password_hash("NettStudy123"), "responsavel"),
                    ("João", "joao", generate_password_hash("1234"), "aluno"),
                ],
            )


def buscar_usuario_por_login(caminho_banco: str, identificador: str) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            "SELECT id, nome, identificador, senha_hash, perfil FROM usuarios WHERE identificador = ? AND ativo = 1",
            (identificador,),
        ).fetchone()
    return dict(registro) if registro else None
