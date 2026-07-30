# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\matematica.py
# Data e hora do último recode: 30/07/2026 15:10 -03:00
# Motivo da alteração: definir o conteúdo inicial de Matemática do 4º ano.

QUESTOES = [
    {"id": "mat-01", "enunciado": "Quanto é 247 + 136?", "alternativas": ["373", "383", "393", "403"], "correta": "383", "explicacao": "Somando unidades, dezenas e centenas: 247 + 136 = 383."},
    {"id": "mat-02", "enunciado": "Quanto é 500 - 278?", "alternativas": ["212", "222", "232", "242"], "correta": "222", "explicacao": "500 - 278 = 222."},
    {"id": "mat-03", "enunciado": "Qual é o resultado de 8 × 7?", "alternativas": ["54", "56", "63", "64"], "correta": "56", "explicacao": "Oito grupos de sete formam 56."},
    {"id": "mat-04", "enunciado": "Quanto é 72 ÷ 8?", "alternativas": ["7", "8", "9", "10"], "correta": "9", "explicacao": "Como 8 × 9 = 72, então 72 ÷ 8 = 9."},
    {"id": "mat-05", "enunciado": "Uma caixa tem 6 fileiras com 9 lápis em cada uma. Quantos lápis há ao todo?", "alternativas": ["45", "48", "54", "63"], "correta": "54", "explicacao": "São 6 grupos de 9: 6 × 9 = 54."},
    {"id": "mat-06", "enunciado": "Qual número completa a sequência: 120, 140, 160, ___?", "alternativas": ["170", "175", "180", "200"], "correta": "180", "explicacao": "A sequência aumenta de 20 em 20."},
    {"id": "mat-07", "enunciado": "Qual é o dobro de 145?", "alternativas": ["280", "290", "300", "310"], "correta": "290", "explicacao": "145 + 145 = 290."},
    {"id": "mat-08", "enunciado": "Pedro tinha 350 figurinhas e ganhou mais 85. Com quantas ficou?", "alternativas": ["425", "435", "445", "455"], "correta": "435", "explicacao": "350 + 85 = 435."},
    {"id": "mat-09", "enunciado": "Uma escola recebeu 96 livros para dividir igualmente entre 4 turmas. Quantos livros cada turma recebeu?", "alternativas": ["22", "24", "26", "28"], "correta": "24", "explicacao": "96 ÷ 4 = 24."},
    {"id": "mat-10", "enunciado": "Um passeio custa R$ 18 por criança. Quanto custará para 7 crianças?", "alternativas": ["R$ 116", "R$ 126", "R$ 136", "R$ 146"], "correta": "R$ 126", "explicacao": "18 × 7 = 126."},
]


def corrigir(respostas: dict[str, str]) -> dict:
    detalhes = []
    acertos = 0
    for questao in QUESTOES:
        resposta = respostas.get(questao["id"], "")
        correta = resposta == questao["correta"]
        acertos += int(correta)
        detalhes.append({**questao, "resposta": resposta, "acertou": correta})
    return {"acertos": acertos, "total": len(QUESTOES), "pontos": acertos * 10, "detalhes": detalhes}
