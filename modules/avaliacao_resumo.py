# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\avaliacao_resumo.py
# Data e hora do último recode: 24/11/2026 20:48 -03:00
# Motivo da alteração: corrigir progressão por habilidade, diversificar tarefas e leituras e revisar propostas de escrita.

import re
import unicodedata
from collections import Counter
from typing import Any


PALAVRAS_IGNORADAS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "ela", "ele", "eles", "em", "era", "essa", "esse", "esta", "este",
    "foi", "mais", "mas", "na", "nas", "no", "nos", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "porque", "que", "se", "sem",
    "sua", "suas", "um", "uma", "umas", "uns",
}

INICIOS_COMUNS = {
    "A", "Ao", "Com", "Depois", "Durante", "Em", "Ela", "Ele", "Juntos",
    "Lá", "Na", "No", "Nos", "O", "Os", "Para", "Quando", "Sua", "Um", "Uma",
}

MARCADORES_SEQUENCIA = {
    "depois", "entao", "em seguida", "mais tarde", "no final", "primeiro",
    "por fim", "quando", "antes", "enquanto",
}


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = texto.lower()
    return re.sub(r"[^a-z0-9\s]", " ", texto)


def _palavras(texto: str) -> list[str]:
    return [
        palavra
        for palavra in _normalizar(texto).split()
        if len(palavra) >= 3 and palavra not in PALAVRAS_IGNORADAS
    ]


def _personagens(historia: dict[str, Any]) -> list[str]:
    texto = " ".join(historia["paginas"])
    nomes = re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]{2,}\b", texto)
    personagens = []
    for nome in nomes:
        if nome in INICIOS_COMUNS or nome in personagens:
            continue
        personagens.append(nome)
    return personagens[:4]


def _palavras_chave_historia(historia: dict[str, Any]) -> list[str]:
    fontes = [
        historia["titulo"],
        historia["tema"],
        *historia.get("vocabulario", []),
        *[pergunta["correta"] for pergunta in historia["perguntas"]],
    ]
    contagem = Counter(_palavras(" ".join(fontes)))
    return [palavra for palavra, _ in contagem.most_common(14)]


def _proporcao_copia(resumo: str, historia: dict[str, Any]) -> float:
    resumo_palavras = _palavras(resumo)
    texto_palavras = _palavras(" ".join(historia["paginas"]))

    if len(resumo_palavras) < 2:
        return 1.0

    pares_resumo = {
        (resumo_palavras[indice], resumo_palavras[indice + 1])
        for indice in range(len(resumo_palavras) - 1)
    }
    pares_texto = {
        (texto_palavras[indice], texto_palavras[indice + 1])
        for indice in range(len(texto_palavras) - 1)
    }

    if not pares_resumo:
        return 1.0

    return len(pares_resumo & pares_texto) / len(pares_resumo)


def _avaliar_producao(historia: dict[str, Any], texto: str, nivel_aluno: int) -> dict[str, Any]:
    proposta=historia["proposta"];tipo=proposta["tipo"]
    palavras=re.findall(r"\b[\wÀ-ÿ]+\b",texto,flags=re.UNICODE)
    normalizado=_normalizar(texto)
    frases=[f.strip() for f in re.split(r"[.!?]+",texto) if f.strip()]
    minimo=int(proposta["minimo_palavras"])
    palavras_normais=_normalizar(texto).split()
    funcionais=sum(p in PALAVRAS_IGNORADAS for p in palavras_normais)
    parece_lista=len(palavras_normais)>=20 and funcionais/max(1,len(palavras_normais))<0.08
    tokens=_palavras(texto)
    diversidade=len(set(tokens))/max(1,len(tokens))
    contexto=[p for p in proposta.get("palavras_contexto",[]) if re.search(r"\b"+re.escape(_normalizar(p))+r"\b",normalizado)]
    copia=_proporcao_copia(texto,historia)
    razoes=bool(re.search(r"\b(porque|pois|por isso|uma razao|alem disso)\b",normalizado))
    contraste=bool(re.search(r"\b(mas|porem|embora|por outro lado|enquanto|diferente)\b",normalizado))
    sequencia=bool(re.search(r"\b(depois|entao|antes|seguinte|quando|final)\b",normalizado))
    # Feedback formal e textual: não é uma validação semântica ou nota de professor.
    descricao={
      "resumo":("Seleção e sequência",len(contexto)>=2 and sequencia,"Selecione os fatos essenciais e organize o que mudou."),
      "opiniao":("Posição e justificativa",razoes and contraste,"Declare uma posição, justifique e considere uma objeção."),
      "continuacao":("Desenvolvimento",sequencia and len(frases)>=4,"Desenvolva uma nova etapa em sequência, preservando o contexto."),
      "comparacao":("Comparação",contraste and razoes,"Mostre diferenças e consequências, explicando a mudança.")}
    rotulo,atende,orientacao=descricao[tipo]
    criterios={
      "extensao":{"titulo":"Extensão","nota":2 if len(palavras)>=minimo else 0,"maximo":2,"retorno":f"Escreva pelo menos {minimo} palavras; foram contadas {len(palavras)}."},
      "contexto":{"titulo":"Relação com o texto","nota":2 if len(contexto)>=2 else 0,"maximo":2,"retorno":"Relacione sua produção a fatos específicos da leitura."},
      "proposta":{"titulo":rotulo,"nota":2 if atende else 0,"maximo":2,"retorno":orientacao},
      "organizacao":{"titulo":"Organização","nota":2 if len(frases)>=3 and not parece_lista else 0,"maximo":2,"retorno":"Organize frases completas que expliquem ações ou posições; evite listas de palavras."},
      "autoria":{"titulo":"Palavras próprias","nota":2 if copia<0.65 and diversidade>=0.45 else 0,"maximo":2,"retorno":"Evite copiar a leitura ou repetir palavras para aumentar o texto."}}
    pontos=sum(c["nota"] for c in criterios.values())
    if parece_lista:
        pontos=min(pontos,3)
    valido=len(palavras)>=minimo and len(contexto)>=2 and atende and len(frases)>=3 and not parece_lista and copia<0.65 and diversidade>=0.45
    status="concluido" if valido else "complementar" if len(palavras)>=minimo//2 else "refazer"
    return {"pontuacao":pontos,"maximo":10,"status":status,"mensagem":"Sua produção foi registrada. Releia o texto e confira se as ideias e justificativas ficaram claras." if valido else "Revise os critérios indicados e envie novamente.",
        "criterios":criterios,"pontos_fortes":[c["retorno"] for c in criterios.values() if c["nota"]==2],"melhorar":[c["retorno"] for c in criterios.values() if c["nota"]<2],
        "total_palavras":len(palavras),"minimo_palavras":minimo,"nivel_aluno":nivel_aluno,"proporcao_copia":round(copia,3),"personagens_esperados":[],"palavras_chave_encontradas":contexto,"tipo_proposta":tipo}



def avaliar_resumo(historia: dict[str, Any], resumo: str, nivel_aluno: int = 3) -> dict[str, Any]:
    resumo = (resumo or "").strip()
    if historia.get("proposta"):
        return _avaliar_producao(historia,resumo,nivel_aluno)
    palavras_resumo = _palavras(resumo)
    texto_normalizado = _normalizar(resumo)
    frases = [
        frase.strip()
        for frase in re.split(r"[.!?]+", resumo)
        if frase.strip()
    ]

    personagens = _personagens(historia)
    personagens_presentes = [
        nome
        for nome in personagens
        if _normalizar(nome) in texto_normalizado
    ]

    palavras_chave = _palavras_chave_historia(historia)
    chaves_presentes = [
        palavra
        for palavra in palavras_chave
        if palavra in palavras_resumo
    ]

    marcadores_presentes = [
        marcador
        for marcador in MARCADORES_SEQUENCIA
        if marcador in texto_normalizado
    ]

    proporcao_copia = _proporcao_copia(resumo, historia)

    criterios = {}

    if personagens and len(personagens_presentes) >= 1:
        nota_personagens = 2
        retorno_personagens = "Você identificou quem participa da história."
    elif any(pronome in texto_normalizado.split() for pronome in ("ele", "ela", "eles")):
        nota_personagens = 1
        retorno_personagens = "Você mencionou alguém da história, mas pode dizer o nome do personagem."
    else:
        nota_personagens = 0
        retorno_personagens = "Diga quem participa da história."

    if len(chaves_presentes) >= 4:
        nota_acontecimento = 2
        retorno_acontecimento = "Você explicou o acontecimento principal."
    elif len(chaves_presentes) >= 2:
        nota_acontecimento = 1
        retorno_acontecimento = "Você encontrou parte do acontecimento principal, mas faltam detalhes importantes."
    else:
        nota_acontecimento = 0
        retorno_acontecimento = "Explique o principal problema, descoberta ou mudança da história."

    if len(frases) >= 3 or len(marcadores_presentes) >= 2:
        nota_sequencia = 2
        retorno_sequencia = "As ideias estão organizadas em uma sequência compreensível."
    elif len(frases) >= 2 or marcadores_presentes:
        nota_sequencia = 1
        retorno_sequencia = "A sequência começou bem, mas pode mostrar melhor o que aconteceu depois."
    else:
        nota_sequencia = 0
        retorno_sequencia = "Organize o resumo mostrando o que aconteceu no começo, depois e no final."

    if proporcao_copia <= 0.35:
        nota_palavras_proprias = 2
        retorno_palavras_proprias = "Você contou a história principalmente com suas próprias palavras."
    elif proporcao_copia <= 0.65:
        nota_palavras_proprias = 1
        retorno_palavras_proprias = "Você usou palavras próprias, mas ainda copiou partes do texto."
    else:
        nota_palavras_proprias = 0
        retorno_palavras_proprias = "Tente contar o que entendeu sem copiar frases da história."

    if len(chaves_presentes) >= 4 and len(palavras_resumo) >= 15:
        nota_fidelidade = 2
        retorno_fidelidade = "Seu resumo permanece ligado aos fatos da história."
    elif len(chaves_presentes) >= 2:
        nota_fidelidade = 1
        retorno_fidelidade = "O resumo está ligado ao texto, mas precisa de fatos mais claros."
    else:
        nota_fidelidade = 0
        retorno_fidelidade = "Volte ao texto e use fatos que realmente aconteceram na história."

    criterios["personagens"] = {
        "titulo": "Personagens",
        "nota": nota_personagens,
        "maximo": 2,
        "retorno": retorno_personagens,
    }
    criterios["acontecimento_principal"] = {
        "titulo": "Acontecimento principal",
        "nota": nota_acontecimento,
        "maximo": 2,
        "retorno": retorno_acontecimento,
    }
    criterios["sequencia"] = {
        "titulo": "Sequência",
        "nota": nota_sequencia,
        "maximo": 2,
        "retorno": retorno_sequencia,
    }
    criterios["palavras_proprias"] = {
        "titulo": "Palavras próprias",
        "nota": nota_palavras_proprias,
        "maximo": 2,
        "retorno": retorno_palavras_proprias,
    }
    criterios["fidelidade"] = {
        "titulo": "Fidelidade ao texto",
        "nota": nota_fidelidade,
        "maximo": 2,
        "retorno": retorno_fidelidade,
    }

    pontuacao = sum(criterio["nota"] for criterio in criterios.values())

    nivel_aluno = max(1, min(5, int(nivel_aluno or 3)))
    minimo_palavras = {1: 5, 2: 8, 3: 12, 4: 15, 5: 18}[nivel_aluno]

    if len(palavras_resumo) < minimo_palavras:
        pontuacao = min(pontuacao, 3)
        status = "refazer"
        mensagem = (
            f"Seu texto ainda está curto para esta atividade. "
            f"Tente escrever pelo menos {minimo_palavras} palavras contando o que aconteceu."
        )
    elif pontuacao >= 7:
        status = "concluido"
        mensagem = "Você demonstrou boa compreensão da história."
    elif pontuacao >= 4:
        status = "complementar"
        mensagem = "Seu resumo tem uma boa base. Complete os pontos indicados abaixo."
    else:
        status = "refazer"
        mensagem = "Vamos tentar novamente com ajuda. Releia os trechos indicados e reorganize suas ideias."

    pontos_fortes = [
        criterio["retorno"]
        for criterio in criterios.values()
        if criterio["nota"] == 2
    ]
    melhorar = [
        criterio["retorno"]
        for criterio in criterios.values()
        if criterio["nota"] < 2
    ]

    return {
        "pontuacao": pontuacao,
        "maximo": 10,
        "status": status,
        "mensagem": mensagem,
        "criterios": criterios,
        "pontos_fortes": pontos_fortes,
        "melhorar": melhorar,
        "total_palavras": len(palavras_resumo),
        "minimo_palavras": minimo_palavras,
        "nivel_aluno": nivel_aluno,
        "proporcao_copia": round(proporcao_copia, 3),
        "personagens_esperados": personagens,
        "palavras_chave_encontradas": chaves_presentes,
    }

