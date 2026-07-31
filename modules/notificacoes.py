# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\notificacoes.py
# Data e hora do último recode: 31/07/2026 08:07 -03:00
# Motivo da alteração: registrar falhas do agendador e executar verificação imediata das notificações.

import html
import sqlite3
import threading
from datetime import date, datetime, timedelta
from pathlib import Path
from time import sleep
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from modules.email_service import enviar_email_notificacao


notificacoes_bp = Blueprint("notificacoes", __name__)
_thread_iniciada = False
_thread_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS configuracoes_notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    dias_semana TEXT NOT NULL DEFAULT '0,1,2,3,4',
    horario_limite TEXT NOT NULL DEFAULT '19:00',
    avisar_atraso INTEGER NOT NULL DEFAULT 1 CHECK (avisar_atraso IN (0, 1)),
    avisar_conclusao INTEGER NOT NULL DEFAULT 1 CHECK (avisar_conclusao IN (0, 1)),
    enviar_relatorio_semanal INTEGER NOT NULL DEFAULT 1 CHECK (enviar_relatorio_semanal IN (0, 1)),
    dia_relatorio INTEGER NOT NULL DEFAULT 6 CHECK (dia_relatorio BETWEEN 0 AND 6),
    horario_relatorio TEXT NOT NULL DEFAULT '18:00',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    UNIQUE (responsavel_id, aluno_id),
    FOREIGN KEY (responsavel_id) REFERENCES responsaveis(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notificacoes_enviadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    configuracao_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('atraso', 'conclusao', 'relatorio_semanal')),
    referencia TEXT NOT NULL,
    destinatario TEXT NOT NULL,
    enviado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (configuracao_id, tipo, referencia),
    FOREIGN KEY (configuracao_id) REFERENCES configuracoes_notificacoes(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_config_notificacoes_aluno
    ON configuracoes_notificacoes (aluno_id);
CREATE INDEX IF NOT EXISTS idx_notificacoes_referencia
    ON notificacoes_enviadas (tipo, referencia);
"""

DIAS = (
    (0, "Segunda-feira"),
    (1, "Terça-feira"),
    (2, "Quarta-feira"),
    (3, "Quinta-feira"),
    (4, "Sexta-feira"),
    (5, "Sábado"),
    (6, "Domingo"),
)


def _conectar(caminho_banco: str) -> sqlite3.Connection:
    Path(caminho_banco).parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho_banco, timeout=20)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_notificacoes(caminho_banco: str) -> None:
    with _conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA)


def _responsavel_logado(caminho_banco: str) -> dict[str, Any] | None:
    usuario_id = session.get("usuario_id")
    if not usuario_id or session.get("perfil") != "responsavel":
        return None
    with _conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            "SELECT id, nome_completo, email FROM responsaveis WHERE usuario_id = ? AND ativo = 1",
            (int(usuario_id),),
        ).fetchone()
    return dict(registro) if registro else None


def _alunos_do_responsavel(caminho_banco: str, responsavel_id: int) -> list[dict[str, Any]]:
    with _conectar(caminho_banco) as conexao:
        registros = conexao.execute(
            """
            SELECT a.id, a.nome_exibicao, a.ano_escolar
            FROM responsavel_aluno ra
            INNER JOIN alunos a ON a.id = ra.aluno_id
            WHERE ra.responsavel_id = ? AND a.ativo = 1
            ORDER BY ra.principal DESC, a.nome_exibicao
            """,
            (responsavel_id,),
        ).fetchall()
    return [dict(item) for item in registros]


def _configuracao(caminho_banco: str, responsavel_id: int, aluno_id: int) -> dict[str, Any]:
    with _conectar(caminho_banco) as conexao:
        conexao.execute(
            """
            INSERT OR IGNORE INTO configuracoes_notificacoes (responsavel_id, aluno_id)
            VALUES (?, ?)
            """,
            (responsavel_id, aluno_id),
        )
        registro = conexao.execute(
            """
            SELECT * FROM configuracoes_notificacoes
            WHERE responsavel_id = ? AND aluno_id = ?
            """,
            (responsavel_id, aluno_id),
        ).fetchone()
    resultado = dict(registro)
    resultado["dias_selecionados"] = {int(valor) for valor in resultado["dias_semana"].split(",") if valor}
    return resultado


def _horario_valido(valor: str) -> bool:
    try:
        datetime.strptime(valor, "%H:%M")
        return True
    except ValueError:
        return False


@notificacoes_bp.route("/responsavel/notificacoes", methods=["GET", "POST"])
def configuracoes_notificacoes():
    caminho_banco = current_app.config["DATABASE_PATH"]
    responsavel = _responsavel_logado(caminho_banco)
    if not responsavel:
        flash("Faça login como responsável para continuar.", "aviso")
        return redirect(url_for("login"))

    alunos = _alunos_do_responsavel(caminho_banco, int(responsavel["id"]))
    if not alunos:
        flash("Cadastre um aluno antes de configurar notificações.", "aviso")
        return redirect(url_for("dashboard_responsavel"))

    aluno_id = request.args.get("aluno_id", type=int) or request.form.get("aluno_id", type=int)
    aluno_id = aluno_id or int(alunos[0]["id"])
    aluno = next((item for item in alunos if int(item["id"]) == int(aluno_id)), None)
    if not aluno:
        flash("Aluno não encontrado nesta família.", "erro")
        return redirect(url_for("notificacoes.configuracoes_notificacoes"))

    if request.method == "POST":
        dias = sorted({int(item) for item in request.form.getlist("dias_semana") if item.isdigit() and 0 <= int(item) <= 6})
        horario_limite = request.form.get("horario_limite", "19:00").strip()
        horario_relatorio = request.form.get("horario_relatorio", "18:00").strip()
        dia_relatorio = request.form.get("dia_relatorio", type=int)
        if not dias:
            flash("Selecione pelo menos um dia de atividade.", "erro")
        elif not _horario_valido(horario_limite) or not _horario_valido(horario_relatorio):
            flash("Informe horários válidos.", "erro")
        elif dia_relatorio is None or not 0 <= dia_relatorio <= 6:
            flash("Selecione o dia do relatório semanal.", "erro")
        else:
            with _conectar(caminho_banco) as conexao:
                conexao.execute(
                    """
                    INSERT INTO configuracoes_notificacoes (
                        responsavel_id, aluno_id, ativo, dias_semana, horario_limite,
                        avisar_atraso, avisar_conclusao, enviar_relatorio_semanal,
                        dia_relatorio, horario_relatorio, atualizado_em
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(responsavel_id, aluno_id) DO UPDATE SET
                        ativo = excluded.ativo,
                        dias_semana = excluded.dias_semana,
                        horario_limite = excluded.horario_limite,
                        avisar_atraso = excluded.avisar_atraso,
                        avisar_conclusao = excluded.avisar_conclusao,
                        enviar_relatorio_semanal = excluded.enviar_relatorio_semanal,
                        dia_relatorio = excluded.dia_relatorio,
                        horario_relatorio = excluded.horario_relatorio,
                        atualizado_em = CURRENT_TIMESTAMP
                    """,
                    (
                        int(responsavel["id"]), int(aluno_id),
                        int("ativo" in request.form), ",".join(map(str, dias)), horario_limite,
                        int("avisar_atraso" in request.form), int("avisar_conclusao" in request.form),
                        int("enviar_relatorio_semanal" in request.form), dia_relatorio, horario_relatorio,
                    ),
                )
            flash(f"Notificações de {aluno['nome_exibicao']} atualizadas.", "sucesso")
            return redirect(url_for("notificacoes.configuracoes_notificacoes", aluno_id=aluno_id))

    configuracao = _configuracao(caminho_banco, int(responsavel["id"]), int(aluno_id))
    return render_template(
        "configuracoes_notificacoes.html",
        responsavel=responsavel,
        alunos=alunos,
        aluno=aluno,
        configuracao=configuracao,
        dias=DIAS,
    )


def _ja_enviado(conexao: sqlite3.Connection, configuracao_id: int, tipo: str, referencia: str) -> bool:
    return conexao.execute(
        "SELECT 1 FROM notificacoes_enviadas WHERE configuracao_id = ? AND tipo = ? AND referencia = ?",
        (configuracao_id, tipo, referencia),
    ).fetchone() is not None


def _registrar_envio(conexao: sqlite3.Connection, configuracao: sqlite3.Row, tipo: str, referencia: str) -> None:
    conexao.execute(
        """
        INSERT OR IGNORE INTO notificacoes_enviadas
            (configuracao_id, aluno_id, tipo, referencia, destinatario)
        VALUES (?, ?, ?, ?, ?)
        """,
        (configuracao["id"], configuracao["aluno_id"], tipo, referencia, configuracao["email"]),
    )


def _total_concluidas(conexao: sqlite3.Connection, aluno_id: int, data_iso: str) -> int:
    return int(conexao.execute(
        """
        SELECT COUNT(*) AS total FROM atividades_diarias
        WHERE aluno_id = ? AND data_atividade = ? AND status = 'concluida'
        """,
        (aluno_id, data_iso),
    ).fetchone()["total"])


def _base_email(titulo: str, conteudo: str) -> str:
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:620px;margin:auto;color:#18203a;line-height:1.6">
      <h1 style="color:#4e5ce6;margin-bottom:6px">NettStudy</h1>
      <h2 style="margin-top:0">{titulo}</h2>
      {conteudo}
      <p style="margin-top:28px;color:#68718c;font-size:13px">Este aviso foi configurado no painel do responsável.</p>
    </div>
    """


def _enviar_atraso(config: dict[str, Any]) -> None:
    nome = html.escape(config["nome_exibicao"])
    conteudo = f"<p>A missão de hoje de <strong>{nome}</strong> ainda não foi concluída até o horário configurado.</p><p>Português, Matemática e Leitura formam a missão completa do dia.</p>"
    enviar_email_notificacao(config["api_key"], config["remetente"], config["email"], f"Atividade pendente de {nome}", _base_email("Atividade ainda pendente", conteudo))


def _enviar_conclusao(config: dict[str, Any]) -> None:
    nome = html.escape(config["nome_exibicao"])
    conteudo = f"<p><strong>{nome}</strong> concluiu 100% da missão de hoje.</p><p>As etapas de Português, Matemática e Leitura foram finalizadas.</p>"
    enviar_email_notificacao(config["api_key"], config["remetente"], config["email"], f"{nome} concluiu a missão de hoje", _base_email("Missão concluída", conteudo))


def _dados_semanais(conexao: sqlite3.Connection, config: dict[str, Any], hoje: date) -> dict[str, Any]:
    inicio = hoje - timedelta(days=6)
    linhas = conexao.execute(
        """
        SELECT data_atividade,
               COUNT(*) AS materias,
               COALESCE(SUM(pontos), 0) AS pontos,
               COALESCE(SUM(acertos), 0) AS acertos,
               COALESCE(SUM(total_questoes), 0) AS questoes
        FROM atividades_diarias
        WHERE aluno_id = ? AND data_atividade BETWEEN ? AND ? AND status = 'concluida'
        GROUP BY data_atividade
        """,
        (config["aluno_id"], inicio.isoformat(), hoje.isoformat()),
    ).fetchall()
    por_data = {item["data_atividade"]: dict(item) for item in linhas}
    dias_programados = {int(valor) for valor in config["dias_semana"].split(",") if valor}
    previstos = 0
    completos = 0
    pontos = 0
    acertos = 0
    questoes = 0
    for deslocamento in range(7):
        dia = inicio + timedelta(days=deslocamento)
        if dia.weekday() in dias_programados:
            previstos += 1
            registro = por_data.get(dia.isoformat())
            if registro and int(registro["materias"]) >= 3:
                completos += 1
        registro = por_data.get(dia.isoformat())
        if registro:
            pontos += int(registro["pontos"])
            acertos += int(registro["acertos"])
            questoes += int(registro["questoes"])
    return {
        "inicio": inicio.strftime("%d/%m"), "fim": hoje.strftime("%d/%m"),
        "previstos": previstos, "completos": completos,
        "frequencia": round((completos / previstos) * 100) if previstos else 0,
        "pontos": pontos,
        "aproveitamento": round((acertos / questoes) * 100) if questoes else 0,
    }


def _enviar_relatorio(config: dict[str, Any], dados: dict[str, Any]) -> None:
    nome = html.escape(config["nome_exibicao"])
    conteudo = f"""
      <p>Resumo de <strong>{nome}</strong> entre {dados['inicio']} e {dados['fim']}:</p>
      <div style="display:grid;gap:10px">
        <div style="padding:14px;background:#f3f5ff;border-radius:12px"><strong>Frequência:</strong> {dados['completos']} de {dados['previstos']} dias programados ({dados['frequencia']}%)</div>
        <div style="padding:14px;background:#f3f5ff;border-radius:12px"><strong>Pontos conquistados:</strong> {dados['pontos']}</div>
        <div style="padding:14px;background:#f3f5ff;border-radius:12px"><strong>Aproveitamento nas questões:</strong> {dados['aproveitamento']}%</div>
      </div>
    """
    enviar_email_notificacao(config["api_key"], config["remetente"], config["email"], f"Relatório semanal de {nome}", _base_email("Relatório semanal", conteudo))


def verificar_notificacoes(config_app: dict[str, Any], logger=None) -> None:
    try:
        fuso = ZoneInfo(config_app["NOTIFICACOES_FUSO"])
    except ZoneInfoNotFoundError:
        fuso = ZoneInfo("UTC")
    agora = datetime.now(fuso)
    data_iso = agora.date().isoformat()
    hora_atual = agora.strftime("%H:%M")
    semana = f"{agora.isocalendar().year}-W{agora.isocalendar().week:02d}"

    with _conectar(config_app["DATABASE_PATH"]) as conexao:
        configuracoes = conexao.execute(
            """
            SELECT c.*, r.email, r.nome_completo, a.nome_exibicao
            FROM configuracoes_notificacoes c
            INNER JOIN responsaveis r ON r.id = c.responsavel_id
            INNER JOIN alunos a ON a.id = c.aluno_id
            WHERE c.ativo = 1 AND r.ativo = 1 AND a.ativo = 1
            """
        ).fetchall()

        if logger:
            logger.info(
                "Verificação de notificações iniciada: %s configuração(ões) ativa(s), data=%s, hora=%s, fuso=%s.",
                len(configuracoes),
                data_iso,
                hora_atual,
                str(fuso),
            )

        for registro in configuracoes:
            config = dict(registro)
            config["api_key"] = config_app["RESEND_API_KEY"]
            config["remetente"] = config_app["RESEND_FROM"]
            dias = {int(valor) for valor in config["dias_semana"].split(",") if valor}
            concluidas = _total_concluidas(conexao, int(config["aluno_id"]), data_iso)
            try:
                if config["avisar_conclusao"] and concluidas == 3 and not _ja_enviado(conexao, config["id"], "conclusao", data_iso):
                    _enviar_conclusao(config)
                    _registrar_envio(conexao, registro, "conclusao", data_iso)
                    if logger:
                        logger.info(
                            "Notificação de conclusão enviada para aluno_id=%s, destinatário=%s, referência=%s.",
                            config["aluno_id"],
                            config["email"],
                            data_iso,
                        )

                if config["avisar_atraso"] and agora.weekday() in dias and hora_atual >= config["horario_limite"] and concluidas < 3 and not _ja_enviado(conexao, config["id"], "atraso", data_iso):
                    _enviar_atraso(config)
                    _registrar_envio(conexao, registro, "atraso", data_iso)
                    if logger:
                        logger.info(
                            "Notificação de atraso enviada para aluno_id=%s, destinatário=%s, referência=%s.",
                            config["aluno_id"],
                            config["email"],
                            data_iso,
                        )

                if config["enviar_relatorio_semanal"] and agora.weekday() == int(config["dia_relatorio"]) and hora_atual >= config["horario_relatorio"] and not _ja_enviado(conexao, config["id"], "relatorio_semanal", semana):
                    _enviar_relatorio(config, _dados_semanais(conexao, config, agora.date()))
                    _registrar_envio(conexao, registro, "relatorio_semanal", semana)
                    if logger:
                        logger.info(
                            "Relatório semanal enviado para aluno_id=%s, destinatário=%s, referência=%s.",
                            config["aluno_id"],
                            config["email"],
                            semana,
                        )
            except RuntimeError as erro:
                if logger:
                    logger.exception(
                        "Falha ao enviar notificação para aluno_id=%s, destinatário=%s: %s",
                        config["aluno_id"],
                        config["email"],
                        erro,
                    )
                continue
            except Exception as erro:
                if logger:
                    logger.exception(
                        "Erro inesperado ao processar notificações do aluno_id=%s: %s",
                        config["aluno_id"],
                        erro,
                    )
                continue


def iniciar_agendador_notificacoes(app) -> None:
    global _thread_iniciada
    if not app.config.get("NOTIFICACOES_ATIVAS"):
        return
    with _thread_lock:
        if _thread_iniciada:
            return
        _thread_iniciada = True

    config_app = {
        "DATABASE_PATH": app.config["DATABASE_PATH"],
        "RESEND_API_KEY": app.config["RESEND_API_KEY"],
        "RESEND_FROM": app.config["RESEND_FROM"],
        "NOTIFICACOES_FUSO": app.config["NOTIFICACOES_FUSO"],
        "NOTIFICACOES_INTERVALO_SEGUNDOS": app.config["NOTIFICACOES_INTERVALO_SEGUNDOS"],
    }

    logger = app.logger

    def executar() -> None:
        logger.info(
            "Agendador de notificações iniciado: intervalo=%ss, fuso=%s, banco=%s.",
            config_app["NOTIFICACOES_INTERVALO_SEGUNDOS"],
            config_app["NOTIFICACOES_FUSO"],
            config_app["DATABASE_PATH"],
        )
        while True:
            try:
                verificar_notificacoes(config_app, logger=logger)
            except Exception as erro:
                logger.exception(
                    "Falha geral no ciclo do agendador de notificações: %s",
                    erro,
                )
            sleep(config_app["NOTIFICACOES_INTERVALO_SEGUNDOS"])

    threading.Thread(
        target=executar,
        name="nettstudy-notificacoes",
        daemon=True,
    ).start()
