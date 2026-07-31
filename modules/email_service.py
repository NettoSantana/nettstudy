# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\email_service.py
# Data e hora do último recode: 31/07/2026 06:32 -03:00
# Motivo da alteração: incluir envio de avisos e relatórios automáticos pelo Resend.

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def enviar_email_recuperacao(
    api_key: str,
    remetente: str,
    destinatario: str,
    nome_responsavel: str,
    link_recuperacao: str,
) -> None:
    if not api_key:
        raise RuntimeError("RESEND_API_KEY não configurada.")

    nome = (nome_responsavel or "Responsável").strip()
    assunto = "Recupere seu acesso ao NettStudy"
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#18203a">
      <h1 style="color:#4e5ce6">NettStudy</h1>
      <p>Olá, {nome}.</p>
      <p>Recebemos uma solicitação para recuperar o acesso da sua família ao NettStudy.</p>
      <p>Use o botão abaixo para redefinir sua senha de responsável ou o PIN de um aluno.</p>
      <p style="margin:28px 0">
        <a href="{link_recuperacao}" style="background:#4e5ce6;color:#fff;padding:14px 20px;border-radius:12px;text-decoration:none;font-weight:bold">
          Recuperar acesso
        </a>
      </p>
      <p>Este link é válido por 30 minutos e funciona apenas uma vez.</p>
      <p>Se você não solicitou a recuperação, ignore esta mensagem.</p>
    </div>
    """

    corpo = json.dumps({
        "from": remetente,
        "to": [destinatario],
        "subject": assunto,
        "html": html,
    }).encode("utf-8")

    requisicao = Request(
        "https://api.resend.com/emails",
        data=corpo,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "NettStudy/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(requisicao, timeout=15) as resposta:
            if resposta.status < 200 or resposta.status >= 300:
                raise RuntimeError(f"Resend respondeu com status {resposta.status}.")
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Falha no envio pelo Resend: {detalhe}") from erro
    except URLError as erro:
        raise RuntimeError("Não foi possível conectar ao serviço de e-mail.") from erro


def enviar_email_validacao(
    api_key: str,
    remetente: str,
    destinatario: str,
    nome_responsavel: str,
    link_validacao: str,
) -> None:
    if not api_key:
        raise RuntimeError("RESEND_API_KEY não configurada.")

    nome = (nome_responsavel or "Responsável").strip()
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#18203a">
      <h1 style="color:#4e5ce6">NettStudy</h1>
      <p>Olá, {nome}.</p>
      <p>Confirme seu e-mail para proteger a conta da sua família no NettStudy.</p>
      <p style="margin:28px 0">
        <a href="{link_validacao}" style="background:#4e5ce6;color:#fff;padding:14px 20px;border-radius:12px;text-decoration:none;font-weight:bold">
          Validar meu e-mail
        </a>
      </p>
      <p>Este link é válido por 24 horas e funciona apenas uma vez.</p>
      <p>Você pode continuar usando o NettStudy normalmente enquanto isso.</p>
      <p>Se você não criou esta conta, ignore esta mensagem.</p>
    </div>
    """
    corpo = json.dumps({
        "from": remetente,
        "to": [destinatario],
        "subject": "Valide seu e-mail no NettStudy",
        "html": html,
    }).encode("utf-8")
    requisicao = Request(
        "https://api.resend.com/emails", data=corpo,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "NettStudy/1.0"},
        method="POST",
    )
    try:
        with urlopen(requisicao, timeout=15) as resposta:
            if resposta.status < 200 or resposta.status >= 300:
                raise RuntimeError(f"Resend respondeu com status {resposta.status}.")
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Falha no envio pelo Resend: {detalhe}") from erro
    except URLError as erro:
        raise RuntimeError("Não foi possível conectar ao serviço de e-mail.") from erro



def enviar_email_notificacao(
    api_key: str,
    remetente: str,
    destinatario: str,
    assunto: str,
    html: str,
) -> None:
    """Envia uma notificação transacional do NettStudy pelo Resend."""
    if not api_key:
        raise RuntimeError("RESEND_API_KEY não configurada.")

    corpo = json.dumps({
        "from": remetente,
        "to": [destinatario],
        "subject": assunto,
        "html": html,
    }).encode("utf-8")
    requisicao = Request(
        "https://api.resend.com/emails",
        data=corpo,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "NettStudy/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(requisicao, timeout=15) as resposta:
            if resposta.status < 200 or resposta.status >= 300:
                raise RuntimeError(f"Resend respondeu com status {resposta.status}.")
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Falha no envio pelo Resend: {detalhe}") from erro
    except URLError as erro:
        raise RuntimeError("Não foi possível conectar ao serviço de e-mail.") from erro
