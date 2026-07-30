# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\app.py
# Data e hora do último recode: 30/07/2026 18:41 -03:00
# Motivo da alteração: integrar anamnese pedagógica em cinco etapas com resumo final.

import os
from datetime import date
from functools import wraps
from typing import Any, Callable

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

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
    obter_pergunta as obter_pergunta_leitura,
    resposta_correta as resposta_correta_leitura,
)
from modules.motor_pedagogico import (
    garantir_perfil_pedagogico,
    gerar_plano_missao,
    inicializar_motor_pedagogico,
    obter_perfil_pedagogico,
    registrar_desempenho,
    resumo_missao_personalizada,
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
    buscar_anamnese_por_aluno,
    buscar_responsavel_por_usuario,
    buscar_usuario_por_login,
    buscar_usuario_por_id,
    cadastrar_familia,
    inicializar_banco,
    listar_alunos_do_responsavel,
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
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    inicializar_banco(app.config["DATABASE_PATH"])
    inicializar_motor_pedagogico(app.config["DATABASE_PATH"])
    inicializar_anamnese_pedagogica(app.config["DATABASE_PATH"])
    registrar_contexto(app)
    registrar_rotas(app)
    registrar_erros(app)
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

            destino = (
                "dashboard_responsavel"
                if usuario["perfil"] == "responsavel"
                else "dashboard_aluno"
            )

            return redirect(url_for(destino))

        return render_template("login.html")

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
            "parentesco": "Responsável",
            "nome_aluno": "",
            "nome_exibicao_aluno": "",
            "ano_escolar": "",
            "usuario_aluno": "",
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
                "parentesco": request.form.get(
                    "parentesco",
                    "Responsável",
                ).strip(),
                "nome_aluno": request.form.get(
                    "nome_aluno",
                    "",
                ).strip(),
                "nome_exibicao_aluno": request.form.get(
                    "nome_exibicao_aluno",
                    "",
                ).strip(),
                "ano_escolar": request.form.get(
                    "ano_escolar",
                    "",
                ).strip(),
                "usuario_aluno": request.form.get(
                    "usuario_aluno",
                    "",
                ).strip().lower(),
            }

            senha_responsavel = request.form.get(
                "senha_responsavel",
                "",
            )
            confirmar_senha = request.form.get(
                "confirmar_senha",
                "",
            )
            pin_aluno = request.form.get(
                "pin_aluno",
                "",
            ).strip()
            confirmar_pin = request.form.get(
                "confirmar_pin",
                "",
            ).strip()

            if senha_responsavel != confirmar_senha:
                flash(
                    "A confirmação da senha do responsável não confere.",
                    "erro",
                )
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            if pin_aluno != confirmar_pin:
                flash(
                    "A confirmação do PIN do aluno não confere.",
                    "erro",
                )
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            try:
                cadastro = cadastrar_familia(
                    caminho_banco=app.config["DATABASE_PATH"],
                    nome_responsavel=dados["nome_responsavel"],
                    email_responsavel=dados["email_responsavel"],
                    senha_responsavel=senha_responsavel,
                    telefone_responsavel=dados["telefone_responsavel"],
                    nome_aluno=dados["nome_aluno"],
                    nome_exibicao_aluno=dados["nome_exibicao_aluno"],
                    ano_escolar=dados["ano_escolar"],
                    usuario_aluno=dados["usuario_aluno"],
                    pin_aluno=pin_aluno,
                    parentesco=dados["parentesco"],
                )
            except ValueError as erro:
                flash(str(erro), "erro")
                return render_template(
                    "novo_cadastro.html",
                    dados=dados,
                ), 400

            session.clear()
            session.update(
                usuario_id=cadastro["usuario_responsavel_id"],
                nome=dados["nome_responsavel"],
                perfil="responsavel",
            )

            flash(
                "Cadastro criado com sucesso. Bem-vindo ao NettStudy!",
                "sucesso",
            )
            return redirect(url_for("anamnese"))

        return render_template(
            "novo_cadastro.html",
            dados=dados,
        )

    @app.route("/anamnese", methods=["GET", "POST"])
    @login_obrigatorio("responsavel")
    def anamnese():
        usuario_id = int(session["usuario_id"])
        alunos = listar_alunos_do_responsavel(app.config["DATABASE_PATH"], usuario_id)
        if not alunos:
            flash("Cadastre um aluno antes de preencher a anamnese.", "aviso")
            return redirect(url_for("dashboard_responsavel"))

        aluno = alunos[0]
        aluno_id = int(aluno["id"])
        estado = obter_estado_anamnese(app.config["DATABASE_PATH"], aluno_id)
        respostas = estado["respostas"]
        etapa = request.args.get("etapa", type=int) or int(estado.get("etapa_atual") or 1)
        etapa = max(1, min(6, etapa))

        if not respostas:
            registro = buscar_anamnese_por_aluno(app.config["DATABASE_PATH"], aluno_id)
            if registro:
                respostas.update({"idade": str(registro["idade"]), "ano_escolar": registro["ano_escolar"]})

        if request.method == "POST":
            etapa_post = request.form.get("etapa", type=int) or etapa
            acao = request.form.get("acao", "continuar")
            try:
                if etapa_post <= 5:
                    salvar_etapa_anamnese(
                        app.config["DATABASE_PATH"], aluno_id, etapa_post, request.form
                    )
                    return redirect(url_for("anamnese", etapa=min(6, etapa_post + 1)))

                if acao == "confirmar":
                    estado = obter_estado_anamnese(app.config["DATABASE_PATH"], aluno_id)
                    respostas = estado["respostas"]
                    resumo = montar_resumo_anamnese(respostas, aluno["nome_exibicao"])
                    legado = converter_para_anamnese_legada(respostas)
                    salvar_anamnese(
                        caminho_banco=app.config["DATABASE_PATH"], aluno_id=aluno_id,
                        **legado,
                    )
                    concluir_anamnese_estruturada(
                        app.config["DATABASE_PATH"], aluno_id, resumo
                    )
                    garantir_perfil_pedagogico(app.config["DATABASE_PATH"], aluno_id)
                    flash("Anamnese concluída e perfil pedagógico atualizado.", "sucesso")
                    return redirect(url_for("dashboard_responsavel"))
            except (ValueError, TypeError) as erro:
                flash(str(erro), "erro")
                etapa = etapa_post

        estado = obter_estado_anamnese(app.config["DATABASE_PATH"], aluno_id)
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

        responsavel = buscar_responsavel_por_usuario(
            app.config["DATABASE_PATH"],
            usuario_id,
        )

        alunos = listar_alunos_do_responsavel(
            app.config["DATABASE_PATH"],
            usuario_id,
        )

        aluno = None

        if alunos:
            aluno_registrado = alunos[0]
            aluno = {
                "id": aluno_registrado["id"],
                "nome": aluno_registrado["nome_exibicao"],
                "nome_completo": aluno_registrado["nome_completo"],
                "ano_escolar": aluno_registrado["ano_escolar"] or "Não informado",
                "parentesco": aluno_registrado["parentesco"] or "Responsável",
                "principal": bool(aluno_registrado["principal"]),
                "sequencia": 0,
                "pontos": 0,
                "progresso_dia": 0,
                "atividades": [
                    {
                        "nome": "Português",
                        "status": "Pendente",
                        "progresso": 0,
                    },
                    {
                        "nome": "Matemática",
                        "status": "Pendente",
                        "progresso": 0,
                    },
                    {
                        "nome": "Leitura",
                        "status": "Pendente",
                        "progresso": 0,
                    },
                ],
            }

        anamnese_registro = (
            buscar_anamnese_por_aluno(
                app.config["DATABASE_PATH"],
                int(aluno["id"]),
            )
            if aluno
            else None
        )

        resumo_dia = (
            obter_resumo_diario(
                app.config["DATABASE_PATH"],
                int(aluno["id"]),
                date.today().isoformat(),
            )
            if aluno
            else {"materias": {}, "concluidas": 0, "progresso": 0, "pontos": 0, "sequencia": 0}
        )

        if aluno:
            aluno["sequencia"] = resumo_dia["sequencia"]
            aluno["pontos"] = resumo_dia["pontos"]
            aluno["progresso_dia"] = resumo_dia["progresso"]
            for atividade in aluno["atividades"]:
                chave = atividade["nome"].lower().replace("á", "a").replace("ê", "e")
                registro = resumo_dia["materias"].get(chave)
                if registro:
                    atividade["status"] = "Concluída"
                    atividade["progresso"] = 100

        reset_missao = (
            obter_reset_missao_dia(
                app.config["DATABASE_PATH"],
                int(aluno["id"]),
                date.today().isoformat(),
            )
            if aluno
            else None
        )

        perfil_pedagogico = (
            garantir_perfil_pedagogico(
                app.config["DATABASE_PATH"],
                int(aluno["id"]),
            )
            if aluno and anamnese_registro
            else None
        )

        return render_template(
            "dashboard_responsavel.html",
            responsavel=responsavel,
            alunos=alunos,
            aluno=aluno,
            anamnese=anamnese_registro,
            resumo_dia=resumo_dia,
            reset_missao=reset_missao,
            perfil_pedagogico=perfil_pedagogico,
        )

    @app.get("/responsavel/perfil-pedagogico")
    @login_obrigatorio("responsavel")
    def perfil_pedagogico():
        alunos = listar_alunos_do_responsavel(
            app.config["DATABASE_PATH"],
            int(session["usuario_id"]),
        )
        if not alunos:
            flash("Nenhum aluno vinculado.", "aviso")
            return redirect(url_for("dashboard_responsavel"))
        aluno = alunos[0]
        perfil = garantir_perfil_pedagogico(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
        )
        return render_template(
            "perfil_pedagogico.html",
            aluno=aluno,
            perfil=perfil,
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
            return redirect(url_for("dashboard_responsavel"))

        if confirmacao != "REFAZER":
            flash("Digite REFAZER para confirmar a operação.", "erro")
            return redirect(url_for("dashboard_responsavel"))

        usuario = buscar_usuario_por_id(
            app.config["DATABASE_PATH"],
            int(session["usuario_id"]),
        )
        if not usuario or not check_password_hash(usuario["senha_hash"], senha):
            flash("Senha do responsável inválida.", "erro")
            return redirect(url_for("dashboard_responsavel"))

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
            return redirect(url_for("dashboard_responsavel"))

        flash(
            "Missão de hoje reiniciada. O histórico anterior foi preservado.",
            "sucesso",
        )
        return redirect(url_for("dashboard_responsavel"))

    @app.get("/aluno")
    @login_obrigatorio("aluno")
    def dashboard_aluno():
        usuario_id = int(session["usuario_id"])

        aluno = buscar_aluno_por_usuario(
            app.config["DATABASE_PATH"],
            usuario_id,
        )

        if not aluno:
            session.clear()
            flash(
                "O cadastro do aluno não foi encontrado. Entre novamente.",
                "erro",
            )
            return redirect(url_for("login"))

        anamnese_registro = buscar_anamnese_por_aluno(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
        )

        if not anamnese_registro:
            session.clear()
            flash(
                "O responsável precisa concluir a anamnese antes do início das atividades.",
                "aviso",
            )
            return redirect(url_for("login"))

        resumo_dia = obter_resumo_diario(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
            date.today().isoformat(),
        )
        personalizacao = resumo_missao_personalizada(
            app.config["DATABASE_PATH"],
            int(aluno["id"]),
        )
        quantidade = personalizacao["quantidade_questoes"]
        configuracao = [
            ("Português", "portugues", f"{quantidade} questões personalizadas", "atividade_portugues"),
            ("Matemática", "matematica", f"{quantidade} questões personalizadas", "atividade_matematica"),
            ("Leitura", "leitura", "História autoral, interpretação e resumo", "atividade_leitura"),
        ]
        missao = [
            {
                "nome": nome,
                "chave": chave,
                "descricao": descricao,
                "rota": rota,
                "concluida": chave in resumo_dia["materias"],
            }
            for nome, chave, descricao, rota in configuracao
        ]

        return render_template(
            "dashboard_aluno.html",
            aluno=aluno,
            missao=missao,
            pontos=resumo_dia["pontos"],
            sequencia=resumo_dia["sequencia"],
            atividades_concluidas=resumo_dia["concluidas"],
            progresso=resumo_dia["progresso"],
            personalizacao=personalizacao,
        )

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
        historia = obter_historia_do_dia(
            aluno_id=int(aluno["id"]),
            nivel_leitura=(
                anamnese["nivel_leitura"]
                if anamnese
                else "basico"
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
                avaliacao = avaliar_resumo(historia, resumo)
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
