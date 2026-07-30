# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\avaliacao_resumo.py
# Data e hora do último recode: 30/07/2026 17:19 -03:00
# Motivo da alteração: avaliar resumos por rubrica de compreensão, com retorno orientativo e estrutura preparada para IA.

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


def avaliar_resumo(historia: dict[str, Any], resumo: str) -> dict[str, Any]:
    resumo = (resumo or "").strip()
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

    if len(palavras_resumo) < 15:
        pontuacao = min(pontuacao, 3)
        status = "refazer"
        mensagem = "Seu texto ainda está muito curto. Releia a história e conte com mais detalhes."
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
        "proporcao_copia": round(proporcao_copia, 3),
        "personagens_esperados": personagens,
        "palavras_chave_encontradas": chaves_presentes,
    }
