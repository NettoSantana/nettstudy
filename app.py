# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\app.py
# Data e hora do último recode: 02/08/2026 18:02 -03:00
# Motivo da alteração: exigir consentimento parental de perfis novos e antigos antes de qualquer uso infantil.

import os
from datetime import date
from functools import wraps
from typing import Any, Callable

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from modules.email_service import enviar_email_recuperacao, enviar_email_validacao

from config import Config
from modules.avaliacao_resumo import avaliar_resumo
from modules.anamnese_pedagogica import (
    concluir as concluir_anamnese_estruturada,
    converter_para_anamnese_legada,
    inicializar_anamnese_pedagogica,
    montar_resumo as montar_resumo_anamnese,
    obter_estado as obter_estado_anamnese,
    opcoes_template as opcoes_anamnese_template,
    salvar_etapa as salvar_etapa_anamnese,
)
from modules.leitura import (
    obter_historia_do_dia,
    obter_historia_por_id,
    obter_pergunta as obter_pergunta_leitura,
    resposta_correta as resposta_correta_leitura,
)
from modules.notificacoes import (
    iniciar_agendador_notificacoes,
    inicializar_notificacoes,
    notificacoes_bp,
)
from modules.motor_pedagogico import (
    garantir_perfil_pedagogico,
    gerar_plano_missao,
    inicializar_motor_pedagogico,
    obter_perfil_pedagogico,
    registrar_desempenho,
    resumo_missao_personalizada,
    recalcular_perfil_por_anamnese,
    proxima_etapa_missao,
    obter_relatorio_pedagogico,
    simular_ciclo_diagnostico,
    historias_lidas_ciclo,
)
from modules.matematica import (
    QUESTOES as QUESTOES_MATEMATICA,
    enriquecer_resultado as enriquecer_resultado_matematica,
    obter_questao as obter_questao_matematica,
    resposta_correta as resposta_correta_matematica,
)
from modules.portugues import (
    QUESTOES as QUESTOES_PORTUGUES,
    TEXTO,
    enriquecer_resultado as enriquecer_resultado_portugues,
    obter_questao as obter_questao_portugues,
    resposta_correta as resposta_correta_portugues,
)

from database import (
    buscar_aluno_por_usuario,
    buscar_aluno_do_responsavel,
    buscar_anamnese_por_aluno,
    buscar_responsavel_por_usuario,
    buscar_usuario_por_login,
    buscar_usuario_por_id,
    cadastrar_responsavel,
    cadastrar_aluno_para_responsavel,
    aluno_possui_consentimento_parental_ativo,
    inicializar_banco,
    listar_alunos_do_responsavel,
    listar_alunos_sem_consentimento_parental,
    finalizar_sessao_adaptativa,
    obter_ou_criar_sessao_adaptativa,
    obter_resumo_diario,
    obter_reset_missao_dia,
    refazer_missao_do_dia,
    registrar_resultado_atividade,
    registrar_tentativa_adaptativa,
    obter_ou_criar_sessao_leitura,
    iniciar_perguntas_leitura,
    registrar_tentativa_leitura,
    registrar_versao_resumo,
    obter_resultado_sessao_leitura,
    salvar_anamnese,
    criar_token_recuperacao_acesso,
    obter_recuperacao_por_token,
    redefinir_senha_responsavel_por_token,
    redefinir_pin_aluno_por_token,
    criar_token_validacao_email,
    validar_email_por_token,
    aplicar_reset_pedagogico_unico,
    registrar_consentimento_parental_para_aluno_existente,
)


VERSAO_TERMO_CONSENTIMENTO_PARENTAL = "2026-08-02-v1"
ORIGEM_CONSENTIMENTO_PARENTAL = "formulario_novo_aluno"
ORIGEM_REGULARIZACAO_CONSENTIMENTO = "primeiro_login_conta_existente"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    inicializar_banco(app.config["DATABASE_PATH"])
    inicializar_motor_pedagogico(app.config["DATABASE_PATH"])
    inicializar_anamnese_pedagogica(app.config["DATABASE_PATH"])
    aplicar_reset_pedagogico_unico(app.config["DATABASE_PATH"])
    inicializar_notificacoes(app.config["DATABASE_PATH"])
    app.register_blueprint(notificacoes_bp)
    registrar_contexto(app)
    registrar_rotas(app)
    registrar_erros(app)
    iniciar_agendador_notificacoes(app)
    return app


def login_obrigatorio(perfil: str | None = None) -> Callable:
    def decorador(funcao: Callable) -> Callable:
        @wraps(funcao)
        def protegida(*args: Any, **kwargs: Any):
            if not session.get("usuario_id"):
                flash("Faça login para continuar.", "aviso")
                return redirect(url_for("login"))

            if perfil and session.get("perfil") != perfil:
                flash("Este acesso não pertence ao seu perfil.", "erro")
                return redirect(url_for("portal"))

            return funcao(*args, **kwargs)

        return protegida

    return decorador


def registrar_contexto(app: Flask) -> None:
    @app.context_processor
    def contexto_global() -> dict[str, Any]:
        return {
            "nome_produto": "NettStudy",
            "usuario_logado": session.get("nome"),
            "perfil_logado": session.get("perfil"),
        }


def registrar_rotas(app: Flask) -> None:
    @app.before_request
    def exigir_consentimento_parental_ativo():
        usuario_id = session.get("usuario_id")
        perfil = session.get("perfil")
        endpoint = request.endpoint or ""

        if not usuario_id or endpoint == "static" or endpoint.startswith("static"):
            return None

        if perfil == "aluno":
            if endpoint in {"sair", "health"}:
                return None
            if not aluno_possui_consentimento_parental_ativo(
                app.config["DATABASE_PATH"],
                int(usuario_id),
            ):
                session.clear()
                flash(
                    "O responsável precisa autorizar este perfil antes do acesso do aluno.",
                    "aviso",
                )
                if endpoint == "login":
                    return None
                return redirect(url_for("login"))
            return None

        rotas_permitidas = {
            "health",
            "login",
            "reenviar_validacao_email",
            "regularizar_consentimento_parental",
            "sair",
            "validar_email",
        }
        if perfil != "responsavel" or endpoint in rotas_permitidas:
            return None

        pendentes = listar_alunos_sem_consentimento_parental(
            app.config["DATABASE_PATH"],
            int(usuario_id),
        )
        if pendentes:
            flash(
                "Atualize o consentimento parental para continuar usando o NettStudy.",
                "aviso",
            )
            return redirect(url_for("regularizar_consentimento_parental"))

        return None

    @app.get("/")
    def inicio():
        return render_template("portal.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identificador = request.form.get("identificador", "").strip().lower()
            senha = request.form.get("senha", "")

            usuario = buscar_usuario_por_login(
                app.config["DATABASE_PATH"],
                identificador,
            )

            if not usuario or not check_password_hash(
                usuario["senha_hash"],
                senha,
            ):
                flash("Login ou senha inválidos.", "erro")
                return render_template(
                    "login.html",
                    identificador=identificador,
                ), 401

            session.clear()
            session.update(
                usuario_id=usuario["id"],
                nome=usuario["nome"],
                perfil=usuario["perfil"],
            )

            if usuario["perfil"] == "responsavel":
                pendentes = listar_alunos_sem_consentimento_parental(
                    app.config["DATABASE_PATH"],
                    int(usuario["id"]),
                )
                if pendentes:
                    flash(
                        "Antes de continuar, revise e confirme a autorização dos perfis infantis já cadastrados.",
                        "aviso",
                    )
                    return redirect(url_for("regularizar_consentimento_parental"))

            if usuario["perfil"] == "aluno" and not aluno_possui_consentimento_parental_ativo(
                app.config["DATABASE_PATH"],
                int(usuario["id"]),
            ):
                session.clear()
                flash(
                    "O responsável precisa autorizar este perfil antes do acesso do aluno.",
                    "aviso",
                )
                return redirect(url_for("login"))

            destino = (
                "dashboard_responsavel"
                if usuario["perfil"] == "responsavel"
                else "dashboard_aluno"
            )

            return redirect(url_for(destino))

        return render_template("login.html")

    @app.route("/recuperar-acesso", methods=["GET", "POST"])
    def recuperar_acesso():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            recuperacao = criar_token_recuperacao_acesso(
                app.config["DATABASE_PATH"],
                email,
                app.config["RECUPERACAO_TOKEN_MINUTOS"],
            )

            if recuperacao:
                link = f"{app.config['BASE_URL']}{url_for('redefinir_acesso', token=recuperacao['token'])}"
                try:
                    enviar_email_recuperacao(
                        app.config["RESEND_API_KEY"],
                        app.config["RESEND_FROM"],
                        recuperacao["email"],
                        recuperacao["nome"],
                        link,
                    )
                except RuntimeError:
                    app.logger.exception("Falha ao enviar e-mail de recuperação.")

            flash(
                "Se o e-mail estiver cadastrado, você receberá um link de recuperação.",
                "sucesso",
            )
            return redirect(url_for("login"))

        return render_template("recuperar_acesso.html")

    @app.route("/redefinir-acesso/<token>", methods=["GET", "POST"])
    def redefinir_acesso(token: str):
        recuperacao = obter_recuperacao_por_token(
            app.config["DATABASE_PATH"],
            token,
        )
        if not recuperacao:
            flash("Este link é inválido, expirou ou já foi utilizado.", "erro")
            return redirect(url_for("recuperar_acesso"))

        if request.method == "POST":
            tipo = request.form.get("tipo", "").strip()
            nova_senha = request.form.get("nova_senha", "")
            confirmar = request.form.get("confirmar_senha", "")

            if nova_senha != confirmar:
                flash("A confirmação não confere.", "erro")
            elif tipo == "responsavel":
                if len(nova_senha) < 8:
                    flash("A nova senha deve ter pelo menos 8 caracteres.", "erro")
                elif redefinir_senha_responsavel_por_token(
                    app.config["DATABASE_PATH"], token, nova_senha
                ):
                    flash("Senha do responsável atualizada. Faça login.", "sucesso")
                    return redirect(url_for("login"))
            elif tipo == "aluno":
                aluno_id = request.form.get("aluno_id", type=int)
                if not nova_senha.isdigit() or len(nova_senha) < 4 or len(nova_senha) > 6:
                    flash("O novo PIN deve ter entre 4 e 6 números.", "erro")
                elif aluno_id and redefinir_pin_aluno_por_token(
                    app.config["DATABASE_PATH"], token, aluno_id, nova_senha
                ):
                    flash("PIN do aluno atualizado. Ele já pode entrar.", "sucesso")
                    return redirect(url_for("login"))
                else:
                    flash("Selecione um aluno válido.", "erro")
            else:
                flash("Escolha qual acesso deseja recuperar.", "erro")

        return render_template(
            "redefinir_acesso.html",
            token=token,
            recuperacao=recuperacao,
        )

    @app.route("/novo-cadastro", methods=["GET", "POST"])
    def novo_cadastro():
        if session.get("usuario_id"):
            destino = (
                "dashboard_responsavel"
                if session.get("perfil") == "responsavel"
                else "dashboard_aluno"
            )
            return redirect(url_for(destino))

        dados = {
            "nome_responsavel": "",
            "email_responsavel": "",
            "telefone_responsavel": "",
        }

        if request.method == "POST":
            dados = {
                "nome_responsavel": request.form.get(
                    "nome_responsavel",
                    "",
                ).strip(),
                "email_responsavel": request.form.get(
                    "email_responsavel",
                    "",
                ).strip().lower(),
                "telefone_responsavel": request.form.get(
                    "telefone_responsavel",
                    "",
                ).strip(),
            }

            senha_responsavel = request.form.get(
                "senha_responsavel",
                "",
            )
            confirmar_senha = request.form.get(
                "confirmar_senha",
                "",
            )

            if senha_responsavel != confirmar_senha:
                flash(
                    "A confirmação da senha do responsável não confere.",
                    "erro",
                )
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            try:
                cadastro = cadastrar_responsavel(
                    caminho_banco=app.config["DATABASE_PATH"],
                    nome_responsavel=dados["nome_responsavel"],
                    email_responsavel=dados["email_responsavel"],
                    senha_responsavel=senha_responsavel,
                    telefone_responsavel=dados["telefone_responsavel"],
                )
            except ValueError as erro:
                flash(str(erro), "erro")
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            validacao = criar_token_validacao_email(
                app.config["DATABASE_PATH"],
                cadastro["responsavel_id"],
                app.config["VALIDACAO_EMAIL_HORAS"],
                app.config["VALIDACAO_EMAIL_REENVIO_SEGUNDOS"],
                ignorar_intervalo=True,
            )
            if validacao and validacao.get("token"):
                link_validacao = (
                    f"{app.config['BASE_URL']}"
                    f"{url_for('validar_email', token=validacao['token'])}"
                )
                try:
                    enviar_email_validacao(
                        app.config["RESEND_API_KEY"],
                        app.config["RESEND_FROM"],
                        validacao["email"],
                        validacao["nome"],
                        link_validacao,
                    )
                except Exception:
                    app.logger.exception(
                        "Falha ao enviar e-mail de validação após o cadastro."
                    )

            session.clear()
            session.update(
                usuario_id=cadastro["usuario_responsavel_id"],
                nome=dados["nome_responsavel"],
                perfil="responsavel",
            )

            flash(
                "Conta criada. Confirme seu e-mail para cadastrar a criança.",
                "sucesso",
            )
            return redirect(url_for("dashboard_responsavel"))

        return render_template(
            "novo_cadastro.html",
            dados=dados,
        )

    @app.get("/validar-email/<token>")
    def validar_email(token: str):
        if validar_email_por_token(app.config["DATABASE_PATH"], token):
            flash(
                "E-mail validado. Agora você já pode cadastrar a criança.",
                "sucesso",
            )
            destino = (
                "novo_aluno"
                if session.get("perfil") == "responsavel"
                else "login"
            )
        else:
            flash("Este link de validação é inválido, expirou ou já foi utilizado.", "erro")
            destino = (
                "dashboard_responsavel"
                if session.get("perfil") == "responsavel"
                else "login"
            )
        return redirect(url_for(destino))

    @app.post("/responsavel/reenviar-validacao-email")
    @login_obrigatorio("responsavel")
    def reenviar_validacao_email():
        responsavel = buscar_responsavel_por_usuario(
            app.config["DATABASE_PATH"], int(session["usuario_id"])
        )
        if not responsavel or responsavel.get("email_validado_em"):
            flash("Seu e-mail já está validado.", "sucesso")
            return redirect(url_for("dashboard_responsavel"))
        validacao = criar_token_validacao_email(
            app.config["DATABASE_PATH"],
            int(responsavel["id"]),
            app.config["VALIDACAO_EMAIL_HORAS"],
            app.config["VALIDACAO_EMAIL_REENVIO_SEGUNDOS"],
        )
        if validacao and validacao.get("aguarde"):
            flash("Aguarde um minuto antes de solicitar outro e-mail.", "aviso")
            return redirect(url_for("dashboard_responsavel"))
        if validacao and validacao.get("token"):
            link_validacao = f"{app.config['BASE_URL']}{url_for('validar_email', token=validacao['token'])}"
            try:
                enviar_email_validacao(
                    app.config["RESEND_API_KEY"], app.config["RESEND_FROM"],
                    validacao["email"], validacao["nome"], link_validacao,
                )
                flash("Enviamos um novo link de validação para seu e-mail.", "sucesso")
            except Exception:
                app.logger.exception("Falha ao reenviar e-mail de validação.")
                flash("Não foi possível enviar o e-mail agora. Tente novamente em instantes.", "erro")
        return redirect(url_for("dashboard_responsavel"))

    @app.route("/responsavel/consentimento-parental", methods=["GET", "POST"])
    @login_obrigatorio("responsavel")
    def regularizar_consentimento_parental():
        usuario_id = int(session["usuario_id"])
        responsavel = buscar_responsavel_por_usuario(
            app.config["DATABASE_PATH"],
            usuario_id,
        )
        if not responsavel:
            session.clear()
            flash("A conta do responsável não foi encontrada.", "erro")
            return redirect(url_for("login"))

        pendentes = listar_alunos_sem_consentimento_parental(
            app.config["DATABASE_PATH"],
            usuario_id,
        )
        if not pendentes:
            flash("Todos os perfis infantis estão autorizados.", "sucesso")
            return redirect(url_for("dashboard_responsavel"))

        aluno_id = (
            request.form.get("aluno_id", type=int)
            or request.args.get("aluno_id", type=int)
            or int(pendentes[0]["id"])
        )
        aluno = next(
            (
                item
                for item in pendentes
                if int(item["id"]) == int(aluno_id)
            ),
            None,
        )
        if not aluno:
            flash("Perfil infantil inválido para esta regularização.", "erro")
            return redirect(url_for("regularizar_consentimento_parental"))

        if request.method == "POST":
            consentimento_aceito = request.form.get(
                "consentimento_parental",
                "",
            ).strip().lower() in {"1", "on", "true", "sim"}
            declaracao_responsavel = request.form.get(
                "declaracao_responsavel",
                "",
            ).strip().lower() in {"1", "on", "true", "sim"}

            try:
                registrar_consentimento_parental_para_aluno_existente(
                    caminho_banco=app.config["DATABASE_PATH"],
                    usuario_responsavel_id=usuario_id,
                    aluno_id=int(aluno["id"]),
                    consentimento_aceito=consentimento_aceito,
                    declaracao_responsavel=declaracao_responsavel,
                    versao_termo=VERSAO_TERMO_CONSENTIMENTO_PARENTAL,
                    origem_confirmacao=ORIGEM_REGULARIZACAO_CONSENTIMENTO,
                )
            except ValueError as erro:
                flash(str(erro), "erro")
            else:
                restantes = listar_alunos_sem_consentimento_parental(
                    app.config["DATABASE_PATH"],
                    usuario_id,
                )
                if restantes:
                    flash(
                        "Autorização registrada. Confirme agora o próximo perfil infantil.",
                        "sucesso",
                    )
                    return redirect(url_for("regularizar_consentimento_parental"))

                flash(
                    "Consentimentos atualizados. O acesso da família foi liberado.",
                    "sucesso",
                )
                return redirect(url_for("dashboard_responsavel"))

        return render_template(
            "consentimento_parental.html",
            responsavel=responsavel,
            aluno=aluno,
            total_pendentes=len(pendentes),
            email_validado=bool(responsavel.get("email_validado_em")),
            versao_termo_consentimento=VERSAO_TERMO_CONSENTIMENTO_PARENTAL,
        )

    @app.route("/anamnese", methods=["GET", "POST"])
    @login_obrigatorio("responsavel")
    def anamnese():
        usuario_id = int(session["usuario_id"])
        alunos = listar_alunos_do_responsavel(app.config["DATABASE_PATH"], usuario_id)
        if not alunos:
            flash("Cadastre um aluno antes de preencher a anamnese.", "aviso")
            return redirect(url_for("novo_aluno"))

        aluno_id = request.args.get("aluno_id", type=int) or request.form.get("aluno_id", type=int)
        aluno_id = aluno_id or session.get("aluno_responsavel_id") or int(alunos[0]["id"])
        aluno = buscar_aluno_do_responsavel(app.config["DATABASE_PATH"], usuario_id, int(aluno_id))
        if not aluno:
            flash("Aluno não encontrado para esta conta.", "erro")
            return redirect(url_for("dashboard_responsavel"))
        session["aluno_responsavel_id"] = int(aluno["id"])

        estado = obter_estado_anamnese(app.config["DATABASE_PATH"], int(aluno["id"]))
        respostas = estado["respostas"]
        etapa = request.args.get("etapa", type=int) or int(estado.get("etapa_atual") or 1)
        etapa = max(1, min(6, etapa))

        if not respostas:
            registro = buscar_anamnese_por_aluno(app.config["DATABASE_PATH"], int(aluno["id"]))
            if registro:
                respostas.update({"idade": str(registro["idade"]), "ano_escolar": registro["ano_escolar"]})

        if request.method == "POST":
            etapa_post = request.form.get("etapa", type=int) or etapa
            acao = request.form.get("acao", "continuar")
            try:
                if etapa_post <= 5:
                    salvar_etapa_anamnese(app.config["DATABASE_PATH"], int(aluno["id"]), etapa_post, request.form)
                    return redirect(url_for("anamnese", aluno_id=aluno["id"], etapa=min(6, etapa_post + 1)))
                if acao == "confirmar":
                    estado = obter_estado_anamnese(app.config["DATABASE_PATH"], int(aluno["id"]))
                    respostas = estado["respostas"]
                    resumo = montar_resumo_anamnese(respostas, aluno["nome_exibicao"])
                    salvar_anamnese(caminho_banco=app.config["DATABASE_PATH"], aluno_id=int(aluno["id"]), **converter_para_anamnese_legada(respostas))
                    concluir_anamnese_estruturada(app.config["DATABASE_PATH"], int(aluno["id"]), resumo)
                    recalcular_perfil_por_anamnese(app.config["DATABASE_PATH"], int(aluno["id"]))
                    flash("Anamnese concluída. Perfil e missões não iniciadas foram recalculados.", "sucesso")
                    return redirect(url_for("dashboard_responsavel", aluno_id=aluno["id"]))
            except (ValueError, TypeError) as erro:
                flash(str(erro), "erro")
                etapa = etapa_post

        estado = obter_estado_anamnese(app.config["DATABASE_PATH"], int(aluno["id"]))
        respostas = {**respostas, **estado["respostas"]}
        resumo = montar_resumo_anamnese(respostas, aluno["nome_exibicao"]) if etapa == 6 else None
        return render_template(
            "anamnese.html", aluno=aluno, respostas=respostas, etapa=etapa,
            resumo=resumo, opcoes=opcoes_anamnese_template(),
        )

    @app.get("/sair")
    def sair():
        session.clear()
        flash("Você saiu do NettStudy.", "sucesso")
        return redirect(url_for("inicio"))

    @app.get("/portal")
    def portal():
        return render_template("portal.html")

    @app.get("/responsavel")
    @login_obrigatorio("responsavel")
    def dashboard_responsavel():
        usuario_id = int(session["usuario_id"])
        responsavel = buscar_responsavel_por_usuario(app.config["DATABASE_PATH"], usuario_id)
        alunos = listar_alunos_do_responsavel(app.config["DATABASE_PATH"], usuario_id)
        aluno_id = request.args.get("aluno_id", type=int) or session.get("aluno_responsavel_id")
        aluno_registrado = None
        if alunos:
            aluno_id = int(aluno_id or alunos[0]["id"])
            aluno_registrado = buscar_aluno_do_responsavel(app.config["DATABASE_PATH"], usuario_id, aluno_id)
            if not aluno_registrado:
                aluno_registrado = alunos[0]
                aluno_id = int(aluno_registrado["id"])
            session["aluno_responsavel_id"] = aluno_id

        aluno = None
        if aluno_registrado:
            resumo_dia = obter_resumo_diario(app.config["DATABASE_PATH"], aluno_id, date.today().isoformat())
            atividades = []
            for nome in ("Português", "Matemática", "Leitura"):
                chave = nome.lower().replace("á", "a").replace("ê", "e")
                concluida = bool(resumo_dia["materias"].get(chave))
                atividades.append({"nome": nome, "status": "Concluída" if concluida else "Pendente", "progresso": 100 if concluida else 0})
            aluno = {
                "id": aluno_id,
                "nome": aluno_registrado["nome_exibicao"],
                "nome_completo": aluno_registrado["nome_completo"],
                "ano_escolar": aluno_registrado["ano_escolar"] or "Não informado",
                "parentesco": aluno_registrado["parentesco"] or "Responsável",
                "principal": bool(aluno_registrado["principal"]),
                "sequencia": resumo_dia["sequencia"],
                "pontos": resumo_dia["pontos"],
                "progresso_dia": resumo_dia["progresso"],
                "atividades": atividades,
            }
        else:
            resumo_dia = {"materias": {}, "concluidas": 0, "progresso": 0, "pontos": 0, "sequencia": 0}

        anamnese_registro = buscar_anamnese_por_aluno(app.config["DATABASE_PATH"], aluno_id) if aluno else None
        reset_missao = obter_reset_missao_dia(app.config["DATABASE_PATH"], aluno_id, date.today().isoformat()) if aluno else None
        perfil = garantir_perfil_pedagogico(app.config["DATABASE_PATH"], aluno_id) if aluno and anamnese_registro else None
        relatorio = obter_relatorio_pedagogico(app.config["DATABASE_PATH"], aluno_id) if perfil else None
        return render_template(
            "dashboard_responsavel.html", responsavel=responsavel, alunos=alunos,
            aluno=aluno, anamnese=anamnese_registro, resumo_dia=resumo_dia,
            reset_missao=reset_missao, perfil_pedagogico=perfil,
            relatorio=relatorio, limite_alunos=5,
        )

    @app.route("/responsavel/alunos/novo", methods=["GET", "POST"])
    @login_obrigatorio("responsavel")
    def novo_aluno():
        usuario_id = int(session["usuario_id"])
        responsavel = buscar_responsavel_por_usuario(
            app.config["DATABASE_PATH"],
            usuario_id,
        )
        if not responsavel:
            session.clear()
            flash("A conta do responsável não foi encontrada.", "erro")
            return redirect(url_for("login"))
        if not responsavel.get("email_validado_em"):
            flash(
                "Confirme o e-mail do responsável antes de cadastrar a criança.",
                "aviso",
            )
            return redirect(url_for("dashboard_responsavel"))

        alunos = listar_alunos_do_responsavel(app.config["DATABASE_PATH"], usuario_id)
        if len(alunos) >= 5:
            flash("O limite é de cinco alunos por responsável.", "aviso")
            return redirect(url_for("dashboard_responsavel"))

        dados = {"nome_aluno": "", "nome_exibicao_aluno": "", "ano_escolar": "", "usuario_aluno": "", "parentesco": "Responsável"}
        if request.method == "POST":
            dados = {chave: request.form.get(chave, "").strip() for chave in dados}
            pin = request.form.get("pin_aluno", "").strip()
            confirmar = request.form.get("confirmar_pin", "").strip()
            consentimento_aceito = request.form.get(
                "consentimento_parental",
                "",
            ).strip().lower() in {"1", "on", "true", "sim"}
            declaracao_responsavel = request.form.get(
                "declaracao_responsavel",
                "",
            ).strip().lower() in {"1", "on", "true", "sim"}
            if pin != confirmar:
                flash("A confirmação do PIN não confere.", "erro")
                return render_template(
                    "novo_aluno.html",
                    dados=dados,
                    total_alunos=len(alunos),
                    versao_termo_consentimento=VERSAO_TERMO_CONSENTIMENTO_PARENTAL,
                ), 400
            try:
                cadastro = cadastrar_aluno_para_responsavel(
                    app.config["DATABASE_PATH"], usuario_id,
                    dados["nome_aluno"], dados["nome_exibicao_aluno"], dados["ano_escolar"],
                    dados["usuario_aluno"], pin, dados["parentesco"],
                    consentimento_aceito=consentimento_aceito,
                    declaracao_responsavel=declaracao_responsavel,
                    versao_termo=VERSAO_TERMO_CONSENTIMENTO_PARENTAL,
                    origem_confirmacao=ORIGEM_CONSENTIMENTO_PARENTAL,
                )
            except ValueError as erro:
                flash(str(erro), "erro")
                return render_template(
                    "novo_aluno.html",
                    dados=dados,
                    total_alunos=len(alunos),
                    versao_termo_consentimento=VERSAO_TERMO_CONSENTIMENTO_PARENTAL,
                ), 400
            session["aluno_responsavel_id"] = cadastro["aluno_id"]
            flash(
                "Aluno adicionado com o consentimento parental registrado. Agora preencha a avaliação inicial educacional.",
                "sucesso",
            )
            return redirect(url_for("anamnese", aluno_id=cadastro["aluno_id"]))
        return render_template(
            "novo_aluno.html",
            dados=dados,
            total_alunos=len(alunos),
            versao_termo_consentimento=VERSAO_TERMO_CONSENTIMENTO_PARENTAL,
        )

    @app.get("/responsavel/perfil-pedagogico")
    @login_obrigatorio("responsavel")
    def perfil_pedagogico():
        usuario_id = int(session["usuario_id"])
        alunos = listar_alunos_do_responsavel(app.config["DATABASE_PATH"], usuario_id)
        if not alunos:
            flash("Nenhum aluno vinculado.", "aviso")
            return redirect(url_for("dashboard_responsavel"))
        aluno_id = request.args.get("aluno_id", type=int) or session.get("aluno_responsavel_id") or int(alunos[0]["id"])
        aluno = buscar_aluno_do_responsavel(app.config["DATABASE_PATH"], usuario_id, int(aluno_id))
        if not aluno:
            flash("Aluno não encontrado para esta conta.", "erro")
            return redirect(url_for("dashboard_responsavel"))
        session["aluno_responsavel_id"] = int(aluno["id"])
        perfil = garantir_perfil_pedagogico(app.config["DATABASE_PATH"], int(aluno["id"]))
        relatorio = obter_relatorio_pedagogico(app.config["DATABASE_PATH"], int(aluno["id"]))
        simulacao = simular_ciclo_diagnostico(
            app.config["DATABASE_PATH"], int(aluno["id"]),
            QUESTOES_PORTUGUES, QUESTOES_MATEMATICA,
        )
        return render_template(
            "perfil_pedagogico.html", aluno=aluno, perfil=perfil,
            relatorio=relatorio, simulacao=simulacao,
        )

    @app.post("/responsavel/refazer-missao")
    @login_obrigatorio("responsavel")
    def refazer_missao():
        aluno_id = request.form.get("aluno_id", type=int)
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao", "").strip()
        motivo = request.form.get("motivo", "").strip()

        if not aluno_id:
            flash("Aluno inválido para reiniciar a missão.", "erro")
            return redirect(url_for("dashboard_responsavel", aluno_id=aluno_id))

        if confirmacao != "REFAZER":
            flash("Digite REFAZER para confirmar a operação.", "erro")
            return redirect(url_for("dashboard_responsavel", aluno_id=aluno_id))

        usuario = buscar_usuario_por_id(
            app.config["DATABASE_PATH"],
            int(session["usuario_id"]),
        )
        if not usuario or not check_password_hash(usuario["senha_hash"], senha):
            flash("Senha do responsável inválida.", "erro")
            return redirect(url_for("dashboard_responsavel", aluno_id=aluno_id))

        try:
            refazer_missao_do_dia(
                app.config["DATABASE_PATH"],
                int(session["usuario_id"]),
                aluno_id,
                date.today().isoformat(),
                motivo,
            )
        except ValueError as erro:
            flash(str(erro), "erro")
            return redirect(url_for("dashboard_responsavel", aluno_id=aluno_id))

        flash(
            "Missão de hoje reiniciada. O histórico anterior foi preservado.",
            "sucesso",
        )
        return redirect(url_for("dashboard_responsavel", aluno_id=aluno_id))

    @app.get("/aluno")
    @login_obrigatorio("aluno")
    def dashboard_aluno():
        aluno = buscar_aluno_por_usuario(
            app.config["DATABASE_PATH"], int(session["usuario_id"])
        )
        if not aluno:
            session.clear()
            flash("O cadastro do aluno não foi encontrado. Entre novamente.", "erro")
            return redirect(url_for("login"))
        if not buscar_anamnese_por_aluno(app.config["DATABASE_PATH"], int(aluno["id"])):
            session.clear()
            flash("O responsável precisa concluir a anamnese antes das atividades.", "aviso")
            return redirect(url_for("login"))

        resumo_dia = obter_resumo_diario(
            app.config["DATABASE_PATH"], int(aluno["id"]), date.today().isoformat()
        )
        personalizacao = resumo_missao_personalizada(
            app.config["DATABASE_PATH"], int(aluno["id"])
        )
        fluxo = proxima_etapa_missao(
            app.config["DATABASE_PATH"], int(aluno["id"])
        )
        return render_template(
            "dashboard_aluno.html", aluno=aluno, pontos=resumo_dia["pontos"],
            sequencia=resumo_dia["sequencia"],
            atividades_concluidas=resumo_dia["concluidas"],
            progresso=resumo_dia["progresso"],
            personalizacao=personalizacao, fluxo=fluxo,
        )

    @app.get("/missao")
    @login_obrigatorio("aluno")
    def iniciar_ou_continuar_missao():
        aluno = _aluno_logado_com_anamnese()
        if not aluno:
            flash("Conclua a anamnese antes das atividades.", "aviso")
            return redirect(url_for("login"))
        fluxo = proxima_etapa_missao(
            app.config["DATABASE_PATH"], int(aluno["id"])
        )
        if fluxo["concluida"]:
            return redirect(url_for("dashboard_aluno"))
        session["etapa_missao"] = fluxo["etapa"]
        return redirect(url_for(fluxo["rota"]))

    def _aluno_logado_com_anamnese() -> dict[str, Any] | None:
        aluno = buscar_aluno_por_usuario(
            app.config["DATABASE_PATH"],
            int(session["usuario_id"]),
        )
        if not aluno or not buscar_anamnese_por_aluno(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
        ):
            return None
        return aluno

    def _processar_atividade_adaptativa(
        aluno: dict[str, Any],
        materia: str,
        nome_materia: str,
        questoes: list[dict[str, Any]],
        obter_questao: Callable,
        validar_resposta: Callable,
        enriquecer_resultado: Callable,
        template: str,
        texto: str | None = None,
    ):
        data_atividade = date.today().isoformat()
        plano_pedagogico = gerar_plano_missao(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
            materia,
            questoes,
            data_atividade,
        )
        codigos = plano_pedagogico["codigos"]
        sessao_adaptativa = obter_ou_criar_sessao_adaptativa(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
            data_atividade,
            materia,
            codigos,
        )

        if sessao_adaptativa["status"] == "concluida":
            resultado = finalizar_sessao_adaptativa(
                app.config["DATABASE_PATH"],
                int(sessao_adaptativa["id"]),
            )
            return render_template(
                "resultado_atividade.html",
                materia=nome_materia,
                resultado=enriquecer_resultado(resultado),
                adaptativa=True,
            )

        if request.method == "POST":
            codigo = request.form.get("questao_codigo", "").strip()
            resposta = request.form.get("resposta", "").strip()
            questao = obter_questao(codigo)
            if not questao or not resposta:
                flash("Escolha uma resposta para continuar.", "erro")
                return redirect(url_for(request.endpoint))

            tentativa = registrar_tentativa_adaptativa(
                app.config["DATABASE_PATH"],
                int(sessao_adaptativa["id"]),
                codigo,
                resposta,
                validar_resposta(questao, resposta),
            )
            registrar_desempenho(
                app.config["DATABASE_PATH"],
                int(aluno["id"]),
                data_atividade,
                materia,
                questao,
                tentativa["numero_tentativa"],
                tentativa["correta"],
                tentativa["dica_nivel"],
                tentativa["resposta_revelada"],
                tentativa["pontos"],
            )

            dica = None
            if tentativa["dica_nivel"]:
                dica = questao["dicas"][tentativa["dica_nivel"] - 1]

            session["feedback_adaptativo"] = {
                "materia": materia,
                "acertou": tentativa["correta"],
                "tentativa": tentativa["numero_tentativa"],
                "pontos": tentativa["pontos"],
                "dica": dica,
                "resposta_revelada": tentativa["resposta_revelada"],
                "resposta_correta": questao["correta"] if tentativa["resposta_revelada"] else None,
                "explicacao": questao["explicacao"] if tentativa["resposta_revelada"] else None,
                "concluida": tentativa["concluida"],
            }
            return redirect(url_for(request.endpoint, retorno="1"))

        feedback = None
        if request.args.get("retorno") == "1":
            candidato = session.pop("feedback_adaptativo", None)
            if candidato and candidato.get("materia") == materia:
                feedback = candidato

        if feedback:
            return render_template(
                template,
                aluno=aluno,
                materia=nome_materia,
                texto=texto,
                feedback=feedback,
                questao=None,
                progresso=sessao_adaptativa["progresso"],
                plano_pedagogico=plano_pedagogico,
            )

        sessao_adaptativa = obter_ou_criar_sessao_adaptativa(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
            data_atividade,
            materia,
            codigos,
        )
        if sessao_adaptativa["status"] == "concluida":
            resultado = finalizar_sessao_adaptativa(
                app.config["DATABASE_PATH"],
                int(sessao_adaptativa["id"]),
            )
            return render_template(
                "resultado_atividade.html",
                materia=nome_materia,
                resultado=enriquecer_resultado(resultado),
                adaptativa=True,
            )

        questao = obter_questao(sessao_adaptativa["questao_atual"])
        return render_template(
            template,
            aluno=aluno,
            materia=nome_materia,
            texto=texto,
            feedback=None,
            questao=questao,
            progresso=sessao_adaptativa["progresso"],
            plano_pedagogico=plano_pedagogico,
        )

    @app.route("/atividade/matematica", methods=["GET", "POST"])
    @login_obrigatorio("aluno")
    def atividade_matematica():
        aluno = _aluno_logado_com_anamnese()
        if not aluno:
            flash("Conclua a anamnese antes das atividades.", "aviso")
            return redirect(url_for("login"))
        return _processar_atividade_adaptativa(
            aluno,
            "matematica",
            "Matemática",
            QUESTOES_MATEMATICA,
            obter_questao_matematica,
            resposta_correta_matematica,
            enriquecer_resultado_matematica,
            "atividade_matematica.html",
        )

    @app.route("/atividade/portugues", methods=["GET", "POST"])
    @login_obrigatorio("aluno")
    def atividade_portugues():
        aluno = _aluno_logado_com_anamnese()
        if not aluno:
            flash("Conclua a anamnese antes das atividades.", "aviso")
            return redirect(url_for("login"))
        return _processar_atividade_adaptativa(
            aluno,
            "portugues",
            "Português",
            QUESTOES_PORTUGUES,
            obter_questao_portugues,
            resposta_correta_portugues,
            enriquecer_resultado_portugues,
            "atividade_portugues.html",
            TEXTO,
        )

    @app.route("/atividade/leitura", methods=["GET", "POST"])
    @login_obrigatorio("aluno")
    def atividade_leitura():
        aluno = _aluno_logado_com_anamnese()
        if not aluno:
            flash("Conclua a anamnese antes das atividades.", "aviso")
            return redirect(url_for("login"))

        data_atividade = date.today().isoformat()
        anamnese = buscar_anamnese_por_aluno(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
        )
        perfil_leitura = garantir_perfil_pedagogico(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
        )
        historia = obter_historia_do_dia(
            aluno_id=int(aluno["id"]),
            nivel_leitura=int(perfil_leitura["nivel_leitura"]),
            interesses=perfil_leitura.get("temas_preferidos", ""),
            historias_excluidas=historias_lidas_ciclo(
                app.config["DATABASE_PATH"], int(aluno["id"]), data_atividade
            ),
        )
        codigos = [
            pergunta["id"]
            for pergunta in historia["perguntas"]
        ]
        sessao_leitura = obter_ou_criar_sessao_leitura(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
            data_atividade,
            historia["id"],
            historia["titulo"],
            codigos,
        )

        if sessao_leitura["historia_id"] != historia["id"]:
            historia_vinculada = obter_historia_por_id(
                sessao_leitura["historia_id"]
            )
            if historia_vinculada:
                historia = historia_vinculada
            else:
                app.logger.error(
                    "História %s vinculada à sessão %s não foi encontrada.",
                    sessao_leitura["historia_id"],
                    sessao_leitura["id"],
                )
                flash(
                    "Não foi possível carregar a leitura de hoje. Tente reiniciar a missão.",
                    "erro",
                )
                return redirect(url_for("dashboard_aluno"))

        if sessao_leitura["fase"] == "concluida":
            resultado = obter_resultado_sessao_leitura(
                app.config["DATABASE_PATH"],
                int(sessao_leitura["id"]),
            )
            for detalhe in resultado["detalhes"]:
                pergunta = obter_pergunta_leitura(historia, detalhe["id"])
                if pergunta:
                    detalhe.update(
                        {
                            "enunciado": pergunta["enunciado"],
                            "correta": pergunta["correta"],
                            "explicacao": pergunta["explicacao"],
                        }
                    )
            return render_template(
                "resultado_atividade.html",
                materia="Leitura",
                resultado=resultado,
                leitura=True,
            )

        if request.method == "POST":
            acao = request.form.get("acao", "").strip()

            if acao == "iniciar_perguntas":
                iniciar_perguntas_leitura(
                    app.config["DATABASE_PATH"],
                    int(sessao_leitura["id"]),
                )
                return redirect(url_for("atividade_leitura"))

            if acao == "responder":
                codigo = request.form.get("pergunta_codigo", "").strip()
                resposta = request.form.get("resposta", "").strip()
                pergunta = obter_pergunta_leitura(historia, codigo)

                if not pergunta or not resposta:
                    flash("Escolha uma resposta para continuar.", "erro")
                    return redirect(url_for("atividade_leitura"))

                tentativa = registrar_tentativa_leitura(
                    app.config["DATABASE_PATH"],
                    int(sessao_leitura["id"]),
                    codigo,
                    resposta,
                    resposta_correta_leitura(pergunta, resposta),
                )
                registrar_desempenho(
                    app.config["DATABASE_PATH"],
                    int(aluno["id"]),
                    data_atividade,
                    "leitura",
                    pergunta,
                    tentativa["numero_tentativa"],
                    tentativa["correta"],
                    tentativa["dica_nivel"],
                    tentativa["resposta_revelada"],
                    tentativa["pontos"],
                )

                dica = None
                if tentativa["dica_nivel"]:
                    dica = pergunta["dicas"][tentativa["dica_nivel"] - 1]

                session["feedback_leitura"] = {
                    "acertou": tentativa["correta"],
                    "tentativa": tentativa["numero_tentativa"],
                    "pontos": tentativa["pontos"],
                    "dica": dica,
                    "resposta_revelada": tentativa["resposta_revelada"],
                    "resposta_correta": (
                        pergunta["correta"]
                        if tentativa["resposta_revelada"]
                        else None
                    ),
                    "explicacao": (
                        pergunta["explicacao"]
                        if tentativa["resposta_revelada"]
                        else None
                    ),
                    "pagina_evidencia": pergunta["pagina_evidencia"],
                    "perguntas_concluidas": tentativa["perguntas_concluidas"],
                }
                return redirect(
                    url_for(
                        "atividade_leitura",
                        retorno="1",
                    )
                )

            if acao == "avaliar_resumo":
                resumo = request.form.get("resumo", "").strip()
                avaliacao = avaliar_resumo(
                    historia,
                    resumo,
                    int(perfil_leitura["nivel_leitura"]),
                )
                versao = registrar_versao_resumo(
                    app.config["DATABASE_PATH"],
                    int(sessao_leitura["id"]),
                    resumo,
                    avaliacao,
                )

                if avaliacao["status"] == "concluido":
                    resultado = obter_resultado_sessao_leitura(
                        app.config["DATABASE_PATH"],
                        int(sessao_leitura["id"]),
                    )
                    for detalhe in resultado["detalhes"]:
                        pergunta = obter_pergunta_leitura(
                            historia,
                            detalhe["id"],
                        )
                        if pergunta:
                            detalhe.update(
                                {
                                    "enunciado": pergunta["enunciado"],
                                    "correta": pergunta["correta"],
                                    "explicacao": pergunta["explicacao"],
                                }
                            )

                    registrar_resultado_atividade(
                        app.config["DATABASE_PATH"],
                        int(aluno["id"]),
                        data_atividade,
                        "leitura",
                        resultado,
                        historia["titulo"],
                    )

                    return render_template(
                        "resultado_atividade.html",
                        materia="Leitura",
                        resultado=resultado,
                        leitura=True,
                        avaliacao_resumo=versao,
                    )

                return render_template(
                    "atividade_leitura.html",
                    aluno=aluno,
                    historia=historia,
                    sessao=sessao_leitura,
                    fase="resumo",
                    resumo=resumo,
                    avaliacao_resumo=versao,
                    feedback=None,
                    pergunta=None,
                ), 400

        sessao_leitura = obter_ou_criar_sessao_leitura(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
            data_atividade,
            historia["id"],
            historia["titulo"],
            codigos,
        )

        feedback = None
        if request.args.get("retorno") == "1":
            feedback = session.pop("feedback_leitura", None)

        if feedback:
            return render_template(
                "atividade_leitura.html",
                aluno=aluno,
                historia=historia,
                sessao=sessao_leitura,
                fase="feedback",
                feedback=feedback,
                pergunta=None,
                resumo="",
                avaliacao_resumo=None,
            )

        pergunta = None
        if sessao_leitura["fase"] == "perguntas":
            pergunta = obter_pergunta_leitura(
                historia,
                sessao_leitura["pergunta_atual"],
            )

        return render_template(
            "atividade_leitura.html",
            aluno=aluno,
            historia=historia,
            sessao=sessao_leitura,
            fase=sessao_leitura["fase"],
            pergunta=pergunta,
            feedback=None,
            resumo="",
            avaliacao_resumo=None,
        )

    @app.get("/pwa-instalar")
    def pwa_instalar():
        return render_template("pwa_instalar.html")

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            produto="NettStudy",
            ambiente=app.config["APP_ENV"],
        )


def registrar_erros(app: Flask) -> None:
    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template(
            "portal.html",
            erro="Página não encontrada.",
        ), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        return jsonify(
            erro="Erro interno do servidor.",
            status=500,
        ), 500


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=app.config["DEBUG"],
    )
