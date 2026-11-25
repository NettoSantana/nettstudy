# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\acesso_aluno.py
# Data e hora do último recode: 25/11/2026 19:11 -0300
# Motivo da alteração: ativar e revogar dispositivos de alunos por link.

from hashlib import sha256
from secrets import token_urlsafe
from time import time

from database import conectar


def inicializar_acesso(caminho):
    with conectar(caminho) as banco:
        banco.executescript("""
            CREATE TABLE IF NOT EXISTS ativacoes_aluno (
                hash TEXT PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                expira INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dispositivos_aluno (
                hash TEXT PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                expira INTEGER NOT NULL
            );
        """)


def _hash(token):
    return sha256(token.encode()).hexdigest()


def emitir_link(caminho, usuario_id):
    token = token_urlsafe(32)
    with conectar(caminho) as banco:
        banco.execute("DELETE FROM ativacoes_aluno WHERE usuario_id=? OR expira<=?", (usuario_id, int(time())))
        banco.execute("INSERT INTO ativacoes_aluno VALUES (?, ?, ?)", (_hash(token), usuario_id, int(time()) + 1800))
    return token


def consumir_link(caminho, token):
    if len(token) != 43:
        return None
    dispositivo = token_urlsafe(32)
    agora = int(time())
    with conectar(caminho) as banco:
        ativacao = banco.execute(
            "DELETE FROM ativacoes_aluno WHERE hash=? AND expira>? RETURNING usuario_id",
            (_hash(token), agora),
        ).fetchone()
        if ativacao is None:
            return None
        usuario_id = ativacao["usuario_id"]
        banco.execute("DELETE FROM dispositivos_aluno WHERE expira<=?", (agora,))
        banco.execute(
            "INSERT INTO dispositivos_aluno VALUES (?, ?, ?)",
            (_hash(dispositivo), usuario_id, agora + 90 * 86400),
        )
    return usuario_id, dispositivo


def usuario_do_dispositivo(caminho, dispositivo):
    if len(dispositivo) != 43:
        return None
    with conectar(caminho) as banco:
        registro = banco.execute(
            """SELECT u.id, u.nome FROM dispositivos_aluno d JOIN usuarios u ON u.id=d.usuario_id
               WHERE d.hash=? AND d.expira>? AND u.ativo=1 AND u.perfil='aluno'""",
            (_hash(dispositivo), int(time())),
        ).fetchone()
    return dict(registro) if registro else None


def revogar_acessos(caminho, usuario_id):
    with conectar(caminho) as banco:
        banco.execute("DELETE FROM ativacoes_aluno WHERE usuario_id=?", (usuario_id,))
        banco.execute("DELETE FROM dispositivos_aluno WHERE usuario_id=?", (usuario_id,))
