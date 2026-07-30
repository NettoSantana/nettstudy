# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\database.py
# Data e hora do último recode: 30/07/2026 14:36 -03:00
# Motivo da alteração: incluir o cadastro transacional do responsável, aluno e vínculo familiar.

import sqlite3
from pathlib import Path
from typing import Any

from werkzeug.security import generate_password_hash


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    identificador TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('responsavel', 'aluno')),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT
);

CREATE TABLE IF NOT EXISTS responsaveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    nome_completo TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    nome_completo TEXT NOT NULL,
    nome_exibicao TEXT NOT NULL,
    data_nascimento TEXT,
    ano_escolar TEXT,
    avatar TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS responsavel_aluno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    parentesco TEXT,
    principal INTEGER NOT NULL DEFAULT 0 CHECK (principal IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (responsavel_id, aluno_id),
    FOREIGN KEY (responsavel_id) REFERENCES responsaveis(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_usuarios_identificador
    ON usuarios (identificador);

CREATE INDEX IF NOT EXISTS idx_responsavel_aluno_responsavel
    ON responsavel_aluno (responsavel_id);

CREATE INDEX IF NOT EXISTS idx_responsavel_aluno_aluno
    ON responsavel_aluno (aluno_id);
"""


def conectar(caminho_banco: str) -> sqlite3.Connection:
    Path(caminho_banco).parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco(caminho_banco: str) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA)
        _criar_dados_demonstracao(conexao)


def _criar_dados_demonstracao(conexao: sqlite3.Connection) -> None:
    total = conexao.execute(
        "SELECT COUNT(*) AS total FROM usuarios"
    ).fetchone()["total"]

    if total > 0:
        _garantir_vinculos_demonstracao(conexao)
        return

    cursor_responsavel = conexao.execute(
        """
        INSERT INTO usuarios (
            nome,
            identificador,
            senha_hash,
            perfil
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "Responsável Demo",
            "responsavel@nettstudy.local",
            generate_password_hash("NettStudy123"),
            "responsavel",
        ),
    )

    cursor_aluno = conexao.execute(
        """
        INSERT INTO usuarios (
            nome,
            identificador,
            senha_hash,
            perfil
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "João",
            "joao",
            generate_password_hash("1234"),
            "aluno",
        ),
    )

    responsavel_id = conexao.execute(
        """
        INSERT INTO responsaveis (
            usuario_id,
            nome_completo,
            email
        )
        VALUES (?, ?, ?)
        """,
        (
            cursor_responsavel.lastrowid,
            "Responsável Demo",
            "responsavel@nettstudy.local",
        ),
    ).lastrowid

    aluno_id = conexao.execute(
        """
        INSERT INTO alunos (
            usuario_id,
            nome_completo,
            nome_exibicao,
            ano_escolar
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            cursor_aluno.lastrowid,
            "João",
            "João",
            "5º ano",
        ),
    ).lastrowid

    conexao.execute(
        """
        INSERT INTO responsavel_aluno (
            responsavel_id,
            aluno_id,
            parentesco,
            principal
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            responsavel_id,
            aluno_id,
            "Responsável",
            1,
        ),
    )


def _garantir_vinculos_demonstracao(conexao: sqlite3.Connection) -> None:
    usuario_responsavel = conexao.execute(
        """
        SELECT id, nome, identificador
        FROM usuarios
        WHERE identificador = ?
          AND perfil = 'responsavel'
        """,
        ("responsavel@nettstudy.local",),
    ).fetchone()

    usuario_aluno = conexao.execute(
        """
        SELECT id, nome
        FROM usuarios
        WHERE identificador = ?
          AND perfil = 'aluno'
        """,
        ("joao",),
    ).fetchone()

    if not usuario_responsavel or not usuario_aluno:
        return

    conexao.execute(
        """
        INSERT OR IGNORE INTO responsaveis (
            usuario_id,
            nome_completo,
            email
        )
        VALUES (?, ?, ?)
        """,
        (
            usuario_responsavel["id"],
            usuario_responsavel["nome"],
            usuario_responsavel["identificador"],
        ),
    )

    conexao.execute(
        """
        INSERT OR IGNORE INTO alunos (
            usuario_id,
            nome_completo,
            nome_exibicao,
            ano_escolar
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            usuario_aluno["id"],
            usuario_aluno["nome"],
            usuario_aluno["nome"],
            "5º ano",
        ),
    )

    responsavel = conexao.execute(
        "SELECT id FROM responsaveis WHERE usuario_id = ?",
        (usuario_responsavel["id"],),
    ).fetchone()

    aluno = conexao.execute(
        "SELECT id FROM alunos WHERE usuario_id = ?",
        (usuario_aluno["id"],),
    ).fetchone()

    if responsavel and aluno:
        conexao.execute(
            """
            INSERT OR IGNORE INTO responsavel_aluno (
                responsavel_id,
                aluno_id,
                parentesco,
                principal
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                responsavel["id"],
                aluno["id"],
                "Responsável",
                1,
            ),
        )


def buscar_usuario_por_login(
    caminho_banco: str,
    identificador: str,
) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT
                id,
                nome,
                identificador,
                senha_hash,
                perfil
            FROM usuarios
            WHERE identificador = ?
              AND ativo = 1
            """,
            (identificador,),
        ).fetchone()

    return dict(registro) if registro else None


def buscar_responsavel_por_usuario(
    caminho_banco: str,
    usuario_id: int,
) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT
                id,
                usuario_id,
                nome_completo,
                email,
                telefone,
                ativo,
                criado_em
            FROM responsaveis
            WHERE usuario_id = ?
              AND ativo = 1
            """,
            (usuario_id,),
        ).fetchone()

    return dict(registro) if registro else None


def buscar_aluno_por_usuario(
    caminho_banco: str,
    usuario_id: int,
) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT
                id,
                usuario_id,
                nome_completo,
                nome_exibicao,
                data_nascimento,
                ano_escolar,
                avatar,
                ativo,
                criado_em
            FROM alunos
            WHERE usuario_id = ?
              AND ativo = 1
            """,
            (usuario_id,),
        ).fetchone()

    return dict(registro) if registro else None


def listar_alunos_do_responsavel(
    caminho_banco: str,
    usuario_responsavel_id: int,
) -> list[dict[str, Any]]:
    with conectar(caminho_banco) as conexao:
        registros = conexao.execute(
            """
            SELECT
                a.id,
                a.usuario_id,
                a.nome_completo,
                a.nome_exibicao,
                a.data_nascimento,
                a.ano_escolar,
                a.avatar,
                ra.parentesco,
                ra.principal
            FROM responsaveis r
            INNER JOIN responsavel_aluno ra
                ON ra.responsavel_id = r.id
            INNER JOIN alunos a
                ON a.id = ra.aluno_id
            WHERE r.usuario_id = ?
              AND r.ativo = 1
              AND a.ativo = 1
            ORDER BY
                ra.principal DESC,
                a.nome_exibicao ASC
            """,
            (usuario_responsavel_id,),
        ).fetchall()

    return [dict(registro) for registro in registros]


def identificador_disponivel(
    caminho_banco: str,
    identificador: str,
) -> bool:
    identificador_normalizado = identificador.strip().lower()

    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT id
            FROM usuarios
            WHERE identificador = ?
            """,
            (identificador_normalizado,),
        ).fetchone()

    return registro is None


def cadastrar_familia(
    caminho_banco: str,
    nome_responsavel: str,
    email_responsavel: str,
    senha_responsavel: str,
    telefone_responsavel: str,
    nome_aluno: str,
    nome_exibicao_aluno: str,
    ano_escolar: str,
    usuario_aluno: str,
    pin_aluno: str,
    parentesco: str = "Responsável",
) -> dict[str, int]:
    nome_responsavel = nome_responsavel.strip()
    email_responsavel = email_responsavel.strip().lower()
    telefone_responsavel = telefone_responsavel.strip()
    nome_aluno = nome_aluno.strip()
    nome_exibicao_aluno = nome_exibicao_aluno.strip()
    ano_escolar = ano_escolar.strip()
    usuario_aluno = usuario_aluno.strip().lower()
    parentesco = parentesco.strip() or "Responsável"

    if not nome_responsavel:
        raise ValueError("Informe o nome do responsável.")

    if not email_responsavel:
        raise ValueError("Informe o e-mail do responsável.")

    if len(senha_responsavel) < 8:
        raise ValueError("A senha do responsável deve ter pelo menos 8 caracteres.")

    if not nome_aluno:
        raise ValueError("Informe o nome do aluno.")

    if not nome_exibicao_aluno:
        nome_exibicao_aluno = nome_aluno.split()[0]

    if not usuario_aluno:
        raise ValueError("Informe o usuário do aluno.")

    if not pin_aluno.isdigit() or len(pin_aluno) != 4:
        raise ValueError("O PIN do aluno deve conter exatamente 4 números.")

    try:
        with conectar(caminho_banco) as conexao:
            cursor_usuario_responsavel = conexao.execute(
                """
                INSERT INTO usuarios (
                    nome,
                    identificador,
                    senha_hash,
                    perfil
                )
                VALUES (?, ?, ?, 'responsavel')
                """,
                (
                    nome_responsavel,
                    email_responsavel,
                    generate_password_hash(senha_responsavel),
                ),
            )

            cursor_responsavel = conexao.execute(
                """
                INSERT INTO responsaveis (
                    usuario_id,
                    nome_completo,
                    email,
                    telefone
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    cursor_usuario_responsavel.lastrowid,
                    nome_responsavel,
                    email_responsavel,
                    telefone_responsavel or None,
                ),
            )

            cursor_usuario_aluno = conexao.execute(
                """
                INSERT INTO usuarios (
                    nome,
                    identificador,
                    senha_hash,
                    perfil
                )
                VALUES (?, ?, ?, 'aluno')
                """,
                (
                    nome_exibicao_aluno,
                    usuario_aluno,
                    generate_password_hash(pin_aluno),
                ),
            )

            cursor_aluno = conexao.execute(
                """
                INSERT INTO alunos (
                    usuario_id,
                    nome_completo,
                    nome_exibicao,
                    ano_escolar
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    cursor_usuario_aluno.lastrowid,
                    nome_aluno,
                    nome_exibicao_aluno,
                    ano_escolar or None,
                ),
            )

            conexao.execute(
                """
                INSERT INTO responsavel_aluno (
                    responsavel_id,
                    aluno_id,
                    parentesco,
                    principal
                )
                VALUES (?, ?, ?, 1)
                """,
                (
                    cursor_responsavel.lastrowid,
                    cursor_aluno.lastrowid,
                    parentesco,
                ),
            )

            return {
                "usuario_responsavel_id": int(
                    cursor_usuario_responsavel.lastrowid
                ),
                "responsavel_id": int(cursor_responsavel.lastrowid),
                "usuario_aluno_id": int(cursor_usuario_aluno.lastrowid),
                "aluno_id": int(cursor_aluno.lastrowid),
            }

    except sqlite3.IntegrityError as erro:
        mensagem = str(erro).lower()

        if "usuarios.identificador" in mensagem:
            raise ValueError(
                "O e-mail do responsável ou o usuário do aluno já está em uso."
            ) from erro

        if "responsaveis.email" in mensagem:
            raise ValueError(
                "Já existe um responsável cadastrado com este e-mail."
            ) from erro

        raise ValueError(
            "Não foi possível concluir o cadastro. Revise os dados informados."
        ) from erro
