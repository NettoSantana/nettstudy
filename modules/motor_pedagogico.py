# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\motor_pedagogico.py
# Data e hora do último recode: 30/07/2026 18:41 -03:00
# Motivo da alteração: incorporar a anamnese estruturada à hipótese inicial sem sobrescrever desempenho real.

import json
import random
import re
import sqlite3
import unicodedata
from datetime import date, datetime, timedelta
from typing import Any

from database import buscar_anamnese_por_aluno, conectar


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
    materia TEXT NOT NULL CHECK (materia IN ('matematica', 'portugues', 'leitura')),
    habilidade TEXT NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 1,
    dominio REAL NOT NULL DEFAULT 40,
    status TEXT NOT NULL DEFAULT 'em_diagnostico'
        CHECK (status IN ('nao_avaliada', 'em_diagnostico', 'precisa_reforco', 'em_aprendizagem', 'consolidada', 'dominada')),
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
    correta INTEGER NOT NULL DEFAULT 0 CHECK (correta IN (0, 1)),
    dica_nivel INTEGER NOT NULL DEFAULT 0,
    resposta_revelada INTEGER NOT NULL DEFAULT 0 CHECK (resposta_revelada IN (0, 1)),
    pontos INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS planos_missao_diaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_atividade TEXT NOT NULL,
    materia TEXT NOT NULL CHECK (materia IN ('matematica', 'portugues', 'leitura')),
    fase TEXT NOT NULL CHECK (fase IN ('diagnostico', 'adaptativa')),
    nivel_alvo INTEGER NOT NULL,
    quantidade_itens INTEGER NOT NULL,
    foco_habilidade TEXT,
    codigos_json TEXT NOT NULL DEFAULT '[]',
    composicao_json TEXT NOT NULL DEFAULT '{}',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (aluno_id, data_atividade, materia),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_eventos_desempenho_aluno
    ON eventos_desempenho (aluno_id, materia, habilidade, data_atividade);
CREATE INDEX IF NOT EXISTS idx_dominio_habilidades_aluno
    ON dominio_habilidades (aluno_id, materia, dominio);
CREATE INDEX IF NOT EXISTS idx_planos_missao_aluno_data
    ON planos_missao_diaria (aluno_id, data_atividade);
"""

HABILIDADES = {
    "matematica": [
        "numeros_quantidades", "adicao", "subtracao", "multiplicacao",
        "divisao", "problemas", "fracoes", "medidas", "dinheiro",
        "geometria", "sequencias", "raciocinio_logico",
    ],
    "portugues": [
        "ortografia", "pontuacao", "classes_palavras", "formacao_frases",
        "vocabulario", "sinonimos_antonimos", "interpretacao",
        "gramatica_aplicada", "producao_textual",
    ],
    "leitura": [
        "leitura_literal", "localizacao_informacoes", "sequencia_acontecimentos",
        "personagens", "causa_consequencia", "inferencia", "ideia_principal",
        "vocabulario_contexto", "resumo", "opiniao_fundamentada",
    ],
}

ROTULOS_HABILIDADES = {
    "numeros_quantidades": "Números e quantidades", "adicao": "Adição",
    "subtracao": "Subtração", "multiplicacao": "Multiplicação",
    "divisao": "Divisão", "problemas": "Resolução de problemas",
    "fracoes": "Frações", "medidas": "Medidas", "dinheiro": "Dinheiro",
    "geometria": "Geometria", "sequencias": "Sequências",
    "raciocinio_logico": "Raciocínio lógico", "ortografia": "Ortografia",
    "pontuacao": "Pontuação", "classes_palavras": "Classes de palavras",
    "formacao_frases": "Formação de frases", "vocabulario": "Vocabulário",
    "sinonimos_antonimos": "Sinônimos e antônimos", "interpretacao": "Interpretação",
    "gramatica_aplicada": "Gramática aplicada", "producao_textual": "Produção textual",
    "leitura_literal": "Leitura literal", "localizacao_informacoes": "Localização de informações",
    "sequencia_acontecimentos": "Sequência dos acontecimentos", "personagens": "Personagens",
    "causa_consequencia": "Causa e consequência", "inferencia": "Inferência",
    "ideia_principal": "Ideia principal", "vocabulario_contexto": "Vocabulário pelo contexto",
    "resumo": "Resumo", "opiniao_fundamentada": "Opinião fundamentada",
}

STATUS_ROTULOS = {
    "nao_avaliada": "Não avaliada", "em_diagnostico": "Em diagnóstico",
    "precisa_reforco": "Precisa de reforço", "em_aprendizagem": "Em aprendizagem",
    "consolidada": "Consolidada", "dominada": "Dominada",
}


def inicializar_motor_pedagogico(caminho_banco: str) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA)


def _normalizar(texto: str | None) -> str:
    base = unicodedata.normalize("NFKD", texto or "")
    base = "".join(c for c in base if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", base.lower())


def _ano_numero(ano_escolar: str | None) -> int:
    encontrado = re.search(r"(\d+)", ano_escolar or "")
    return max(1, min(9, int(encontrado.group(1)))) if encontrado else 1


def _faixa(idade: int) -> str:
    if idade <= 7: return "Inicial"
    if idade <= 9: return "Fundamental 1A"
    if idade <= 11: return "Fundamental 1B"
    if idade <= 13: return "Fundamental 2A"
    return "Fundamental 2B"


def _quantidade_por_concentracao(minutos: int) -> int:
    if minutos <= 10: return 6
    if minutos <= 15: return 8
    return 10


def _nivel_leitura(valor: str | None, ano: int) -> int:
    mapa = {"iniciante": 1, "basico": 2, "intermediario": 4, "avancado": 6}
    informado = mapa.get((valor or "").lower(), ano)
    return max(1, min(9, round((informado + ano) / 2)))


def _ajustes_dificuldades(dificuldades: str, materia: str, habilidade: str) -> float:
    texto = _normalizar(dificuldades)
    palavras = {
        "matematica": {
            "multiplicacao": ["multiplicacao", "tabuada"],
            "divisao": ["divisao", "dividir"],
            "problemas": ["problema", "interpretar conta"],
            "adicao": ["adicao", "somar"],
            "subtracao": ["subtracao", "diminuir"],
        },
        "portugues": {
            "ortografia": ["ortografia", "escrever"],
            "interpretacao": ["interpretacao", "entender texto"],
            "pontuacao": ["pontuacao", "virgula"],
            "producao_textual": ["redacao", "texto", "escrita"],
        },
        "leitura": {
            "resumo": ["resumo", "resumir"],
            "inferencia": ["interpretacao", "inferir"],
            "localizacao_informacoes": ["localizar", "encontrar informacao"],
        },
    }
    return -18 if any(p in texto for p in palavras.get(materia, {}).get(habilidade, [])) else 0


def garantir_perfil_pedagogico(caminho_banco: str, aluno_id: int) -> dict[str, Any]:
    anamnese = buscar_anamnese_por_aluno(caminho_banco, aluno_id)
    if not anamnese:
        raise ValueError("A anamnese precisa ser concluída antes do perfil pedagógico.")

    ano = _ano_numero(anamnese["ano_escolar"])
    idade = int(anamnese["idade"])
    quantidade = _quantidade_por_concentracao(int(anamnese["tempo_concentracao"]))
    nivel_matematica = ano
    nivel_portugues = ano
    nivel_leitura = _nivel_leitura(anamnese["nivel_leitura"], ano)
    temas = anamnese["materias_preferidas"] or anamnese["objetivo_principal"] or ""

    with conectar(caminho_banco) as conexao:
        perfil = conexao.execute(
            "SELECT * FROM perfis_pedagogicos WHERE aluno_id = ?", (aluno_id,)
        ).fetchone()
        if not perfil:
            conexao.execute(
                """
                INSERT INTO perfis_pedagogicos (
                    aluno_id, faixa_desenvolvimento, nivel_matematica,
                    nivel_portugues, nivel_leitura, quantidade_questoes, temas_preferidos
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (aluno_id, _faixa(idade), nivel_matematica, nivel_portugues,
                 nivel_leitura, quantidade, temas),
            )
        else:
            conexao.execute(
                """
                UPDATE perfis_pedagogicos
                SET faixa_desenvolvimento = ?, quantidade_questoes = ?,
                    temas_preferidos = ?, atualizado_em = CURRENT_TIMESTAMP
                WHERE aluno_id = ?
                """,
                (_faixa(idade), quantidade, temas, aluno_id),
            )

        niveis = {"matematica": nivel_matematica, "portugues": nivel_portugues, "leitura": nivel_leitura}
        for materia, habilidades in HABILIDADES.items():
            for habilidade in habilidades:
                dominio = max(10, min(70, 42 + _ajustes_dificuldades(
                    anamnese["dificuldades"], materia, habilidade
                )))
                conexao.execute(
                    """
                    INSERT INTO dominio_habilidades (
                        aluno_id, materia, habilidade, nivel, dominio, status
                    ) VALUES (?, ?, ?, ?, ?, 'em_diagnostico')
                    ON CONFLICT(aluno_id, materia, habilidade) DO UPDATE SET
                        nivel = excluded.nivel,
                        dominio = excluded.dominio,
                        status = 'em_diagnostico',
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE dominio_habilidades.total_tentativas = 0
                    """,
                    (aluno_id, materia, habilidade, niveis[materia], dominio),
                )

    return obter_perfil_pedagogico(caminho_banco, aluno_id)


def obter_perfil_pedagogico(caminho_banco: str, aluno_id: int) -> dict[str, Any]:
    with conectar(caminho_banco) as conexao:
        perfil = conexao.execute(
            "SELECT * FROM perfis_pedagogicos WHERE aluno_id = ?", (aluno_id,)
        ).fetchone()
        if not perfil:
            return {}
        dominios = conexao.execute(
            """
            SELECT materia, habilidade, nivel, dominio, status, total_tentativas,
                   acertos_primeira, dicas_utilizadas, respostas_reveladas
            FROM dominio_habilidades
            WHERE aluno_id = ?
            ORDER BY materia, dominio ASC, habilidade
            """,
            (aluno_id,),
        ).fetchall()
        dias = conexao.execute(
            "SELECT COUNT(DISTINCT data_atividade) AS total FROM eventos_desempenho WHERE aluno_id = ?",
            (aluno_id,),
        ).fetchone()["total"]

    grupos = {"matematica": [], "portugues": [], "leitura": []}
    for item in dominios:
        registro = dict(item)
        registro["rotulo"] = ROTULOS_HABILIDADES.get(registro["habilidade"], registro["habilidade"])
        registro["status_rotulo"] = STATUS_ROTULOS.get(registro["status"], registro["status"])
        registro["dominio"] = round(float(registro["dominio"]))
        grupos[registro["materia"]].append(registro)

    resultado = dict(perfil)
    resultado["dominios"] = grupos
    resultado["dias_observados"] = int(dias or 0)
    resultado["dias_restantes_diagnostico"] = max(0, int(perfil["dias_diagnostico"]) - int(dias or 0))
    resultado["fase"] = "adaptativa" if perfil["diagnostico_concluido"] else "diagnostico"
    return resultado


def _status_por_dominio(valor: float, diagnostico: bool) -> str:
    if diagnostico: return "em_diagnostico"
    if valor < 40: return "precisa_reforco"
    if valor < 70: return "em_aprendizagem"
    if valor < 88: return "consolidada"
    return "dominada"


def registrar_desempenho(
    caminho_banco: str, aluno_id: int, data_atividade: str, materia: str,
    questao: dict[str, Any], numero_tentativa: int, correta: bool,
    dica_nivel: int, resposta_revelada: bool, pontos: int,
) -> None:
    habilidade = questao.get("habilidade", "geral")
    nivel_questao = int(questao.get("nivel", 1))
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            """
            INSERT INTO eventos_desempenho (
                aluno_id, data_atividade, materia, habilidade, questao_codigo,
                nivel_questao, numero_tentativa, correta, dica_nivel,
                resposta_revelada, pontos
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (aluno_id, data_atividade, materia, habilidade, questao["id"],
             nivel_questao, numero_tentativa, int(correta), dica_nivel,
             int(resposta_revelada), pontos),
        )
        dominio = conexao.execute(
            """SELECT * FROM dominio_habilidades
               WHERE aluno_id = ? AND materia = ? AND habilidade = ?""",
            (aluno_id, materia, habilidade),
        ).fetchone()
        if not dominio:
            conexao.execute(
                """INSERT INTO dominio_habilidades
                   (aluno_id, materia, habilidade, nivel, dominio, status)
                   VALUES (?, ?, ?, ?, 40, 'em_diagnostico')""",
                (aluno_id, materia, habilidade, nivel_questao),
            )
            dominio_atual = 40.0
            nivel_atual = nivel_questao
        else:
            dominio_atual = float(dominio["dominio"])
            nivel_atual = int(dominio["nivel"])

        if correta and numero_tentativa == 1: delta = 8
        elif correta and numero_tentativa == 2: delta = 5
        elif correta: delta = 2
        elif resposta_revelada: delta = -8
        else: delta = -2
        novo_dominio = max(0, min(100, dominio_atual + delta))

        recentes = conexao.execute(
            """
            SELECT correta, numero_tentativa, resposta_revelada
            FROM eventos_desempenho
            WHERE aluno_id = ? AND materia = ? AND habilidade = ?
            ORDER BY id DESC LIMIT 8
            """,
            (aluno_id, materia, habilidade),
        ).fetchall()
        taxa = 0.0
        if recentes:
            valor = sum(1 if r["correta"] and r["numero_tentativa"] == 1 else
                        .7 if r["correta"] else 0 for r in recentes)
            taxa = valor / len(recentes)
        novo_nivel = nivel_atual
        if len(recentes) >= 5 and taxa >= .80 and novo_dominio >= 78:
            novo_nivel = min(9, nivel_atual + 1)
        elif len(recentes) >= 5 and taxa < .50 and novo_dominio < 40:
            novo_nivel = max(1, nivel_atual - 1)

        dias = conexao.execute(
            "SELECT COUNT(DISTINCT data_atividade) AS total FROM eventos_desempenho WHERE aluno_id = ?",
            (aluno_id,),
        ).fetchone()["total"]
        perfil = conexao.execute(
            "SELECT dias_diagnostico FROM perfis_pedagogicos WHERE aluno_id = ?",
            (aluno_id,),
        ).fetchone()
        diagnostico = int(dias or 0) < int(perfil["dias_diagnostico"] if perfil else 5)
        status = _status_por_dominio(novo_dominio, diagnostico)

        conexao.execute(
            """
            UPDATE dominio_habilidades
            SET nivel = ?, dominio = ?, status = ?,
                total_tentativas = total_tentativas + 1,
                acertos_primeira = acertos_primeira + ?,
                dicas_utilizadas = dicas_utilizadas + ?,
                respostas_reveladas = respostas_reveladas + ?,
                atualizado_em = CURRENT_TIMESTAMP
            WHERE aluno_id = ? AND materia = ? AND habilidade = ?
            """,
            (novo_nivel, novo_dominio, status,
             int(correta and numero_tentativa == 1), int(dica_nivel > 0),
             int(resposta_revelada), aluno_id, materia, habilidade),
        )
        if not diagnostico:
            conexao.execute(
                """UPDATE perfis_pedagogicos SET diagnostico_concluido = 1,
                   atualizado_em = CURRENT_TIMESTAMP WHERE aluno_id = ?""",
                (aluno_id,),
            )


def _composicao(quantidade: int) -> dict[str, int]:
    revisao = max(1, round(quantidade * .30))
    desafio = max(1, round(quantidade * .20))
    atual = quantidade - revisao - desafio
    return {"revisao": revisao, "atual": atual, "desafio": desafio}


def gerar_plano_missao(
    caminho_banco: str, aluno_id: int, materia: str,
    questoes: list[dict[str, Any]], data_atividade: str | None = None,
) -> dict[str, Any]:
    data_ref = data_atividade or date.today().isoformat()
    perfil = garantir_perfil_pedagogico(caminho_banco, aluno_id)
    with conectar(caminho_banco) as conexao:
        existente = conexao.execute(
            """SELECT * FROM planos_missao_diaria
               WHERE aluno_id = ? AND data_atividade = ? AND materia = ?""",
            (aluno_id, data_ref, materia),
        ).fetchone()
        if existente:
            plano = dict(existente)
            plano["codigos"] = json.loads(plano.pop("codigos_json"))
            plano["composicao"] = json.loads(plano.pop("composicao_json"))
            return plano

        nivel_alvo = int(perfil[f"nivel_{materia}"])
        quantidade = min(int(perfil["quantidade_questoes"]), len(questoes))
        dominios = perfil["dominios"].get(materia, [])
        foco = dominios[0]["habilidade"] if dominios else None
        fase = perfil["fase"]
        comp = _composicao(quantidade)

        def prioridade(q: dict[str, Any]) -> tuple:
            nivel = int(q.get("nivel", nivel_alvo))
            habilidade = q.get("habilidade")
            foco_prioridade = 0 if habilidade == foco else 1
            if fase == "diagnostico":
                distancia = abs(nivel - nivel_alvo)
                return (distancia, foco_prioridade, random.random())
            categoria = 1
            if nivel < nivel_alvo: categoria = 0
            elif nivel > nivel_alvo: categoria = 2
            ordem_categoria = {0: comp["revisao"], 1: comp["atual"], 2: comp["desafio"]}
            return (foco_prioridade, abs(nivel - nivel_alvo), -ordem_categoria[categoria], random.random())

        selecionadas = sorted(questoes, key=prioridade)[:quantidade]
        random.shuffle(selecionadas)
        codigos = [q["id"] for q in selecionadas]
        conexao.execute(
            """
            INSERT INTO planos_missao_diaria (
                aluno_id, data_atividade, materia, fase, nivel_alvo,
                quantidade_itens, foco_habilidade, codigos_json, composicao_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (aluno_id, data_ref, materia, fase, nivel_alvo, quantidade, foco,
             json.dumps(codigos), json.dumps(comp)),
        )
    return gerar_plano_missao(caminho_banco, aluno_id, materia, questoes, data_ref)


def resumo_missao_personalizada(caminho_banco: str, aluno_id: int) -> dict[str, Any]:
    perfil = garantir_perfil_pedagogico(caminho_banco, aluno_id)
    focos = {}
    for materia, dominios in perfil["dominios"].items():
        focos[materia] = dominios[0] if dominios else None
    return {
        "fase": perfil["fase"],
        "dias_observados": perfil["dias_observados"],
        "dias_restantes": perfil["dias_restantes_diagnostico"],
        "quantidade_questoes": perfil["quantidade_questoes"],
        "faixa": perfil["faixa_desenvolvimento"],
        "focos": focos,
    }
