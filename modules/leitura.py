# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\leitura.py
# Data e hora do último recode: 30/07/2026 15:10 -03:00
# Motivo da alteração: definir a primeira leitura autoral do NettStudy.

TITULO = "O mapa da árvore antiga"
PAGINAS = [
    "Theo gostava de explorar o quintal da avó. Perto do muro havia uma árvore muito antiga, com raízes grossas e galhos que faziam sombra sobre o banco de madeira. Em uma tarde, ele percebeu uma pequena caixa escondida entre duas raízes.",
    "Dentro da caixa havia um papel amarelado com desenhos do quintal. Uma linha pontilhada começava na árvore, passava pelo canteiro de flores e terminava perto de uma pedra redonda. Theo chamou a avó e perguntou se aquele papel era um mapa.",
    "A avó sorriu e contou que tinha desenhado o mapa quando era criança. Debaixo da pedra não havia ouro, mas uma lata com fotografias, cartas e lembranças da família. Theo entendeu que um tesouro também pode ser feito de histórias importantes.",
]
PERGUNTAS = [
    {"id": "lei-01", "enunciado": "Onde Theo encontrou a caixa?", "alternativas": ["No canteiro", "Entre as raízes da árvore", "Dentro da casa", "Atrás do muro"], "correta": "Entre as raízes da árvore"},
    {"id": "lei-02", "enunciado": "Quem havia desenhado o mapa?", "alternativas": ["Theo", "O avô", "A avó", "Um vizinho"], "correta": "A avó"},
    {"id": "lei-03", "enunciado": "Qual foi a principal descoberta de Theo?", "alternativas": ["Todo tesouro precisa ter ouro", "Histórias e lembranças também podem ser tesouros", "A árvore era perigosa", "O mapa estava errado"], "correta": "Histórias e lembranças também podem ser tesouros"},
]


def corrigir(respostas: dict[str, str], resumo: str) -> dict:
    detalhes = []
    acertos = 0
    for questao in PERGUNTAS:
        resposta = respostas.get(questao["id"], "")
        correta = resposta == questao["correta"]
        acertos += int(correta)
        detalhes.append({**questao, "resposta": resposta, "acertou": correta})
    resumo_limpo = resumo.strip()
    resumo_valido = len(resumo_limpo.split()) >= 15
    pontos = acertos * 20 + (40 if resumo_valido else 0)
    return {"acertos": acertos, "total": len(PERGUNTAS), "pontos": pontos, "detalhes": detalhes, "resumo": resumo_limpo, "resumo_valido": resumo_valido}
