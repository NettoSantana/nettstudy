# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\portugues.py
# Data e hora do último recode: 30/07/2026 15:29 -03:00
# Motivo da alteração: adaptar Português para uma questão por vez, repetição de erros e dicas progressivas.

TEXTO = "Na manhã de sábado, Lia encontrou um passarinho no quintal. Ele estava assustado e não conseguia voar. Lia chamou seu pai, colocou água em uma pequena vasilha e ficou observando de longe. Depois de descansar, o passarinho abriu as asas e voou até uma árvore."

QUESTOES = [
    {"id": "por-01", "enunciado": "Onde Lia encontrou o passarinho?", "alternativas": ["Na escola", "No quintal", "Na rua", "Na cozinha"], "correta": "No quintal", "dicas": ["A informação aparece logo na primeira frase.", "Procure o local citado depois da palavra passarinho.", "O local faz parte da casa e costuma ter plantas."], "explicacao": "O texto informa que Lia encontrou o passarinho no quintal."},
    {"id": "por-02", "enunciado": "Como o passarinho estava?", "alternativas": ["Assustado", "Faminto", "Cantando", "Dormindo"], "correta": "Assustado", "dicas": ["Leia novamente a segunda frase.", "A palavra descreve o sentimento do passarinho.", "Ele estava com medo e não conseguia voar."], "explicacao": "O texto diz que ele estava assustado."},
    {"id": "por-03", "enunciado": "Quem Lia chamou?", "alternativas": ["Sua mãe", "Seu irmão", "Seu pai", "Sua professora"], "correta": "Seu pai", "dicas": ["A resposta aparece depois de dizer que o passarinho não voava.", "Lia chamou um adulto da família.", "O texto usa a palavra pai."], "explicacao": "Lia chamou seu pai."},
    {"id": "por-04", "enunciado": "Qual palavra é sinônimo de 'assustado'?", "alternativas": ["Alegre", "Com medo", "Cansado", "Rápido"], "correta": "Com medo", "dicas": ["Sinônimo é uma palavra ou expressão com sentido parecido.", "Pense em como alguém se sente quando leva um susto.", "Assustado descreve alguém que sente medo."], "explicacao": "Assustado significa estar com medo."},
    {"id": "por-05", "enunciado": "Qual frase está pontuada corretamente?", "alternativas": ["Lia chamou seu pai", "Lia chamou, seu pai.", "Lia chamou seu pai.", "lia chamou seu pai."], "correta": "Lia chamou seu pai.", "dicas": ["Uma frase deve começar com letra maiúscula.", "Uma frase declarativa termina com ponto final.", "Não separe o verbo e seu complemento com vírgula nesse caso."], "explicacao": "A frase começa com letra maiúscula e termina com ponto final."},
    {"id": "por-06", "enunciado": "Qual é o plural de 'árvore'?", "alternativas": ["Árvores", "Árvoreis", "Árvoras", "Árvore"], "correta": "Árvores", "dicas": ["Plural indica mais de uma árvore.", "Na maioria dos casos, acrescentamos s ao final.", "A palavra mantém sua forma e recebe a letra s."], "explicacao": "O plural correto é árvores."},
    {"id": "por-07", "enunciado": "Na frase 'O passarinho abriu as asas', qual é o verbo?", "alternativas": ["passarinho", "abriu", "asas", "o"], "correta": "abriu", "dicas": ["O verbo indica uma ação ou estado.", "Pergunte: o que o passarinho fez?", "A ação realizada foi abrir."], "explicacao": "Abriu indica a ação realizada."},
    {"id": "por-08", "enunciado": "Qual palavra está escrita corretamente?", "alternativas": ["passarino", "pasarinho", "passarinho", "passarinhio"], "correta": "passarinho", "dicas": ["Observe a quantidade de letras s.", "A palavra vem de pássaro e usa ss.", "O final correto é nho."], "explicacao": "A grafia correta é passarinho."},
    {"id": "por-09", "enunciado": "Por que Lia observou o passarinho de longe?", "alternativas": ["Para não assustá-lo mais", "Porque estava chovendo", "Para chamar os amigos", "Porque queria ir embora"], "correta": "Para não assustá-lo mais", "dicas": ["A resposta não está escrita exatamente, mas pode ser concluída pelo cuidado de Lia.", "Pense por que alguém evita chegar perto de um animal assustado.", "Manter distância ajuda o animal a ficar mais tranquilo."], "explicacao": "Essa é a conclusão coerente com o cuidado mostrado por Lia."},
    {"id": "por-10", "enunciado": "Qual é a ideia principal do texto?", "alternativas": ["Lia cuidou de um passarinho até ele conseguir voar", "Lia plantou uma árvore", "O pai de Lia comprou uma ave", "Lia perdeu uma vasilha"], "correta": "Lia cuidou de um passarinho até ele conseguir voar", "dicas": ["A ideia principal resume o texto inteiro.", "Considere o problema, o cuidado de Lia e o final da história.", "O passarinho precisava de ajuda e depois conseguiu voar."], "explicacao": "Essa alternativa resume o começo, o cuidado e o desfecho do texto."},
]

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
