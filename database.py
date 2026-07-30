# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\database.py
# Data e hora do último recode: 30/07/2026 19:36 -03:00
# Motivo da alteração: adicionar recuperação segura da senha do responsável e do PIN dos alunos.

import hashlib
import json
import random
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
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

CREATE TABLE IF NOT EXISTS anamneses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL UNIQUE,
    idade INTEGER NOT NULL CHECK (idade BETWEEN 4 AND 18),
    ano_escolar TEXT NOT NULL,
    dificuldades TEXT NOT NULL,
    materias_preferidas TEXT,
    nivel_leitura TEXT NOT NULL,
    tempo_concentracao INTEGER NOT NULL CHECK (tempo_concentracao BETWEEN 5 AND 180),
    preferencia_interacao TEXT NOT NULL CHECK (preferencia_interacao IN ('texto', 'voz', 'ambos')),
    objetivo_principal TEXT NOT NULL,
    observacoes TEXT,
    concluida INTEGER NOT NULL DEFAULT 1 CHECK (concluida IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_usuarios_identificador
    ON usuarios (identificador);

CREATE INDEX IF NOT EXISTS idx_responsavel_aluno_responsavel
    ON responsavel_aluno (responsavel_id);

CREATE INDEX IF NOT EXISTS idx_responsavel_aluno_aluno
    ON responsavel_aluno (aluno_id);

CREATE TABLE IF NOT EXISTS atividades_diarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    materia TEXT NOT NULL CHECK (materia IN ('matematica', 'portugues', 'leitura')),
    status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'concluida')),
    acertos INTEGER NOT NULL DEFAULT 0,
    total_questoes INTEGER NOT NULL DEFAULT 0,
    pontos INTEGER NOT NULL DEFAULT 0,
    concluida_em TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (aluno_id, data_atividade, materia),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS respostas_atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atividade_id INTEGER NOT NULL,
    questao_codigo TEXT NOT NULL,
    resposta TEXT,
    correta INTEGER NOT NULL DEFAULT 0 CHECK (correta IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (atividade_id, questao_codigo),
    FOREIGN KEY (atividade_id) REFERENCES atividades_diarias(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resumos_leitura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atividade_id INTEGER NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    resumo TEXT NOT NULL,
    valido INTEGER NOT NULL DEFAULT 0 CHECK (valido IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atividade_id) REFERENCES atividades_diarias(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_atividades_aluno_data
    ON atividades_diarias (aluno_id, data_atividade);

CREATE TABLE IF NOT EXISTS sessoes_adaptativas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    materia TEXT NOT NULL CHECK (materia IN ('matematica', 'portugues')),
    fila_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ativa' CHECK (status IN ('ativa', 'concluida')),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    concluida_em TEXT,
    UNIQUE (aluno_id, data_atividade, materia),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tentativas_adaptativas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id INTEGER NOT NULL,
    questao_codigo TEXT NOT NULL,
    numero_tentativa INTEGER NOT NULL,
    resposta TEXT NOT NULL,
    correta INTEGER NOT NULL DEFAULT 0 CHECK (correta IN (0, 1)),
    dica_nivel INTEGER NOT NULL DEFAULT 0 CHECK (dica_nivel BETWEEN 0 AND 3),
    resposta_revelada INTEGER NOT NULL DEFAULT 0 CHECK (resposta_revelada IN (0, 1)),
    pontos INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (sessao_id, questao_codigo, numero_tentativa),
    FOREIGN KEY (sessao_id) REFERENCES sessoes_adaptativas(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessoes_adaptativas_aluno_data
    ON sessoes_adaptativas (aluno_id, data_atividade, materia);

CREATE INDEX IF NOT EXISTS idx_tentativas_adaptativas_sessao
    ON tentativas_adaptativas (sessao_id, questao_codigo);
"""


LEITURA_ADAPTATIVA_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessoes_leitura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    historia_id TEXT NOT NULL,
    titulo TEXT NOT NULL,
    fase TEXT NOT NULL DEFAULT 'leitura'
        CHECK (fase IN ('leitura', 'perguntas', 'resumo', 'concluida')),
    fila_json TEXT NOT NULL DEFAULT '[]',
    pontos_perguntas INTEGER NOT NULL DEFAULT 0,
    acertos_perguntas INTEGER NOT NULL DEFAULT 0,
    total_perguntas INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    concluida_em TEXT,
    UNIQUE (aluno_id, data_atividade),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tentativas_leitura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id INTEGER NOT NULL,
    pergunta_codigo TEXT NOT NULL,
    numero_tentativa INTEGER NOT NULL,
    resposta TEXT NOT NULL,
    correta INTEGER NOT NULL DEFAULT 0 CHECK (correta IN (0, 1)),
    dica_nivel INTEGER NOT NULL DEFAULT 0 CHECK (dica_nivel BETWEEN 0 AND 3),
    resposta_revelada INTEGER NOT NULL DEFAULT 0 CHECK (resposta_revelada IN (0, 1)),
    pontos INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (sessao_id, pergunta_codigo, numero_tentativa),
    FOREIGN KEY (sessao_id) REFERENCES sessoes_leitura(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS versoes_resumo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id INTEGER NOT NULL,
    numero_versao INTEGER NOT NULL,
    resumo TEXT NOT NULL,
    total_palavras INTEGER NOT NULL DEFAULT 0,
    pontuacao INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL
        CHECK (status IN ('refazer', 'complementar', 'concluido')),
    criterios_json TEXT NOT NULL,
    retorno_json TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (sessao_id, numero_versao),
    FOREIGN KEY (sessao_id) REFERENCES sessoes_leitura(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessoes_leitura_aluno_data
    ON sessoes_leitura (aluno_id, data_atividade);

CREATE INDEX IF NOT EXISTS idx_tentativas_leitura_sessao
    ON tentativas_leitura (sessao_id, pergunta_codigo);

CREATE INDEX IF NOT EXISTS idx_versoes_resumo_sessao
    ON versoes_resumo (sessao_id, numero_versao);
"""


RESET_MISSAO_SCHEMA = """
CREATE TABLE IF NOT EXISTS resets_missao_diaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel_usuario_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    motivo TEXT,
    historico_json TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (aluno_id, data_atividade),
    FOREIGN KEY (responsavel_usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_resets_missao_aluno_data
    ON resets_missao_diaria (aluno_id, data_atividade);
"""


RECUPERACAO_ACESSO_SCHEMA = """
CREATE TABLE IF NOT EXISTS tokens_recuperacao_acesso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel_id INTEGER NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expira_em TEXT NOT NULL,
    usado_em TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (responsavel_id) REFERENCES responsaveis(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tokens_recuperacao_hash
    ON tokens_recuperacao_acesso (token_hash);

CREATE INDEX IF NOT EXISTS idx_tokens_recuperacao_responsavel
    ON tokens_recuperacao_acesso (responsavel_id, criado_em);
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
        conexao.executescript(LEITURA_ADAPTATIVA_SCHEMA)
        conexao.executescript(RESET_MISSAO_SCHEMA)
        conexao.executescript(RECUPERACAO_ACESSO_SCHEMA)
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



def buscar_anamnese_por_aluno(
    caminho_banco: str,
    aluno_id: int,
) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                idade,
                ano_escolar,
                dificuldades,
                materias_preferidas,
                nivel_leitura,
                tempo_concentracao,
                preferencia_interacao,
                objetivo_principal,
                observacoes,
                concluida,
                criado_em,
                atualizado_em
            FROM anamneses
            WHERE aluno_id = ?
            """,
            (aluno_id,),
        ).fetchone()

    return dict(registro) if registro else None


def salvar_anamnese(
    caminho_banco: str,
    aluno_id: int,
    idade: int,
    ano_escolar: str,
    dificuldades: str,
    materias_preferidas: str,
    nivel_leitura: str,
    tempo_concentracao: int,
    preferencia_interacao: str,
    objetivo_principal: str,
    observacoes: str,
) -> None:
    ano_escolar = ano_escolar.strip()
    dificuldades = dificuldades.strip()
    materias_preferidas = materias_preferidas.strip()
    nivel_leitura = nivel_leitura.strip()
    preferencia_interacao = preferencia_interacao.strip().lower()
    objetivo_principal = objetivo_principal.strip()
    observacoes = observacoes.strip()

    if idade < 4 or idade > 18:
        raise ValueError("Informe uma idade entre 4 e 18 anos.")
    if not ano_escolar:
        raise ValueError("Informe o ano escolar.")
    if not dificuldades:
        raise ValueError("Informe as principais dificuldades do aluno.")
    if nivel_leitura not in {"iniciante", "basico", "intermediario", "avancado"}:
        raise ValueError("Selecione um nível de leitura válido.")
    if tempo_concentracao < 5 or tempo_concentracao > 180:
        raise ValueError("O tempo de concentração deve ficar entre 5 e 180 minutos.")
    if preferencia_interacao not in {"texto", "voz", "ambos"}:
        raise ValueError("Selecione uma preferência de interação válida.")
    if not objetivo_principal:
        raise ValueError("Informe o objetivo principal.")

    with conectar(caminho_banco) as conexao:
        aluno = conexao.execute(
            "SELECT id FROM alunos WHERE id = ? AND ativo = 1",
            (aluno_id,),
        ).fetchone()
        if not aluno:
            raise ValueError("Aluno não encontrado.")

        conexao.execute(
            """
            INSERT INTO anamneses (
                aluno_id,
                idade,
                ano_escolar,
                dificuldades,
                materias_preferidas,
                nivel_leitura,
                tempo_concentracao,
                preferencia_interacao,
                objetivo_principal,
                observacoes,
                concluida
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(aluno_id) DO UPDATE SET
                idade = excluded.idade,
                ano_escolar = excluded.ano_escolar,
                dificuldades = excluded.dificuldades,
                materias_preferidas = excluded.materias_preferidas,
                nivel_leitura = excluded.nivel_leitura,
                tempo_concentracao = excluded.tempo_concentracao,
                preferencia_interacao = excluded.preferencia_interacao,
                objetivo_principal = excluded.objetivo_principal,
                observacoes = excluded.observacoes,
                concluida = 1,
                atualizado_em = CURRENT_TIMESTAMP
            """,
            (
                aluno_id,
                idade,
                ano_escolar,
                dificuldades,
                materias_preferidas or None,
                nivel_leitura,
                tempo_concentracao,
                preferencia_interacao,
                objetivo_principal,
                observacoes or None,
            ),
        )



def registrar_resultado_atividade(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str,
    materia: str,
    resultado: dict[str, Any],
    titulo_leitura: str | None = None,
) -> int:
    if materia not in {"matematica", "portugues", "leitura"}:
        raise ValueError("Matéria inválida.")

    with conectar(caminho_banco) as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO atividades_diarias (
                aluno_id, data_atividade, materia, status,
                acertos, total_questoes, pontos, concluida_em
            )
            VALUES (?, ?, ?, 'concluida', ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(aluno_id, data_atividade, materia) DO UPDATE SET
                status = 'concluida',
                acertos = excluded.acertos,
                total_questoes = excluded.total_questoes,
                pontos = excluded.pontos,
                concluida_em = CURRENT_TIMESTAMP
            """,
            (
                aluno_id,
                data_atividade,
                materia,
                int(resultado["acertos"]),
                int(resultado["total"]),
                int(resultado["pontos"]),
            ),
        )
        atividade = conexao.execute(
            "SELECT id FROM atividades_diarias WHERE aluno_id = ? AND data_atividade = ? AND materia = ?",
            (aluno_id, data_atividade, materia),
        ).fetchone()
        atividade_id = int(atividade["id"])

        conexao.execute("DELETE FROM respostas_atividades WHERE atividade_id = ?", (atividade_id,))
        for detalhe in resultado["detalhes"]:
            conexao.execute(
                """
                INSERT INTO respostas_atividades (
                    atividade_id, questao_codigo, resposta, correta
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    atividade_id,
                    detalhe["id"],
                    detalhe.get("resposta") or None,
                    int(bool(detalhe["acertou"])),
                ),
            )

        if materia == "leitura":
            conexao.execute(
                """
                INSERT INTO resumos_leitura (
                    atividade_id, titulo, resumo, valido
                ) VALUES (?, ?, ?, ?)
                ON CONFLICT(atividade_id) DO UPDATE SET
                    titulo = excluded.titulo,
                    resumo = excluded.resumo,
                    valido = excluded.valido
                """,
                (
                    atividade_id,
                    titulo_leitura or "Leitura do dia",
                    resultado.get("resumo", ""),
                    int(bool(resultado.get("resumo_valido"))),
                ),
            )

    return atividade_id


def obter_resumo_diario(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str,
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        registros = conexao.execute(
            """
            SELECT materia, status, acertos, total_questoes, pontos
            FROM atividades_diarias
            WHERE aluno_id = ? AND data_atividade = ?
            """,
            (aluno_id, data_atividade),
        ).fetchall()

        pontos_total = conexao.execute(
            "SELECT COALESCE(SUM(pontos), 0) AS total FROM atividades_diarias WHERE aluno_id = ?",
            (aluno_id,),
        ).fetchone()["total"]

    por_materia = {registro["materia"]: dict(registro) for registro in registros}
    concluidas = sum(1 for registro in registros if registro["status"] == "concluida")
    return {
        "materias": por_materia,
        "concluidas": concluidas,
        "progresso": round((concluidas / 3) * 100),
        "pontos": int(pontos_total),
        "sequencia": 1 if concluidas == 3 else 0,
    }



def obter_ou_criar_sessao_adaptativa(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str,
    materia: str,
    codigos_questoes: list[str],
) -> dict[str, Any]:
    if materia not in {"matematica", "portugues"}:
        raise ValueError("Matéria adaptativa inválida.")

    with conectar(caminho_banco) as conexao:
        sessao = conexao.execute(
            """
            SELECT id, fila_json, status
            FROM sessoes_adaptativas
            WHERE aluno_id = ? AND data_atividade = ? AND materia = ?
            """,
            (aluno_id, data_atividade, materia),
        ).fetchone()

        if not sessao:
            fila = list(codigos_questoes)
            random.shuffle(fila)
            cursor = conexao.execute(
                """
                INSERT INTO sessoes_adaptativas (
                    aluno_id, data_atividade, materia, fila_json
                ) VALUES (?, ?, ?, ?)
                """,
                (aluno_id, data_atividade, materia, json.dumps(fila)),
            )
            sessao_id = int(cursor.lastrowid)
            status = "ativa"
        else:
            sessao_id = int(sessao["id"])
            fila = json.loads(sessao["fila_json"])
            status = sessao["status"]

        resolvidas = max(0, len(codigos_questoes) - len(fila))
        progresso = round((resolvidas / len(codigos_questoes)) * 100) if codigos_questoes else 0

        return {
            "id": sessao_id,
            "fila": fila,
            "status": status,
            "questao_atual": fila[0] if fila else None,
            "progresso": progresso,
        }


def registrar_tentativa_adaptativa(
    caminho_banco: str,
    sessao_id: int,
    questao_codigo: str,
    resposta: str,
    correta: bool,
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        sessao = conexao.execute(
            """
            SELECT id, aluno_id, data_atividade, materia, fila_json, status
            FROM sessoes_adaptativas
            WHERE id = ?
            """,
            (sessao_id,),
        ).fetchone()

        if not sessao or sessao["status"] != "ativa":
            raise ValueError("Esta atividade não está mais ativa.")

        fila = json.loads(sessao["fila_json"])
        if not fila or fila[0] != questao_codigo:
            raise ValueError("A questão enviada não corresponde à questão atual.")

        tentativa_anterior = conexao.execute(
            """
            SELECT COUNT(*) AS total
            FROM tentativas_adaptativas
            WHERE sessao_id = ? AND questao_codigo = ?
            """,
            (sessao_id, questao_codigo),
        ).fetchone()["total"]
        numero_tentativa = int(tentativa_anterior) + 1

        pontos_por_tentativa = {1: 10, 2: 8, 3: 6, 4: 4, 5: 2}
        pontos = pontos_por_tentativa.get(numero_tentativa, 0) if correta else 0
        dica_nivel = 0
        resposta_revelada = 0

        if not correta:
            if numero_tentativa == 2:
                dica_nivel = 1
            elif numero_tentativa == 3:
                dica_nivel = 2
            elif numero_tentativa == 4:
                dica_nivel = 3
            elif numero_tentativa >= 5:
                dica_nivel = 3
                resposta_revelada = 1

        conexao.execute(
            """
            INSERT INTO tentativas_adaptativas (
                sessao_id, questao_codigo, numero_tentativa, resposta,
                correta, dica_nivel, resposta_revelada, pontos
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sessao_id,
                questao_codigo,
                numero_tentativa,
                resposta,
                int(correta),
                dica_nivel,
                resposta_revelada,
                pontos,
            ),
        )

        fila.pop(0)
        if not correta and numero_tentativa < 5:
            fila.append(questao_codigo)

        concluida = len(fila) == 0
        conexao.execute(
            """
            UPDATE sessoes_adaptativas
            SET fila_json = ?,
                status = ?,
                atualizado_em = CURRENT_TIMESTAMP,
                concluida_em = CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE concluida_em END
            WHERE id = ?
            """,
            (
                json.dumps(fila),
                "concluida" if concluida else "ativa",
                int(concluida),
                sessao_id,
            ),
        )

        return {
            "sessao_id": sessao_id,
            "numero_tentativa": numero_tentativa,
            "correta": bool(correta),
            "dica_nivel": dica_nivel,
            "resposta_revelada": bool(resposta_revelada),
            "pontos": pontos,
            "concluida": concluida,
        }


def finalizar_sessao_adaptativa(
    caminho_banco: str,
    sessao_id: int,
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        sessao = conexao.execute(
            """
            SELECT id, aluno_id, data_atividade, materia, status
            FROM sessoes_adaptativas
            WHERE id = ?
            """,
            (sessao_id,),
        ).fetchone()
        if not sessao or sessao["status"] != "concluida":
            raise ValueError("A sessão ainda não foi concluída.")

        linhas = conexao.execute(
            """
            SELECT
                questao_codigo,
                MAX(numero_tentativa) AS tentativas,
                MAX(correta) AS acertou,
                MAX(resposta_revelada) AS resposta_revelada,
                SUM(pontos) AS pontos
            FROM tentativas_adaptativas
            WHERE sessao_id = ?
            GROUP BY questao_codigo
            ORDER BY questao_codigo
            """,
            (sessao_id,),
        ).fetchall()

        detalhes = []
        for linha in linhas:
            ultima = conexao.execute(
                """
                SELECT resposta
                FROM tentativas_adaptativas
                WHERE sessao_id = ? AND questao_codigo = ?
                ORDER BY numero_tentativa DESC
                LIMIT 1
                """,
                (sessao_id, linha["questao_codigo"]),
            ).fetchone()
            detalhes.append(
                {
                    "id": linha["questao_codigo"],
                    "resposta": ultima["resposta"] if ultima else "",
                    "acertou": bool(linha["acertou"]),
                    "tentativas": int(linha["tentativas"]),
                    "resposta_revelada": bool(linha["resposta_revelada"]),
                    "pontos": int(linha["pontos"] or 0),
                }
            )

        resultado = {
            "acertos": sum(1 for item in detalhes if item["acertou"]),
            "total": len(detalhes),
            "pontos": sum(item["pontos"] for item in detalhes),
            "detalhes": detalhes,
        }

    registrar_resultado_atividade(
        caminho_banco,
        int(sessao["aluno_id"]),
        sessao["data_atividade"],
        sessao["materia"],
        resultado,
    )
    return resultado


def obter_ou_criar_sessao_leitura(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str,
    historia_id: str,
    titulo: str,
    codigos_perguntas: list[str],
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT *
            FROM sessoes_leitura
            WHERE aluno_id = ? AND data_atividade = ?
            """,
            (aluno_id, data_atividade),
        ).fetchone()

        if not registro:
            fila = list(codigos_perguntas)
            random.shuffle(fila)
            cursor = conexao.execute(
                """
                INSERT INTO sessoes_leitura (
                    aluno_id,
                    data_atividade,
                    historia_id,
                    titulo,
                    fase,
                    fila_json,
                    total_perguntas
                )
                VALUES (?, ?, ?, ?, 'leitura', ?, ?)
                """,
                (
                    aluno_id,
                    data_atividade,
                    historia_id,
                    titulo,
                    json.dumps(fila),
                    len(codigos_perguntas),
                ),
            )
            sessao_id = int(cursor.lastrowid)
            fase = "leitura"
            pontos = 0
            acertos = 0
        else:
            sessao_id = int(registro["id"])
            fila = json.loads(registro["fila_json"])
            fase = registro["fase"]
            pontos = int(registro["pontos_perguntas"])
            acertos = int(registro["acertos_perguntas"])

        return {
            "id": sessao_id,
            "fase": fase,
            "fila": fila,
            "pergunta_atual": fila[0] if fila else None,
            "pontos_perguntas": pontos,
            "acertos_perguntas": acertos,
            "total_perguntas": len(codigos_perguntas),
        }


def iniciar_perguntas_leitura(
    caminho_banco: str,
    sessao_id: int,
) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            """
            UPDATE sessoes_leitura
            SET fase = 'perguntas',
                atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ? AND fase = 'leitura'
            """,
            (sessao_id,),
        )


def registrar_tentativa_leitura(
    caminho_banco: str,
    sessao_id: int,
    pergunta_codigo: str,
    resposta: str,
    correta: bool,
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        sessao = conexao.execute(
            """
            SELECT *
            FROM sessoes_leitura
            WHERE id = ?
            """,
            (sessao_id,),
        ).fetchone()

        if not sessao or sessao["fase"] != "perguntas":
            raise ValueError("A etapa de perguntas não está ativa.")

        fila = json.loads(sessao["fila_json"])
        if not fila or fila[0] != pergunta_codigo:
            raise ValueError("A pergunta enviada não corresponde à pergunta atual.")

        total_anterior = conexao.execute(
            """
            SELECT COUNT(*) AS total
            FROM tentativas_leitura
            WHERE sessao_id = ? AND pergunta_codigo = ?
            """,
            (sessao_id, pergunta_codigo),
        ).fetchone()["total"]

        numero_tentativa = int(total_anterior) + 1
        pontos_por_tentativa = {1: 10, 2: 8, 3: 6, 4: 4, 5: 2}
        pontos = pontos_por_tentativa.get(numero_tentativa, 0) if correta else 0
        dica_nivel = 0
        resposta_revelada = 0

        if not correta:
            if numero_tentativa == 2:
                dica_nivel = 1
            elif numero_tentativa == 3:
                dica_nivel = 2
            elif numero_tentativa == 4:
                dica_nivel = 3
            elif numero_tentativa >= 5:
                dica_nivel = 3
                resposta_revelada = 1

        conexao.execute(
            """
            INSERT INTO tentativas_leitura (
                sessao_id,
                pergunta_codigo,
                numero_tentativa,
                resposta,
                correta,
                dica_nivel,
                resposta_revelada,
                pontos
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sessao_id,
                pergunta_codigo,
                numero_tentativa,
                resposta,
                int(correta),
                dica_nivel,
                resposta_revelada,
                pontos,
            ),
        )

        fila.pop(0)
        if not correta and numero_tentativa < 5:
            fila.append(pergunta_codigo)

        perguntas_concluidas = len(fila) == 0
        nova_fase = "resumo" if perguntas_concluidas else "perguntas"

        conexao.execute(
            """
            UPDATE sessoes_leitura
            SET fila_json = ?,
                fase = ?,
                pontos_perguntas = pontos_perguntas + ?,
                acertos_perguntas = acertos_perguntas + ?,
                atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                json.dumps(fila),
                nova_fase,
                pontos,
                int(correta),
                sessao_id,
            ),
        )

        return {
            "numero_tentativa": numero_tentativa,
            "correta": bool(correta),
            "dica_nivel": dica_nivel,
            "resposta_revelada": bool(resposta_revelada),
            "pontos": pontos,
            "perguntas_concluidas": perguntas_concluidas,
        }


def registrar_versao_resumo(
    caminho_banco: str,
    sessao_id: int,
    resumo: str,
    avaliacao: dict[str, Any],
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        sessao = conexao.execute(
            "SELECT id, fase FROM sessoes_leitura WHERE id = ?",
            (sessao_id,),
        ).fetchone()

        if not sessao or sessao["fase"] not in {"resumo", "concluida"}:
            raise ValueError("A etapa do resumo ainda não está disponível.")

        numero_versao = int(
            conexao.execute(
                """
                SELECT COUNT(*) AS total
                FROM versoes_resumo
                WHERE sessao_id = ?
                """,
                (sessao_id,),
            ).fetchone()["total"]
        ) + 1

        conexao.execute(
            """
            INSERT INTO versoes_resumo (
                sessao_id,
                numero_versao,
                resumo,
                total_palavras,
                pontuacao,
                status,
                criterios_json,
                retorno_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sessao_id,
                numero_versao,
                resumo,
                int(avaliacao["total_palavras"]),
                int(avaliacao["pontuacao"]),
                avaliacao["status"],
                json.dumps(avaliacao["criterios"], ensure_ascii=False),
                json.dumps(
                    {
                        "mensagem": avaliacao["mensagem"],
                        "pontos_fortes": avaliacao["pontos_fortes"],
                        "melhorar": avaliacao["melhorar"],
                    },
                    ensure_ascii=False,
                ),
            ),
        )

        if avaliacao["status"] == "concluido":
            conexao.execute(
                """
                UPDATE sessoes_leitura
                SET fase = 'concluida',
                    atualizado_em = CURRENT_TIMESTAMP,
                    concluida_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (sessao_id,),
            )

    return {
        "numero_versao": numero_versao,
        **avaliacao,
    }


def obter_resultado_sessao_leitura(
    caminho_banco: str,
    sessao_id: int,
) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        sessao = conexao.execute(
            "SELECT * FROM sessoes_leitura WHERE id = ?",
            (sessao_id,),
        ).fetchone()

        if not sessao:
            raise ValueError("Sessão de leitura não encontrada.")

        tentativas = conexao.execute(
            """
            SELECT
                pergunta_codigo,
                MAX(numero_tentativa) AS tentativas,
                MAX(correta) AS acertou,
                MAX(resposta_revelada) AS resposta_revelada,
                SUM(pontos) AS pontos
            FROM tentativas_leitura
            WHERE sessao_id = ?
            GROUP BY pergunta_codigo
            ORDER BY pergunta_codigo
            """,
            (sessao_id,),
        ).fetchall()

        versao = conexao.execute(
            """
            SELECT *
            FROM versoes_resumo
            WHERE sessao_id = ?
            ORDER BY numero_versao DESC
            LIMIT 1
            """,
            (sessao_id,),
        ).fetchone()

        detalhes = []
        for tentativa in tentativas:
            ultima = conexao.execute(
                """
                SELECT resposta
                FROM tentativas_leitura
                WHERE sessao_id = ? AND pergunta_codigo = ?
                ORDER BY numero_tentativa DESC
                LIMIT 1
                """,
                (sessao_id, tentativa["pergunta_codigo"]),
            ).fetchone()
            detalhes.append(
                {
                    "id": tentativa["pergunta_codigo"],
                    "resposta": ultima["resposta"] if ultima else "",
                    "acertou": bool(tentativa["acertou"]),
                    "tentativas": int(tentativa["tentativas"]),
                    "resposta_revelada": bool(tentativa["resposta_revelada"]),
                    "pontos": int(tentativa["pontos"] or 0),
                }
            )

        pontuacao_resumo = int(versao["pontuacao"]) if versao else 0
        resumo = versao["resumo"] if versao else ""
        pontos_resumo = pontuacao_resumo * 7

        return {
            "sessao_id": int(sessao["id"]),
            "aluno_id": int(sessao["aluno_id"]),
            "data_atividade": sessao["data_atividade"],
            "titulo": sessao["titulo"],
            "acertos": sum(1 for item in detalhes if item["acertou"]),
            "total": int(sessao["total_perguntas"]),
            "pontos": int(sessao["pontos_perguntas"]) + pontos_resumo,
            "pontos_perguntas": int(sessao["pontos_perguntas"]),
            "pontos_resumo": pontos_resumo,
            "pontuacao_resumo": pontuacao_resumo,
            "resumo": resumo,
            "resumo_valido": pontuacao_resumo >= 7,
            "detalhes": detalhes,
        }


def buscar_usuario_por_id(
    caminho_banco: str,
    usuario_id: int,
) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT id, nome, identificador, senha_hash, perfil, ativo
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()
    return dict(registro) if registro else None


def obter_reset_missao_dia(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str,
) -> dict[str, Any] | None:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT id, motivo, criado_em
            FROM resets_missao_diaria
            WHERE aluno_id = ? AND data_atividade = ?
            """,
            (aluno_id, data_atividade),
        ).fetchone()
    return dict(registro) if registro else None


def refazer_missao_do_dia(
    caminho_banco: str,
    responsavel_usuario_id: int,
    aluno_id: int,
    data_atividade: str,
    motivo: str = "",
) -> dict[str, Any]:
    motivo = (motivo or "").strip()

    with conectar(caminho_banco) as conexao:
        vinculo = conexao.execute(
            """
            SELECT r.id AS responsavel_id, a.nome_exibicao
            FROM responsaveis r
            INNER JOIN responsavel_aluno ra ON ra.responsavel_id = r.id
            INNER JOIN alunos a ON a.id = ra.aluno_id
            WHERE r.usuario_id = ?
              AND a.id = ?
              AND r.ativo = 1
              AND a.ativo = 1
            """,
            (responsavel_usuario_id, aluno_id),
        ).fetchone()
        if not vinculo:
            raise ValueError("O aluno não pertence a este responsável.")

        reset_existente = conexao.execute(
            """
            SELECT id
            FROM resets_missao_diaria
            WHERE aluno_id = ? AND data_atividade = ?
            """,
            (aluno_id, data_atividade),
        ).fetchone()
        if reset_existente:
            raise ValueError("A missão de hoje já foi reiniciada uma vez.")

        atividades = [dict(row) for row in conexao.execute(
            "SELECT * FROM atividades_diarias WHERE aluno_id = ? AND data_atividade = ?",
            (aluno_id, data_atividade),
        ).fetchall()]
        atividade_ids = [int(item["id"]) for item in atividades]

        respostas = []
        resumos = []
        if atividade_ids:
            marcas = ",".join("?" for _ in atividade_ids)
            respostas = [dict(row) for row in conexao.execute(
                f"SELECT * FROM respostas_atividades WHERE atividade_id IN ({marcas})",
                atividade_ids,
            ).fetchall()]
            resumos = [dict(row) for row in conexao.execute(
                f"SELECT * FROM resumos_leitura WHERE atividade_id IN ({marcas})",
                atividade_ids,
            ).fetchall()]

        sessoes_adaptativas = [dict(row) for row in conexao.execute(
            "SELECT * FROM sessoes_adaptativas WHERE aluno_id = ? AND data_atividade = ?",
            (aluno_id, data_atividade),
        ).fetchall()]
        sessoes_adaptativas_ids = [int(item["id"]) for item in sessoes_adaptativas]
        tentativas_adaptativas = []
        if sessoes_adaptativas_ids:
            marcas = ",".join("?" for _ in sessoes_adaptativas_ids)
            tentativas_adaptativas = [dict(row) for row in conexao.execute(
                f"SELECT * FROM tentativas_adaptativas WHERE sessao_id IN ({marcas})",
                sessoes_adaptativas_ids,
            ).fetchall()]

        sessoes_leitura = [dict(row) for row in conexao.execute(
            "SELECT * FROM sessoes_leitura WHERE aluno_id = ? AND data_atividade = ?",
            (aluno_id, data_atividade),
        ).fetchall()]
        sessoes_leitura_ids = [int(item["id"]) for item in sessoes_leitura]
        tentativas_leitura = []
        versoes_resumo = []
        if sessoes_leitura_ids:
            marcas = ",".join("?" for _ in sessoes_leitura_ids)
            tentativas_leitura = [dict(row) for row in conexao.execute(
                f"SELECT * FROM tentativas_leitura WHERE sessao_id IN ({marcas})",
                sessoes_leitura_ids,
            ).fetchall()]
            versoes_resumo = [dict(row) for row in conexao.execute(
                f"SELECT * FROM versoes_resumo WHERE sessao_id IN ({marcas})",
                sessoes_leitura_ids,
            ).fetchall()]

        historico = {
            "aluno_id": aluno_id,
            "aluno_nome": vinculo["nome_exibicao"],
            "data_atividade": data_atividade,
            "atividades_diarias": atividades,
            "respostas_atividades": respostas,
            "resumos_leitura": resumos,
            "sessoes_adaptativas": sessoes_adaptativas,
            "tentativas_adaptativas": tentativas_adaptativas,
            "sessoes_leitura": sessoes_leitura,
            "tentativas_leitura": tentativas_leitura,
            "versoes_resumo": versoes_resumo,
        }

        conexao.execute(
            """
            INSERT INTO resets_missao_diaria (
                responsavel_usuario_id,
                aluno_id,
                data_atividade,
                motivo,
                historico_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                responsavel_usuario_id,
                aluno_id,
                data_atividade,
                motivo or None,
                json.dumps(historico, ensure_ascii=False),
            ),
        )

        if atividade_ids:
            marcas = ",".join("?" for _ in atividade_ids)
            conexao.execute(
                f"DELETE FROM respostas_atividades WHERE atividade_id IN ({marcas})",
                atividade_ids,
            )
            conexao.execute(
                f"DELETE FROM resumos_leitura WHERE atividade_id IN ({marcas})",
                atividade_ids,
            )

        if sessoes_adaptativas_ids:
            marcas = ",".join("?" for _ in sessoes_adaptativas_ids)
            conexao.execute(
                f"DELETE FROM tentativas_adaptativas WHERE sessao_id IN ({marcas})",
                sessoes_adaptativas_ids,
            )

        if sessoes_leitura_ids:
            marcas = ",".join("?" for _ in sessoes_leitura_ids)
            conexao.execute(
                f"DELETE FROM tentativas_leitura WHERE sessao_id IN ({marcas})",
                sessoes_leitura_ids,
            )
            conexao.execute(
                f"DELETE FROM versoes_resumo WHERE sessao_id IN ({marcas})",
                sessoes_leitura_ids,
            )

        conexao.execute(
            "DELETE FROM sessoes_adaptativas WHERE aluno_id = ? AND data_atividade = ?",
            (aluno_id, data_atividade),
        )
        conexao.execute(
            "DELETE FROM sessoes_leitura WHERE aluno_id = ? AND data_atividade = ?",
            (aluno_id, data_atividade),
        )
        conexao.execute(
            "DELETE FROM atividades_diarias WHERE aluno_id = ? AND data_atividade = ?",
            (aluno_id, data_atividade),
        )

    return {
        "aluno_id": aluno_id,
        "data_atividade": data_atividade,
        "historico_preservado": True,
    }




def criar_token_recuperacao_acesso(
    caminho_banco: str,
    email_responsavel: str,
    validade_minutos: int = 30,
) -> dict[str, Any] | None:
    email = (email_responsavel or "").strip().lower()
    agora = datetime.now(timezone.utc)
    expira_em = agora + timedelta(minutes=max(5, validade_minutos))

    with conectar(caminho_banco) as conexao:
        responsavel = conexao.execute(
            """
            SELECT id, nome_completo, email
            FROM responsaveis
            WHERE lower(email) = ?
              AND ativo = 1
            """,
            (email,),
        ).fetchone()
        if not responsavel:
            return None

        conexao.execute(
            """
            UPDATE tokens_recuperacao_acesso
            SET usado_em = ?
            WHERE responsavel_id = ?
              AND usado_em IS NULL
            """,
            (agora.isoformat(), responsavel["id"]),
        )

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        conexao.execute(
            """
            INSERT INTO tokens_recuperacao_acesso (
                responsavel_id,
                token_hash,
                expira_em
            ) VALUES (?, ?, ?)
            """,
            (responsavel["id"], token_hash, expira_em.isoformat()),
        )

    return {
        "token": token,
        "nome": responsavel["nome_completo"],
        "email": responsavel["email"],
    }


def obter_recuperacao_por_token(
    caminho_banco: str,
    token: str,
) -> dict[str, Any] | None:
    token_hash = hashlib.sha256((token or "").encode("utf-8")).hexdigest()
    agora = datetime.now(timezone.utc)

    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            """
            SELECT
                t.id AS token_id,
                t.expira_em,
                t.usado_em,
                r.id AS responsavel_id,
                r.usuario_id AS responsavel_usuario_id,
                r.nome_completo,
                r.email
            FROM tokens_recuperacao_acesso t
            INNER JOIN responsaveis r ON r.id = t.responsavel_id
            WHERE t.token_hash = ?
              AND r.ativo = 1
            """,
            (token_hash,),
        ).fetchone()
        if not registro or registro["usado_em"]:
            return None

        expira_em = datetime.fromisoformat(registro["expira_em"])
        if expira_em.tzinfo is None:
            expira_em = expira_em.replace(tzinfo=timezone.utc)
        if expira_em <= agora:
            return None

        alunos = conexao.execute(
            """
            SELECT a.id, a.usuario_id, a.nome_exibicao, a.nome_completo
            FROM responsavel_aluno ra
            INNER JOIN alunos a ON a.id = ra.aluno_id
            WHERE ra.responsavel_id = ?
              AND a.ativo = 1
            ORDER BY ra.principal DESC, a.nome_exibicao
            """,
            (registro["responsavel_id"],),
        ).fetchall()

    resultado = dict(registro)
    resultado["alunos"] = [dict(aluno) for aluno in alunos]
    return resultado


def redefinir_senha_responsavel_por_token(
    caminho_banco: str,
    token: str,
    nova_senha: str,
) -> bool:
    recuperacao = obter_recuperacao_por_token(caminho_banco, token)
    if not recuperacao:
        return False

    agora = datetime.now(timezone.utc).isoformat()
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            """
            UPDATE usuarios
            SET senha_hash = ?, atualizado_em = ?
            WHERE id = ? AND perfil = 'responsavel' AND ativo = 1
            """,
            (generate_password_hash(nova_senha), agora, recuperacao["responsavel_usuario_id"]),
        )
        conexao.execute(
            "UPDATE tokens_recuperacao_acesso SET usado_em = ? WHERE id = ?",
            (agora, recuperacao["token_id"]),
        )
    return True


def redefinir_pin_aluno_por_token(
    caminho_banco: str,
    token: str,
    aluno_id: int,
    novo_pin: str,
) -> bool:
    recuperacao = obter_recuperacao_por_token(caminho_banco, token)
    if not recuperacao:
        return False

    aluno = next(
        (item for item in recuperacao["alunos"] if int(item["id"]) == int(aluno_id)),
        None,
    )
    if not aluno:
        return False

    agora = datetime.now(timezone.utc).isoformat()
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            """
            UPDATE usuarios
            SET senha_hash = ?, atualizado_em = ?
            WHERE id = ? AND perfil = 'aluno' AND ativo = 1
            """,
            (generate_password_hash(novo_pin), agora, aluno["usuario_id"]),
        )
        conexao.execute(
            "UPDATE tokens_recuperacao_acesso SET usado_em = ? WHERE id = ?",
            (agora, recuperacao["token_id"]),
        )
    return True
