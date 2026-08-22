# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\motor_pedagogico.py
# Data e hora do último recode: 22/08/2026 02:41 -03:00
# Motivo da alteração: iniciar cada matéria no nível sugerido pela avaliação inicial por faixa etária.

import json
import random
import re
import unicodedata
from datetime import date, timedelta
from typing import Any

from database import buscar_anamnese_por_aluno, conectar
from modules.tempo import data_app, data_iso_app

SCHEMA = """
CREATE TABLE IF NOT EXISTS perfis_pedagogicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL UNIQUE,
    faixa_desenvolvimento TEXT NOT NULL,
    nivel_matematica INTEGER NOT NULL DEFAULT 1,
    nivel_portugues INTEGER NOT NULL DEFAULT 1,
    nivel_leitura INTEGER NOT NULL DEFAULT 1,
    dias_diagnostico INTEGER NOT NULL DEFAULT 5,
    diagnostico_concluido INTEGER NOT NULL DEFAULT 0 CHECK (diagnostico_concluido IN (0, 1)),
    quantidade_questoes INTEGER NOT NULL DEFAULT 10,
    temas_preferidos TEXT,
    origem TEXT NOT NULL DEFAULT 'anamnese',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS dominio_habilidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    materia TEXT NOT NULL,
    habilidade TEXT NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 1,
    dominio REAL NOT NULL DEFAULT 40,
    status TEXT NOT NULL DEFAULT 'em_diagnostico',
    total_tentativas INTEGER NOT NULL DEFAULT 0,
    acertos_primeira INTEGER NOT NULL DEFAULT 0,
    dicas_utilizadas INTEGER NOT NULL DEFAULT 0,
    respostas_reveladas INTEGER NOT NULL DEFAULT 0,
    atualizado_em TEXT,
    UNIQUE (aluno_id, materia, habilidade),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS eventos_desempenho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    materia TEXT NOT NULL,
    habilidade TEXT NOT NULL,
    questao_codigo TEXT NOT NULL,
    nivel_questao INTEGER NOT NULL,
    numero_tentativa INTEGER NOT NULL,
    correta INTEGER NOT NULL DEFAULT 0,
    dica_nivel INTEGER NOT NULL DEFAULT 0,
    resposta_revelada INTEGER NOT NULL DEFAULT 0,
    pontos INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS planos_missao_diaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    materia TEXT NOT NULL,
    fase TEXT NOT NULL,
    nivel_alvo INTEGER NOT NULL,
    quantidade_itens INTEGER NOT NULL,
    foco_habilidade TEXT,
    codigos_json TEXT NOT NULL DEFAULT '[]',
    composicao_json TEXT NOT NULL DEFAULT '{}',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (aluno_id, data_atividade, materia),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);
"""

HABILIDADES = {
    "matematica": ["numeros_quantidades","adicao_visual","adicao","subtracao","multiplicacao","divisao","problemas","fracoes","medidas","dinheiro","geometria","sequencias","raciocinio_logico","porcentagem","algebra","proporcionalidade"],
    "portugues": ["vocabulario_visual","som_inicial","ortografia","pontuacao","classes_palavras","formacao_frases","vocabulario","sinonimos_antonimos","interpretacao","gramatica_aplicada","producao_textual","localizacao_informacoes","sequencia_acontecimentos","coesao","concordancia"],
    "leitura": ["leitura_literal","localizacao_informacoes","sequencia_acontecimentos","personagens","causa_consequencia","inferencia","ideia_principal","vocabulario_contexto","resumo","opiniao_fundamentada"],
}

ROTULOS_HABILIDADES = {chave: chave.replace("_"," ").title() for lista in HABILIDADES.values() for chave in lista}
STATUS_ROTULOS = {"nao_avaliada":"Não avaliada","em_diagnostico":"Em diagnóstico","precisa_reforco":"Precisa de reforço","em_aprendizagem":"Em aprendizagem","consolidada":"Consolidada","dominada":"Dominada"}


def inicializar_motor_pedagogico(caminho_banco: str) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA)


def _normalizar(texto: str | None) -> str:
    base = unicodedata.normalize("NFKD", texto or "")
    base = "".join(c for c in base if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", base.lower())


def _ano_numero(ano_escolar: str | None) -> int:
    encontrado = re.search(r"(\d+)", ano_escolar or "")
    return max(1, min(5, int(encontrado.group(1)))) if encontrado else 1


def _faixa(idade: int) -> str:
    if idade <= 5: return "4-5"
    if idade <= 8: return "6-8"
    if idade <= 11: return "9-11"
    return "12-13"


def obter_faixa_etaria_aluno(caminho_banco: str, aluno_id: int) -> str:
    anamnese = buscar_anamnese_por_aluno(caminho_banco, aluno_id)
    if not anamnese:
        raise ValueError("A avaliação inicial precisa ser concluída antes de iniciar a missão.")
    return _faixa(int(anamnese["idade"]))


def materias_missao_aluno(caminho_banco: str, aluno_id: int) -> tuple[str, ...]:
    faixa_etaria = obter_faixa_etaria_aluno(caminho_banco, aluno_id)
    if faixa_etaria in {"4-5", "6-8"}:
        return ("portugues", "matematica")
    return ("portugues", "matematica", "leitura")


def _quantidade_por_concentracao(minutos: int) -> int:
    if minutos <= 10: return 6
    if minutos <= 15: return 8
    return 10


def _nivel_leitura(valor: str | None, ano: int) -> int:
    mapa = {"iniciante":1,"basico":2,"intermediario":4,"avancado":5}
    return max(1, min(5, round((mapa.get((valor or "").lower(), ano) + ano) / 2)))


def _niveis_da_avaliacao(caminho_banco: str, aluno_id: int, padrao: dict[str, int]) -> dict[str, int]:
    with conectar(caminho_banco) as conexao:
        registro = conexao.execute(
            "SELECT resumo_json FROM anamneses_estruturadas WHERE aluno_id = ? AND concluida = 1",
            (aluno_id,),
        ).fetchone()
    if not registro or not registro["resumo_json"]:
        return padrao
    try:
        resumo = json.loads(registro["resumo_json"])
        sugeridos = resumo.get("niveis_iniciais", {})
        return {
            materia: max(1, min(5, int(sugeridos.get(materia, nivel))))
            for materia, nivel in padrao.items()
        }
    except (TypeError, ValueError, json.JSONDecodeError):
        return padrao


def garantir_perfil_pedagogico(caminho_banco: str, aluno_id: int) -> dict[str, Any]:
    anamnese = buscar_anamnese_por_aluno(caminho_banco, aluno_id)
    if not anamnese:
        raise ValueError("A avaliação inicial precisa ser concluída antes do perfil pedagógico.")
    ano = _ano_numero(anamnese["ano_escolar"])
    idade = int(anamnese["idade"])
    quantidade = _quantidade_por_concentracao(int(anamnese["tempo_concentracao"]))
    niveis_padrao = {"matematica":ano,"portugues":ano,"leitura":_nivel_leitura(anamnese["nivel_leitura"],ano)}
    niveis = _niveis_da_avaliacao(caminho_banco, aluno_id, niveis_padrao)
    temas = anamnese["materias_preferidas"] or anamnese["objetivo_principal"] or ""
    with conectar(caminho_banco) as conexao:
        perfil = conexao.execute("SELECT * FROM perfis_pedagogicos WHERE aluno_id = ?",(aluno_id,)).fetchone()
        if not perfil:
            conexao.execute("""INSERT INTO perfis_pedagogicos
                (aluno_id,faixa_desenvolvimento,nivel_matematica,nivel_portugues,nivel_leitura,quantidade_questoes,temas_preferidos)
                VALUES (?,?,?,?,?,?,?)""",(aluno_id,_faixa(idade),niveis["matematica"],niveis["portugues"],niveis["leitura"],quantidade,temas))
        else:
            tentativas = conexao.execute("SELECT COUNT(*) total FROM eventos_desempenho WHERE aluno_id=?",(aluno_id,)).fetchone()["total"]
            if int(tentativas or 0) == 0:
                conexao.execute("""UPDATE perfis_pedagogicos SET faixa_desenvolvimento=?,nivel_matematica=?,nivel_portugues=?,nivel_leitura=?,quantidade_questoes=?,temas_preferidos=?,atualizado_em=CURRENT_TIMESTAMP WHERE aluno_id=?""",
                    (_faixa(idade),niveis["matematica"],niveis["portugues"],niveis["leitura"],quantidade,temas,aluno_id))
            else:
                conexao.execute("UPDATE perfis_pedagogicos SET faixa_desenvolvimento=?,quantidade_questoes=?,temas_preferidos=?,atualizado_em=CURRENT_TIMESTAMP WHERE aluno_id=?",
                    (_faixa(idade),quantidade,temas,aluno_id))
        for materia, habilidades in HABILIDADES.items():
            for habilidade in habilidades:
                conexao.execute("""INSERT INTO dominio_habilidades (aluno_id,materia,habilidade,nivel,dominio,status)
                    VALUES (?,?,?,?,42,'em_diagnostico')
                    ON CONFLICT(aluno_id,materia,habilidade) DO UPDATE SET nivel=excluded.nivel,atualizado_em=CURRENT_TIMESTAMP
                    WHERE dominio_habilidades.total_tentativas=0""",(aluno_id,materia,habilidade,niveis[materia]))
    return obter_perfil_pedagogico(caminho_banco,aluno_id)


def obter_perfil_pedagogico(caminho_banco: str, aluno_id: int) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        perfil = conexao.execute("SELECT * FROM perfis_pedagogicos WHERE aluno_id=?",(aluno_id,)).fetchone()
        if not perfil: return {}
        dominios = conexao.execute("SELECT * FROM dominio_habilidades WHERE aluno_id=? ORDER BY materia,dominio,habilidade",(aluno_id,)).fetchall()
        dias = conexao.execute("SELECT COUNT(DISTINCT data_atividade) total FROM eventos_desempenho WHERE aluno_id=?",(aluno_id,)).fetchone()["total"]
    grupos={"matematica":[],"portugues":[],"leitura":[]}
    for item in dominios:
        r=dict(item); r["rotulo"]=ROTULOS_HABILIDADES.get(r["habilidade"],r["habilidade"]); r["status_rotulo"]=STATUS_ROTULOS.get(r["status"],r["status"]); r["dominio"]=round(float(r["dominio"])); grupos[r["materia"]].append(r)
    resultado=dict(perfil); resultado["dominios"]=grupos; resultado["dias_observados"]=int(dias or 0); resultado["dias_restantes_diagnostico"]=max(0,int(perfil["dias_diagnostico"])-int(dias or 0)); resultado["fase"]="adaptativa" if perfil["diagnostico_concluido"] else "diagnostico"
    return resultado


def _status_por_dominio(valor: float, diagnostico: bool) -> str:
    if diagnostico: return "em_diagnostico"
    if valor < 40: return "precisa_reforco"
    if valor < 70: return "em_aprendizagem"
    if valor < 88: return "consolidada"
    return "dominada"


def registrar_desempenho(caminho_banco: str, aluno_id: int, data_atividade: str, materia: str,
    questao: dict[str, Any], numero_tentativa: int, correta: bool, dica_nivel: int,
    resposta_revelada: bool, pontos: int) -> None:
    habilidade=questao.get("habilidade","geral"); nivel_questao=int(questao.get("nivel",1))
    with conectar(caminho_banco) as conexao:
        conexao.execute("""INSERT INTO eventos_desempenho (aluno_id,data_atividade,materia,habilidade,questao_codigo,nivel_questao,numero_tentativa,correta,dica_nivel,resposta_revelada,pontos)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(aluno_id,data_atividade,materia,habilidade,questao["id"],nivel_questao,numero_tentativa,int(correta),dica_nivel,int(resposta_revelada),pontos))
        dominio=conexao.execute("SELECT * FROM dominio_habilidades WHERE aluno_id=? AND materia=? AND habilidade=?",(aluno_id,materia,habilidade)).fetchone()
        if not dominio:
            conexao.execute("INSERT INTO dominio_habilidades (aluno_id,materia,habilidade,nivel,dominio,status) VALUES (?,?,?,?,40,'em_diagnostico')",(aluno_id,materia,habilidade,nivel_questao)); atual=40.0; nivel_atual=nivel_questao
        else: atual=float(dominio["dominio"]); nivel_atual=int(dominio["nivel"])
        delta=8 if correta and numero_tentativa==1 else 5 if correta and numero_tentativa==2 else 2 if correta else -8 if resposta_revelada else -2
        novo=max(0,min(100,atual+delta))
        recentes=conexao.execute("SELECT correta,numero_tentativa FROM eventos_desempenho WHERE aluno_id=? AND materia=? AND habilidade=? ORDER BY id DESC LIMIT 8",(aluno_id,materia,habilidade)).fetchall()
        taxa=(sum(1 if r["correta"] and r["numero_tentativa"]==1 else .7 if r["correta"] else 0 for r in recentes)/len(recentes)) if recentes else 0
        novo_nivel=nivel_atual
        if len(recentes)>=5 and taxa>=.8 and novo>=78: novo_nivel=min(5,nivel_atual+1)
        elif len(recentes)>=5 and taxa<.5 and novo<40: novo_nivel=max(1,nivel_atual-1)
        dias=conexao.execute("SELECT COUNT(DISTINCT data_atividade) total FROM eventos_desempenho WHERE aluno_id=?",(aluno_id,)).fetchone()["total"]
        perfil=conexao.execute("SELECT dias_diagnostico FROM perfis_pedagogicos WHERE aluno_id=?",(aluno_id,)).fetchone()
        diagnostico=int(dias or 0)<int(perfil["dias_diagnostico"] if perfil else 5)
        conexao.execute("""UPDATE dominio_habilidades SET nivel=?,dominio=?,status=?,total_tentativas=total_tentativas+1,
            acertos_primeira=acertos_primeira+?,dicas_utilizadas=dicas_utilizadas+?,respostas_reveladas=respostas_reveladas+?,atualizado_em=CURRENT_TIMESTAMP
            WHERE aluno_id=? AND materia=? AND habilidade=?""",(novo_nivel,novo,_status_por_dominio(novo,diagnostico),int(correta and numero_tentativa==1),int(dica_nivel>0),int(resposta_revelada),aluno_id,materia,habilidade))
        campo=f"nivel_{materia}"
        conexao.execute(f"UPDATE perfis_pedagogicos SET {campo}=(SELECT ROUND(AVG(nivel)) FROM dominio_habilidades WHERE aluno_id=? AND materia=?), diagnostico_concluido=?, atualizado_em=CURRENT_TIMESTAMP WHERE aluno_id=?",(aluno_id,materia,int(not diagnostico),aluno_id))


def _composicao(quantidade: int, nivel_alvo: int) -> dict[str,int]:
    revisao = 0 if nivel_alvo == 1 else max(1,round(quantidade*.30))
    desafio = max(1,round(quantidade*.20))
    atual = quantidade-revisao-desafio
    return {"revisao":revisao,"atual":atual,"desafio":desafio}


def _escolher(grupo: list[dict[str,Any]], quantidade: int, foco: str | None) -> list[dict[str,Any]]:
    ordenado=sorted(grupo,key=lambda q:(0 if q.get("habilidade")==foco else 1,random.random()))
    return ordenado[:quantidade]


def _codigos_usados_ciclo(
    caminho_banco: str,
    aluno_id: int,
    materia: str,
    data_ref: str,
    dias: int = 5,
) -> tuple[set[str], set[str]]:
    inicio = (date.fromisoformat(data_ref) - timedelta(days=max(1, dias - 1))).isoformat()
    with conectar(caminho_banco) as conexao:
        planos = conexao.execute(
            """SELECT codigos_json
               FROM planos_missao_diaria
               WHERE aluno_id = ? AND materia = ?
                 AND data_atividade BETWEEN ? AND ?
                 AND data_atividade <> ?""",
            (aluno_id, materia, inicio, data_ref, data_ref),
        ).fetchall()
        reforco = conexao.execute(
            """SELECT DISTINCT questao_codigo
               FROM eventos_desempenho
               WHERE aluno_id = ? AND materia = ?
                 AND data_atividade BETWEEN ? AND ?
                 AND (correta = 0 OR resposta_revelada = 1)""",
            (aluno_id, materia, inicio, data_ref),
        ).fetchall()

    usados: set[str] = set()
    for plano in planos:
        try:
            usados.update(json.loads(plano["codigos_json"]))
        except (TypeError, json.JSONDecodeError):
            continue
    codigos_reforco = {str(item["questao_codigo"]) for item in reforco}
    return usados, codigos_reforco


def _preencher_categoria(
    selecionadas: list[dict[str, Any]],
    grupo: list[dict[str, Any]],
    quantidade: int,
    foco: str | None,
) -> None:
    usados = {item["id"] for item in selecionadas}
    disponiveis = [item for item in grupo if item["id"] not in usados]
    selecionadas.extend(_escolher(disponiveis, quantidade, foco))


def gerar_plano_missao(
    caminho_banco: str,
    aluno_id: int,
    materia: str,
    questoes: list[dict[str, Any]],
    data_atividade: str | None = None,
) -> dict[str, Any]:
    data_ref = data_atividade or data_iso_app()
    perfil = garantir_perfil_pedagogico(caminho_banco, aluno_id)
    nivel_alvo = int(perfil[f"nivel_{materia}"])
    faixa_etaria = perfil["faixa_desenvolvimento"]
    questoes_faixa = [
        item
        for item in questoes
        if item.get("faixa_etaria") == faixa_etaria
    ]
    if not questoes_faixa:
        raise ValueError(
            f"Nenhuma questão de {materia} disponível para a faixa {faixa_etaria}."
        )
    quantidade = min(int(perfil["quantidade_questoes"]), len(questoes_faixa))
    dominios = perfil["dominios"].get(materia, [])
    foco = dominios[0]["habilidade"] if dominios else None
    fase = perfil["fase"]
    comp = _composicao(quantidade, nivel_alvo)

    usados_ciclo, reforco = _codigos_usados_ciclo(
        caminho_banco, aluno_id, materia, data_ref
    )
    permitidas = [
        item for item in questoes_faixa
        if int(item.get("nivel", 1)) <= nivel_alvo + 1
        and (item["id"] not in usados_ciclo or item["id"] in reforco)
    ]
    if len(permitidas) < quantidade:
        permitidas = [
            item for item in questoes_faixa
            if int(item.get("nivel", 1)) <= nivel_alvo + 1
        ]

    revisao = [item for item in permitidas if int(item.get("nivel", 1)) < nivel_alvo]
    atuais = [item for item in permitidas if int(item.get("nivel", 1)) == nivel_alvo]
    desafios = [item for item in permitidas if int(item.get("nivel", 1)) == nivel_alvo + 1]

    selecionadas: list[dict[str, Any]] = []
    _preencher_categoria(selecionadas, revisao, comp["revisao"], foco)
    _preencher_categoria(selecionadas, atuais, comp["atual"], foco)
    _preencher_categoria(selecionadas, desafios, comp["desafio"], foco)

    faltam = quantidade - len(selecionadas)
    if faltam > 0:
        reforcos_prioritarios = [
            item for item in permitidas if item["id"] in reforco
        ]
        _preencher_categoria(selecionadas, reforcos_prioritarios, faltam, foco)

    faltam = quantidade - len(selecionadas)
    if faltam > 0:
        _preencher_categoria(selecionadas, permitidas, faltam, foco)

    selecionadas = selecionadas[:quantidade]
    codigos = [item["id"] for item in selecionadas]

    with conectar(caminho_banco) as conexao:
        existente = conexao.execute(
            """SELECT * FROM planos_missao_diaria
               WHERE aluno_id = ? AND data_atividade = ? AND materia = ?""",
            (aluno_id, data_ref, materia),
        ).fetchone()
        if existente:
            antigos = json.loads(existente["codigos_json"])
            sessao = conexao.execute(
                """SELECT id FROM sessoes_adaptativas
                   WHERE aluno_id = ? AND data_atividade = ? AND materia = ?""",
                (aluno_id, data_ref, materia),
            ).fetchone()
            tentativas = 0
            if sessao:
                tentativas = conexao.execute(
                    """SELECT COUNT(*) total FROM tentativas_adaptativas
                       WHERE sessao_id = ?""",
                    (sessao["id"],),
                ).fetchone()["total"]
            mapa = {item["id"]: item for item in questoes_faixa}
            valido = all(
                codigo in mapa
                and int(mapa[codigo].get("nivel", 1)) <= nivel_alvo + 1
                and (codigo not in usados_ciclo or codigo in reforco)
                for codigo in antigos
            )
            if int(tentativas or 0) > 0 or valido:
                plano = dict(existente)
                plano["codigos"] = antigos
                plano["composicao"] = json.loads(plano.pop("composicao_json"))
                plano.pop("codigos_json", None)
                return plano
            conexao.execute(
                "DELETE FROM planos_missao_diaria WHERE id = ?",
                (existente["id"],),
            )

        conexao.execute(
            """INSERT INTO planos_missao_diaria (
                   aluno_id, data_atividade, materia, fase, nivel_alvo,
                   quantidade_itens, foco_habilidade, codigos_json,
                   composicao_json
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                aluno_id, data_ref, materia, fase, nivel_alvo,
                len(codigos), foco, json.dumps(codigos),
                json.dumps(comp),
            ),
        )
    return gerar_plano_missao(
        caminho_banco, aluno_id, materia, questoes, data_ref
    )


def recalcular_perfil_por_anamnese(
    caminho_banco: str,
    aluno_id: int,
) -> dict[str, Any]:
    perfil = garantir_perfil_pedagogico(caminho_banco, aluno_id)
    hoje = data_iso_app()
    with conectar(caminho_banco) as conexao:
        sessoes_ativas = conexao.execute(
            """SELECT id, materia
               FROM sessoes_adaptativas
               WHERE aluno_id = ? AND data_atividade = ? AND status = 'ativa'""",
            (aluno_id, hoje),
        ).fetchall()
        for sessao in sessoes_ativas:
            total = conexao.execute(
                "SELECT COUNT(*) total FROM tentativas_adaptativas WHERE sessao_id = ?",
                (sessao["id"],),
            ).fetchone()["total"]
            if int(total or 0) == 0:
                conexao.execute(
                    "DELETE FROM sessoes_adaptativas WHERE id = ?",
                    (sessao["id"],),
                )
                conexao.execute(
                    """DELETE FROM planos_missao_diaria
                       WHERE aluno_id = ? AND data_atividade = ? AND materia = ?""",
                    (aluno_id, hoje, sessao["materia"]),
                )

        leitura = conexao.execute(
            """SELECT id FROM sessoes_leitura
               WHERE aluno_id = ? AND data_atividade = ?""",
            (aluno_id, hoje),
        ).fetchone()
        if leitura:
            total = conexao.execute(
                "SELECT COUNT(*) total FROM tentativas_leitura WHERE sessao_id = ?",
                (leitura["id"],),
            ).fetchone()["total"]
            if int(total or 0) == 0:
                conexao.execute(
                    "DELETE FROM sessoes_leitura WHERE id = ?",
                    (leitura["id"],),
                )
    with conectar(caminho_banco) as conexao:
        for materia in ("matematica", "portugues", "leitura"):
            media = conexao.execute(
                """SELECT ROUND(AVG(nivel)) nivel
                   FROM dominio_habilidades
                   WHERE aluno_id = ? AND materia = ?""",
                (aluno_id, materia),
            ).fetchone()["nivel"]
            if media:
                conexao.execute(
                    f"""UPDATE perfis_pedagogicos
                        SET nivel_{materia} = ?, atualizado_em = CURRENT_TIMESTAMP
                        WHERE aluno_id = ?""",
                    (max(1, min(5, int(media))), aluno_id),
                )
        conexao.execute(
            """DELETE FROM planos_missao_diaria
               WHERE aluno_id = ? AND data_atividade = ?
                 AND materia NOT IN (
                     SELECT materia FROM sessoes_adaptativas
                     WHERE aluno_id = ? AND data_atividade = ?
                 )""",
            (aluno_id, hoje, aluno_id, hoje),
        )
    return obter_perfil_pedagogico(caminho_banco, aluno_id)


def proxima_etapa_missao(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str | None = None,
) -> dict[str, Any]:
    data_ref = data_atividade or data_iso_app()
    materias_permitidas = set(materias_missao_aluno(caminho_banco, aluno_id))
    ordem_completa = [
        ("portugues", "Português", "atividade_portugues"),
        ("matematica", "Matemática", "atividade_matematica"),
        ("leitura", "Leitura", "atividade_leitura"),
    ]
    ordem = [item for item in ordem_completa if item[0] in materias_permitidas]
    total_etapas = len(ordem)
    with conectar(caminho_banco) as conexao:
        concluidas = {
            item["materia"]
            for item in conexao.execute(
                """SELECT materia FROM atividades_diarias
                   WHERE aluno_id = ? AND data_atividade = ?
                     AND status = 'concluida'""",
                (aluno_id, data_ref),
            ).fetchall()
        }
    for indice, (chave, nome, rota) in enumerate(ordem, start=1):
        if chave not in concluidas:
            return {
                "concluida": False,
                "chave": chave,
                "nome": nome,
                "rota": rota,
                "etapa": indice,
                "total_etapas": total_etapas,
                "rotulo_botao": "Iniciar atividades" if not concluidas else "Continuar atividades",
            }
    return {
        "concluida": True,
        "chave": None,
        "nome": "Missão concluída",
        "rota": "dashboard_aluno",
        "etapa": total_etapas,
        "total_etapas": total_etapas,
        "rotulo_botao": "Missão concluída",
    }


def obter_relatorio_pedagogico(
    caminho_banco: str,
    aluno_id: int,
    dias: int = 30,
) -> dict[str, Any]:
    inicio = (data_app() - timedelta(days=max(1, dias - 1))).isoformat()
    with conectar(caminho_banco) as conexao:
        linhas = conexao.execute(
            """SELECT materia, habilidade,
                      COUNT(*) tentativas,
                      SUM(CASE WHEN correta = 1 AND numero_tentativa = 1 THEN 1 ELSE 0 END) acertos_primeira,
                      SUM(CASE WHEN dica_nivel > 0 THEN 1 ELSE 0 END) dicas,
                      SUM(CASE WHEN resposta_revelada = 1 THEN 1 ELSE 0 END) reveladas,
                      ROUND(AVG(pontos), 1) media_pontos
               FROM eventos_desempenho
               WHERE aluno_id = ? AND data_atividade >= ?
               GROUP BY materia, habilidade
               ORDER BY materia, tentativas DESC""",
            (aluno_id, inicio),
        ).fetchall()
        dias_ativos = conexao.execute(
            """SELECT COUNT(DISTINCT data_atividade) total
               FROM atividades_diarias
               WHERE aluno_id = ? AND data_atividade >= ?""",
            (aluno_id, inicio),
        ).fetchone()["total"]

    por_materia = {"portugues": [], "matematica": [], "leitura": []}
    for linha in linhas:
        item = dict(linha)
        tentativas = max(1, int(item["tentativas"]))
        item["taxa_primeira"] = round(int(item["acertos_primeira"] or 0) / tentativas * 100)
        item["rotulo"] = ROTULOS_HABILIDADES.get(item["habilidade"], item["habilidade"])
        por_materia.setdefault(item["materia"], []).append(item)

    fortes = []
    atencao = []
    for materia, itens in por_materia.items():
        for item in itens:
            resumo = {"materia": materia, **item}
            if item["taxa_primeira"] >= 75 and int(item["reveladas"] or 0) == 0:
                fortes.append(resumo)
            elif item["taxa_primeira"] < 50 or int(item["reveladas"] or 0) > 0:
                atencao.append(resumo)
    return {
        "periodo_dias": dias,
        "dias_ativos": int(dias_ativos or 0),
        "por_materia": por_materia,
        "fortes": fortes[:5],
        "atencao": atencao[:5],
    }


def simular_ciclo_diagnostico(
    caminho_banco: str,
    aluno_id: int,
    questoes_portugues: list[dict[str, Any]],
    questoes_matematica: list[dict[str, Any]],
    dias: int = 5,
) -> list[dict[str, Any]]:
    perfil = garantir_perfil_pedagogico(caminho_banco, aluno_id)
    usados = {"portugues": set(), "matematica": set()}
    resultado = []
    for deslocamento in range(dias):
        data_ref = data_app() + timedelta(days=deslocamento)
        dia = {"dia": deslocamento + 1, "data": data_ref.isoformat()}
        for materia, banco in (
            ("portugues", questoes_portugues),
            ("matematica", questoes_matematica),
        ):
            banco = [
                item
                for item in banco
                if item.get("faixa_etaria") == perfil["faixa_desenvolvimento"]
            ]
            nivel = int(perfil[f"nivel_{materia}"])
            comp = _composicao(min(int(perfil["quantidade_questoes"]), len(banco)), nivel)
            candidatas = [
                item for item in banco
                if int(item.get("nivel", 1)) <= nivel + 1
                and item["id"] not in usados[materia]
            ]
            categorias = (
                [item for item in candidatas if int(item["nivel"]) < nivel],
                [item for item in candidatas if int(item["nivel"]) == nivel],
                [item for item in candidatas if int(item["nivel"]) == nivel + 1],
            )
            selecionadas = (
                categorias[0][:comp["revisao"]]
                + categorias[1][:comp["atual"]]
                + categorias[2][:comp["desafio"]]
            )
            if len(selecionadas) < sum(comp.values()):
                restantes = [item for item in candidatas if item not in selecionadas]
                selecionadas.extend(restantes[:sum(comp.values()) - len(selecionadas)])
            usados[materia].update(item["id"] for item in selecionadas)
            dia[materia] = selecionadas
        resultado.append(dia)
    return resultado


def historias_lidas_ciclo(
    caminho_banco: str,
    aluno_id: int,
    data_atividade: str | None = None,
    dias: int = 5,
) -> set[str]:
    data_ref = data_atividade or data_iso_app()
    inicio = (date.fromisoformat(data_ref) - timedelta(days=max(1, dias - 1))).isoformat()
    with conectar(caminho_banco) as conexao:
        linhas = conexao.execute(
            """SELECT DISTINCT historia_id
               FROM sessoes_leitura
               WHERE aluno_id = ? AND data_atividade BETWEEN ? AND ?
                 AND data_atividade <> ?""",
            (aluno_id, inicio, data_ref, data_ref),
        ).fetchall()
    return {str(item["historia_id"]) for item in linhas}


def resumo_missao_personalizada(caminho_banco: str, aluno_id: int) -> dict[str,Any]:
    perfil=garantir_perfil_pedagogico(caminho_banco,aluno_id)
    return {"fase":perfil["fase"],"dias_observados":perfil["dias_observados"],"dias_restantes":perfil["dias_restantes_diagnostico"],"quantidade_questoes":perfil["quantidade_questoes"],"faixa":perfil["faixa_desenvolvimento"],"focos":{m:(d[0] if d else None) for m,d in perfil["dominios"].items()}}
