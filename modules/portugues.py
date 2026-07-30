# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\portugues.py
# Data e hora do último recode: 30/07/2026 15:10 -03:00
# Motivo da alteração: definir o conteúdo inicial de Português do 4º ano.

TEXTO = "Na manhã de sábado, Lia encontrou um passarinho no quintal. Ele estava assustado e não conseguia voar. Lia chamou seu pai, colocou água em uma pequena vasilha e ficou observando de longe. Depois de descansar, o passarinho abriu as asas e voou até uma árvore."

QUESTOES = [
    {"id": "por-01", "enunciado": "Onde Lia encontrou o passarinho?", "alternativas": ["Na escola", "No quintal", "Na rua", "Na cozinha"], "correta": "No quintal", "explicacao": "O texto informa que Lia encontrou o passarinho no quintal."},
    {"id": "por-02", "enunciado": "Como o passarinho estava?", "alternativas": ["Assustado", "Faminto", "Cantando", "Dormindo"], "correta": "Assustado", "explicacao": "O texto diz que ele estava assustado."},
    {"id": "por-03", "enunciado": "Quem Lia chamou?", "alternativas": ["Sua mãe", "Seu irmão", "Seu pai", "Sua professora"], "correta": "Seu pai", "explicacao": "Lia chamou seu pai."},
    {"id": "por-04", "enunciado": "Qual palavra é sinônimo de 'assustado'?", "alternativas": ["Alegre", "Com medo", "Cansado", "Rápido"], "correta": "Com medo", "explicacao": "Assustado significa estar com medo."},
    {"id": "por-05", "enunciado": "Qual frase está pontuada corretamente?", "alternativas": ["Lia chamou seu pai", "Lia chamou, seu pai.", "Lia chamou seu pai.", "lia chamou seu pai."], "correta": "Lia chamou seu pai.", "explicacao": "A frase começa com letra maiúscula e termina com ponto final."},
    {"id": "por-06", "enunciado": "Qual é o plural de 'árvore'?", "alternativas": ["Árvores", "Árvoreis", "Árvoras", "Árvore"], "correta": "Árvores", "explicacao": "O plural correto é árvores."},
    {"id": "por-07", "enunciado": "Na frase 'O passarinho abriu as asas', qual é o verbo?", "alternativas": ["passarinho", "abriu", "asas", "o"], "correta": "abriu", "explicacao": "Abriu indica a ação realizada."},
    {"id": "por-08", "enunciado": "Qual palavra está escrita corretamente?", "alternativas": ["passarino", "pasarinho", "passarinho", "passarinhio"], "correta": "passarinho", "explicacao": "A grafia correta é passarinho."},
    {"id": "por-09", "enunciado": "Por que Lia observou o passarinho de longe?", "alternativas": ["Para não assustá-lo mais", "Porque estava chovendo", "Para chamar os amigos", "Porque queria ir embora"], "correta": "Para não assustá-lo mais", "explicacao": "Essa é a conclusão coerente com o cuidado mostrado por Lia."},
    {"id": "por-10", "enunciado": "Qual é a ideia principal do texto?", "alternativas": ["Lia cuidou de um passarinho até ele conseguir voar", "Lia plantou uma árvore", "O pai de Lia comprou uma ave", "Lia perdeu uma vasilha"], "correta": "Lia cuidou de um passarinho até ele conseguir voar", "explicacao": "Essa alternativa resume o começo, o cuidado e o desfecho do texto."},
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
