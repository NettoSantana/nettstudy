# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\motor_pedagogico.py
# Data e hora do último recode: 24/11/2026 20:48 -03:00
# Motivo da alteração: corrigir progressão por habilidade, diversificar tarefas e leituras e revisar propostas de escrita.

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
    if materia not in HABILIDADES:
        raise ValueError("Matéria inválida.")
    habilidade = questao.get("habilidade", "geral")
    nivel_questao = int(questao.get("nivel", 1))
    with conectar(caminho_banco) as conexao:
        # Um reenvio da mesma tentativa não pode alterar domínio ou promover duas vezes.
        duplicada = conexao.execute(
            "SELECT 1 FROM eventos_desempenho WHERE aluno_id=? AND data_atividade=? AND materia=? AND questao_codigo=? AND numero_tentativa=?",
            (aluno_id,data_atividade,materia,questao["id"],numero_tentativa),
        ).fetchone()
        if duplicada:
            return
        conexao.execute("""INSERT INTO eventos_desempenho (aluno_id,data_atividade,materia,habilidade,questao_codigo,nivel_questao,numero_tentativa,correta,dica_nivel,resposta_revelada,pontos)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(aluno_id,data_atividade,materia,habilidade,questao["id"],nivel_questao,numero_tentativa,int(correta),dica_nivel,int(resposta_revelada),pontos))
        dominio = conexao.execute("SELECT * FROM dominio_habilidades WHERE aluno_id=? AND materia=? AND habilidade=?",(aluno_id,materia,habilidade)).fetchone()
        if not dominio:
            conexao.execute("INSERT INTO dominio_habilidades (aluno_id,materia,habilidade,nivel,dominio,status) VALUES (?,?,?,?,40,'em_diagnostico')",(aluno_id,materia,habilidade,nivel_questao))
            dominio = conexao.execute("SELECT * FROM dominio_habilidades WHERE aluno_id=? AND materia=? AND habilidade=?",(aluno_id,materia,habilidade)).fetchone()
        nivel_atual = int(dominio["nivel"])
        delta = 7 if correta and numero_tentativa==1 and dica_nivel==0 else 3 if correta else -4
        novo = max(0,min(100,float(dominio["dominio"])+delta))
        # Somente primeiras tentativas em itens distintos do nível atual contam para avanço.
        faixa_perfil=conexao.execute("SELECT faixa_desenvolvimento FROM perfis_pedagogicos WHERE aluno_id=?",(aluno_id,)).fetchone()
        legado_inicial=bool(faixa_perfil and faixa_perfil["faixa_desenvolvimento"]=="4-5")
        recentes = conexao.execute("""SELECT e.* FROM eventos_desempenho e
            WHERE e.aluno_id=? AND e.materia=? AND e.habilidade=?
              AND e.numero_tentativa=1 AND (?=1 OR e.questao_codigo LIKE '%v3%') AND e.nivel_questao>=?
              AND e.id=(SELECT MAX(x.id) FROM eventos_desempenho x
                WHERE x.aluno_id=e.aluno_id AND x.materia=e.materia AND x.habilidade=e.habilidade
                  AND x.questao_codigo=e.questao_codigo AND x.numero_tentativa=1)
            ORDER BY e.id DESC LIMIT 8""",(aluno_id,materia,habilidade,int(legado_inicial),nivel_atual)).fetchall()
        acertos = sum(bool(r["correta"]) and not r["dica_nivel"] and not r["resposta_revelada"] for r in recentes)
        novo_nivel = nivel_atual
        if (questao.get("versao")==3 or legado_inicial) and len(recentes)>=5 and acertos/len(recentes)>=0.8 and novo>=75:
            novo_nivel = min(5,nivel_atual+1)
        # Erros em revisões fáceis não justificam reduzir uma habilidade avançada.
        if (questao.get("versao")==3 or legado_inicial) and len(recentes)>=5 and acertos/len(recentes)<0.4 and novo<35:
            novo_nivel = max(1,nivel_atual-1)
        dias=conexao.execute("SELECT COUNT(DISTINCT data_atividade) total FROM eventos_desempenho WHERE aluno_id=?",(aluno_id,)).fetchone()["total"]
        perfil=conexao.execute("SELECT dias_diagnostico FROM perfis_pedagogicos WHERE aluno_id=?",(aluno_id,)).fetchone()
        diagnostico=int(dias or 0)<int(perfil["dias_diagnostico"] if perfil else 5)
        conexao.execute("""UPDATE dominio_habilidades SET nivel=?,dominio=?,status=?,total_tentativas=total_tentativas+1,
            acertos_primeira=acertos_primeira+?,dicas_utilizadas=dicas_utilizadas+?,respostas_reveladas=respostas_reveladas+?,atualizado_em=CURRENT_TIMESTAMP
            WHERE aluno_id=? AND materia=? AND habilidade=?""",(novo_nivel,novo,_status_por_dominio(novo,diagnostico),int(correta and numero_tentativa==1),int(dica_nivel>0),int(resposta_revelada),aluno_id,materia,habilidade))
        # O indicador geral usa apenas habilidades efetivamente praticadas.
        campo=f"nivel_{materia}"
        conexao.execute(f"UPDATE perfis_pedagogicos SET {campo}=(SELECT ROUND(AVG(nivel)) FROM dominio_habilidades WHERE aluno_id=? AND materia=? AND total_tentativas>0), diagnostico_concluido=?, atualizado_em=CURRENT_TIMESTAMP WHERE aluno_id=?",(aluno_id,materia,int(not diagnostico),aluno_id))


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
    dias: int = 16,
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


def _chave_conteudo(questao: dict[str, Any]) -> str:
    # Nas tarefas de pontuação, as frases estão nas alternativas.
    base = _normalizar(questao["enunciado"])
    if questao.get("habilidade") == "pontuacao":
        base += "|" + "|".join(sorted(_normalizar(str(valor)) for valor in questao["alternativas"]))
    return base


def _preencher_categoria(
    selecionadas: list[dict[str, Any]],
    grupo: list[dict[str, Any]],
    quantidade: int,
    foco: str | None,
) -> None:
    usados = {item["id"] for item in selecionadas}
    textos = {_chave_conteudo(item) for item in selecionadas}
    disponiveis = []
    for item in grupo:
        texto = _chave_conteudo(item)
        if item["id"] not in usados and texto not in textos:
            disponiveis.append(item)
            textos.add(texto)
    selecionadas.extend(_escolher(disponiveis, quantidade, foco))


def gerar_plano_missao(caminho_banco: str, aluno_id: int, materia: str,
    questoes: list[dict[str, Any]], data_atividade: str | None = None) -> dict[str, Any]:
    data_ref = data_atividade or data_iso_app()
    perfil = garantir_perfil_pedagogico(caminho_banco, aluno_id)
    with conectar(caminho_banco) as conexao:
        existente = conexao.execute("SELECT * FROM planos_missao_diaria WHERE aluno_id=? AND data_atividade=? AND materia=?",(aluno_id,data_ref,materia)).fetchone()
        # Nunca substitua um plano no meio da sessão, nem sorteie a cada abertura.
        if existente:
            plano=dict(existente);plano["codigos"]=json.loads(plano.pop("codigos_json"));plano["composicao"]=json.loads(plano.pop("composicao_json"));return plano
        anteriores = conexao.execute("SELECT data_atividade,codigos_json FROM planos_missao_diaria WHERE aluno_id=? AND materia=? AND data_atividade<? ORDER BY data_atividade",(aluno_id,materia,data_ref)).fetchall()
    faixa = perfil["faixa_desenvolvimento"]
    banco = [q for q in questoes if q.get("faixa_etaria")==faixa]
    novos = [q for q in banco if q.get("versao")==3]
    banco = novos or banco
    if not banco:
        raise ValueError(f"Não há questões de {materia} para {faixa}.")
    mapa={q["id"]:q for q in questoes}
    ultima={}; ultima_familia={}
    for registro in anteriores:
        for codigo in json.loads(registro["codigos_json"]):
            q=mapa.get(codigo)
            if q:
                chave=q.get("assinatura") or _chave_conteudo(q)
                ultima[chave]=registro["data_atividade"]
                ultima_familia[q.get("familia",q["habilidade"])]=registro["data_atividade"]
    dominios={d["habilidade"]:d for d in perfil["dominios"].get(materia,[])}
    praticados=[int(d["nivel"]) for d in dominios.values() if int(d.get("total_tentativas",0))>0]
    base=int(round(sum(praticados)/len(praticados))) if praticados else int(perfil[f"nivel_{materia}"])
    base=max(1,min(5,base))
    por_habilidade={}
    for q in banco:
        por_habilidade.setdefault(q["habilidade"],[]).append(q)
    rng=random.Random(f"{aluno_id}:{data_ref}:{materia}:curriculo3")
    for h in list(por_habilidade):
        dominio=dominios.get(h,{})
        alvo=int(dominio["nivel"]) if int(dominio.get("total_tentativas",0))>0 else base
        por_habilidade[h]=[q for q in por_habilidade[h] if max(1,alvo-1)<=int(q["nivel"])<=min(5,alvo+1)]
        if not por_habilidade[h]:
            del por_habilidade[h]
    habilidades=list(por_habilidade)
    if not habilidades:
        habilidades=list(por_habilidade)
    rng.shuffle(habilidades)
    habilidades.sort(key=lambda h:(0 if int(dominios.get(h,{}).get("total_tentativas",0))>0 and float(dominios[h]["dominio"])<55 else 1,
        min(ultima_familia.get(q.get("familia",h),"") for q in por_habilidade[h])))
    quantidade=min(int(perfil["quantidade_questoes"]),len(banco))
    selecionadas=[];usados=set();familias={};composicao={"revisao":0,"atual":0,"desafio":0}
    limite_recente=(date.fromisoformat(data_ref)-timedelta(days=15)).isoformat()
    novidades={q.get("assinatura") or _chave_conteudo(q) for qs in por_habilidade.values() for q in qs
               if ultima.get(q.get("assinatura") or _chave_conteudo(q),"")<limite_recente}
    for rodada in range(quantidade*3):
        for habilidade in habilidades:
            if len(selecionadas)>=quantidade:
                break
            dominio=dominios.get(habilidade,{})
            # Domínios nunca praticados usam a base atual, sem prender o aluno ao cadastro antigo.
            alvo=int(dominio["nivel"]) if int(dominio.get("total_tentativas",0))>0 else base
            # Um desafio e uma revisão a cada cinco itens, os demais do nível da habilidade.
            categoria="desafio" if len(selecionadas)%5==4 and alvo<5 else "revisao" if len(selecionadas)%5==3 and alvo>1 else "atual"
            nivel_desejado=min(5,alvo+1) if categoria=="desafio" else max(1,alvo-1) if categoria=="revisao" else alvo
            candidatas=[q for q in por_habilidade[habilidade] if (q.get("assinatura") or _chave_conteudo(q)) not in usados]
            if not candidatas:
                continue
            rng.shuffle(candidatas)
            limite_recente=(date.fromisoformat(data_ref)-timedelta(days=15)).isoformat()
            candidatas.sort(key=lambda q:(
                1 if ultima.get(q.get("assinatura") or _chave_conteudo(q),"")>=limite_recente else 0,
                abs(int(q["nivel"])-nivel_desejado),
                familias.get(q.get("familia",habilidade),0),
                1 if (q.get("assinatura") or _chave_conteudo(q)) in ultima else 0,
                ultima.get(q.get("assinatura") or _chave_conteudo(q),"")))
            q=candidatas[0]
            chave_escolhida=q.get("assinatura") or _chave_conteudo(q)
            if ultima.get(chave_escolhida,"")>=limite_recente and novidades-usados:
                continue
            familia=q.get("familia",habilidade)
            # Evitar que milhares de variações de uma família ocupem a missão inteira.
            limite=2
            if familias.get(familia,0)>=limite and rodada<quantidade:
                continue
            selecionadas.append(q);usados.add(q.get("assinatura") or _chave_conteudo(q));familias[familia]=familias.get(familia,0)+1
            real="revisao" if int(q["nivel"])<alvo else "desafio" if int(q["nivel"])>alvo else "atual"
            composicao[real]+=1
        if len(selecionadas)>=quantidade:
            break
    codigos=[q["id"] for q in selecionadas]
    foco=habilidades[0] if habilidades else None
    with conectar(caminho_banco) as conexao:
        # INSERT OR IGNORE também protege duas requisições simultâneas.
        conexao.execute("""INSERT OR IGNORE INTO planos_missao_diaria
            (aluno_id,data_atividade,materia,fase,nivel_alvo,quantidade_itens,foco_habilidade,codigos_json,composicao_json)
            VALUES (?,?,?,?,?,?,?,?,?)""",(aluno_id,data_ref,materia,perfil["fase"],base,len(codigos),foco,json.dumps(codigos),json.dumps(composicao)))
        linha=conexao.execute("SELECT * FROM planos_missao_diaria WHERE aluno_id=? AND data_atividade=? AND materia=?",(aluno_id,data_ref,materia)).fetchone()
    plano=dict(linha);plano["codigos"]=json.loads(plano.pop("codigos_json"));plano["composicao"]=json.loads(plano.pop("composicao_json"));return plano


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
                   WHERE aluno_id = ? AND materia = ? AND total_tentativas > 0""",
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
    dias: int = 16,
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


def historias_lidas_ciclo(caminho_banco: str, aluno_id: int,
    data_atividade: str | None = None, dias: int = 16) -> set[str]:
    class HistoricoLeitura(set):
        pass
    data_ref=data_atividade or data_iso_app()
    with conectar(caminho_banco) as conexao:
        linhas=conexao.execute("SELECT historia_id,MAX(data_atividade) ultima FROM sessoes_leitura WHERE aluno_id=? AND data_atividade<? GROUP BY historia_id",(aluno_id,data_ref)).fetchall()
    resultado=HistoricoLeitura(str(r["historia_id"]) for r in linhas)
    resultado.ultima_leitura={str(r["historia_id"]):r["ultima"] for r in linhas}
    return resultado


def resumo_missao_personalizada(caminho_banco: str, aluno_id: int) -> dict[str,Any]:
    perfil=garantir_perfil_pedagogico(caminho_banco,aluno_id)
    return {"fase":perfil["fase"],"dias_observados":perfil["dias_observados"],"dias_restantes":perfil["dias_restantes_diagnostico"],"quantidade_questoes":perfil["quantidade_questoes"],"faixa":perfil["faixa_desenvolvimento"],"focos":{m:(d[0] if d else None) for m,d in perfil["dominios"].items()}}

