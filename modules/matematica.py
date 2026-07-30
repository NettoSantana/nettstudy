# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\matematica.py
# Data e hora do último recode: 30/07/2026 18:11 -03:00
# Motivo da alteração: classificar questões por habilidade, nível e contexto para o motor pedagógico.

QUESTOES = [
    {"id": "mat-01", "enunciado": "Quanto é 247 + 136?", "alternativas": ["373", "383", "393", "403"], "correta": "383", "dicas": ["Some primeiro as unidades: 7 + 6.", "Depois some as dezenas, lembrando do valor que foi para a próxima casa.", "Separe a conta em centenas, dezenas e unidades."], "explicacao": "Somando unidades, dezenas e centenas: 247 + 136 = 383."},
    {"id": "mat-02", "enunciado": "Quanto é 500 - 278?", "alternativas": ["212", "222", "232", "242"], "correta": "222", "dicas": ["Pense quanto falta de 278 para chegar a 500.", "Você pode calcular 500 - 200 e depois retirar 78.", "Faça a subtração por partes: 500 - 278 = 300 - 78."], "explicacao": "500 - 278 = 222."},
    {"id": "mat-03", "enunciado": "Qual é o resultado de 8 × 7?", "alternativas": ["54", "56", "63", "64"], "correta": "56", "dicas": ["Pense em oito grupos com sete elementos.", "Use 7 × 4 = 28 e dobre o resultado.", "Some 7 oito vezes."], "explicacao": "Oito grupos de sete formam 56."},
    {"id": "mat-04", "enunciado": "Quanto é 72 ÷ 8?", "alternativas": ["7", "8", "9", "10"], "correta": "9", "dicas": ["Procure um número que multiplicado por 8 resulte em 72.", "8 × 8 é 64. Falta mais um grupo de 8.", "Conte os grupos de 8 existentes em 72."], "explicacao": "Como 8 × 9 = 72, então 72 ÷ 8 = 9."},
    {"id": "mat-05", "enunciado": "Uma caixa tem 6 fileiras com 9 lápis em cada uma. Quantos lápis há ao todo?", "alternativas": ["45", "48", "54", "63"], "correta": "54", "dicas": ["Há seis grupos iguais de nove lápis.", "Transforme o problema em uma multiplicação.", "Calcule 6 × 9."], "explicacao": "São 6 grupos de 9: 6 × 9 = 54."},
    {"id": "mat-06", "enunciado": "Qual número completa a sequência: 120, 140, 160, ___?", "alternativas": ["170", "175", "180", "200"], "correta": "180", "dicas": ["Observe quanto aumentou de 120 para 140.", "A mesma diferença aparece de 140 para 160.", "Continue somando 20."], "explicacao": "A sequência aumenta de 20 em 20."},
    {"id": "mat-07", "enunciado": "Qual é o dobro de 145?", "alternativas": ["280", "290", "300", "310"], "correta": "290", "dicas": ["Dobro significa duas vezes a mesma quantidade.", "Some 145 com 145.", "Calcule 100 + 100, 40 + 40 e 5 + 5."], "explicacao": "145 + 145 = 290."},
    {"id": "mat-08", "enunciado": "Pedro tinha 350 figurinhas e ganhou mais 85. Com quantas ficou?", "alternativas": ["425", "435", "445", "455"], "correta": "435", "dicas": ["Ele ganhou figurinhas, então a quantidade aumentou.", "Some 350 com 80 e depois acrescente 5.", "350 + 80 = 430; agora falta somar 5."], "explicacao": "350 + 85 = 435."},
    {"id": "mat-09", "enunciado": "Uma escola recebeu 96 livros para dividir igualmente entre 4 turmas. Quantos livros cada turma recebeu?", "alternativas": ["22", "24", "26", "28"], "correta": "24", "dicas": ["Dividir igualmente indica uma divisão.", "Procure um número que multiplicado por 4 resulte em 96.", "Metade de 96 é 48; metade de 48 é 24."], "explicacao": "96 ÷ 4 = 24."},
    {"id": "mat-10", "enunciado": "Um passeio custa R$ 18 por criança. Quanto custará para 7 crianças?", "alternativas": ["R$ 116", "R$ 126", "R$ 136", "R$ 146"], "correta": "R$ 126", "dicas": ["O mesmo valor será pago sete vezes.", "Calcule 18 × 7.", "Use 10 × 7 e 8 × 7, depois some os resultados."], "explicacao": "18 × 7 = 126."},
]


METADADOS = {
    "mat-01": ("adicao", 4, "numeros"), "mat-02": ("subtracao", 4, "numeros"),
    "mat-03": ("multiplicacao", 3, "tabuada"), "mat-04": ("divisao", 4, "tabuada"),
    "mat-05": ("problemas", 4, "material_escolar"), "mat-06": ("sequencias", 3, "raciocinio"),
    "mat-07": ("multiplicacao", 4, "dobro"), "mat-08": ("problemas", 4, "colecao"),
    "mat-09": ("divisao", 4, "escola"), "mat-10": ("dinheiro", 5, "passeio"),
}

for questao in QUESTOES:
    habilidade, nivel, tema = METADADOS[questao["id"]]
    questao.update(habilidade=habilidade, nivel=nivel, tema=tema)

QUESTOES_POR_ID = {questao["id"]: questao for questao in QUESTOES}


def obter_questao(codigo: str) -> dict | None:
    return QUESTOES_POR_ID.get(codigo)


def resposta_correta(questao: dict, resposta: str) -> bool:
    return resposta == questao["correta"]


def enriquecer_resultado(resultado: dict) -> dict:
    detalhes = []
    for item in resultado["detalhes"]:
        questao = obter_questao(item["id"])
        if questao:
            detalhes.append({**questao, **item})
    return {**resultado, "detalhes": detalhes}
