# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\database.py
# Data e hora do último recode: 30/07/2026 15:10 -03:00
# Motivo da alteração: registrar atividades diárias, respostas, pontos e resumos de leitura.

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
