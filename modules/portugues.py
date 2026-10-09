# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\portugues.py
# Data e hora do último recode: 09/10/2026 15:07 -03:00
# Motivo da alteração: ampliar atividades por idade e nível, variar Matemática e evitar repetição próxima preservando sessões existentes.

from typing import Any


TEXTO = "Na manhã de sábado, Lia encontrou um passarinho no quintal. Ele estava assustado e não conseguia voar. Lia chamou seu pai, colocou água em uma pequena vasilha e ficou observando de longe. Depois de descansar, o passarinho abriu as asas e voou até uma árvore."


def _q(codigo: str, nivel: int, habilidade: str, tema: str, enunciado: str,
       alternativas: list[str], correta: str, dicas: list[str], explicacao: str,
       faixa_etaria: str | None = None, figura: str | None = None) -> dict[str, Any]:
    return {
        "id": codigo, "nivel": nivel, "habilidade": habilidade, "tema": tema,
        "enunciado": enunciado, "alternativas": alternativas, "correta": correta,
        "dicas": dicas, "explicacao": explicacao,
        "faixa_etaria": faixa_etaria, "figura": figura,
    }


QUESTOES = [
    _q("por-101",1,"ortografia","alfabetizacao","Qual palavra começa com a letra B?",["Casa","Bola","Dado","Foca"],"Bola",["Observe a primeira letra.","Procure a palavra que começa com B.","Bola começa com B."],"A palavra bola começa com a letra B."),
    _q("por-102",1,"formacao_frases","alfabetizacao","Qual opção forma uma frase completa?",["O gato.","Muito azul","Na escola","E depois"],"O gato.",["Uma frase pode comunicar uma ideia completa.","Procure quem aparece na frase.","'O gato.' apresenta uma ideia completa."],"A opção 'O gato.' forma uma frase completa."),
    _q("por-103",1,"vocabulario","animais","Qual palavra nomeia um animal?",["Mesa","Cachorro","Janela","Lápis"],"Cachorro",["Pense em um ser vivo.","Ele pode ser um animal de estimação.","Cachorro é um animal."],"Cachorro é o nome de um animal."),
    _q("por-104",1,"ortografia","silabas","Qual palavra tem duas sílabas?",["Sol","Bola","Elefante","Borboleta"],"Bola",["Bata palmas ao falar.","Bo-la.","Bola tem duas sílabas."],"A palavra bola tem duas sílabas."),
    _q("por-105",1,"localizacao_informacoes","leitura_curta","Leia: 'Ana tem uma pipa.' O que Ana tem?",["Uma bola","Uma pipa","Um livro","Uma boneca"],"Uma pipa",["A resposta está na frase.","Procure a palavra depois de 'uma'.","Ana tem uma pipa."],"A frase informa que Ana tem uma pipa."),
    _q("por-106",1,"sequencia_acontecimentos","rotina","O que costuma acontecer primeiro?",["Dormir","Acordar","Almoçar","Ir para a cama"],"Acordar",["Pense no início do dia.","Antes de fazer as atividades, levantamos.","Primeiro acordamos."],"Acordar costuma acontecer primeiro."),
    _q("por-201",2,"ortografia","grafia","Qual palavra está escrita corretamente?",["caza","casa","cassa","kasa"],"casa",["Pense na palavra usada para moradia.","Ela começa com c.","A grafia correta é casa."],"Casa é a escrita correta."),
    _q("por-202",2,"pontuacao","frase","Qual frase termina corretamente?",["Hoje está sol","Hoje está sol.","hoje está sol.","Hoje, está sol"],"Hoje está sol.",["A frase começa com letra maiúscula.","Uma afirmação termina com ponto final.","'Hoje está sol.' está completa."],"A frase correta começa com maiúscula e termina com ponto."),
    _q("por-203",2,"localizacao_informacoes","animais","Leia: 'O coelho correu para a toca.' Para onde o coelho correu?",["Para a escola","Para a toca","Para o rio","Para a árvore"],"Para a toca",["A resposta aparece no fim da frase.","Procure o local depois de 'para'.","O coelho correu para a toca."],"O coelho correu para a toca."),
    _q("por-204",2,"sinonimos_antonimos","vocabulario","Qual é o contrário de grande?",["Alto","Pequeno","Largo","Forte"],"Pequeno",["Procure uma palavra com sentido oposto.","Pense em tamanho.","Pequeno é o contrário de grande."],"Pequeno é o antônimo de grande."),
    _q("por-205",2,"formacao_frases","ordem","Organize as palavras: 'bola / a / caiu'.",["Caiu bola a.","A bola caiu.","Bola a caiu.","A caiu bola."],"A bola caiu.",["Comece com o artigo A.","Depois vem quem caiu.","A bola caiu."],"A ordem correta é 'A bola caiu.'"),
    _q("por-206",2,"vocabulario","contexto","Na frase 'A sopa está quente', como está a sopa?",["Fria","Quente","Doce","Vazia"],"Quente",["A resposta está na frase.","Procure a característica da sopa.","A sopa está quente."],"A sopa está quente."),
    _q("por-301",3,"localizacao_informacoes","animais","Onde Lia encontrou o passarinho?",["Na escola","No quintal","Na rua","Na cozinha"],"No quintal",["A informação aparece na primeira frase.","Procure o local citado.","Lia o encontrou no quintal."],"O texto informa que Lia encontrou o passarinho no quintal."),
    _q("por-302",3,"interpretacao","emocao","Como o passarinho estava?",["Assustado","Faminto","Cantando","Dormindo"],"Assustado",["Leia a segunda frase.","A palavra descreve o sentimento.","O texto diz que ele estava assustado."],"O passarinho estava assustado."),
    _q("por-303",3,"ortografia","plural","Qual é o plural de 'árvore'?",["Árvores","Árvoreis","Árvoras","Árvore"],"Árvores",["Plural indica mais de uma.","Acrescente s.","O plural é árvores."],"O plural correto é árvores."),
    _q("por-304",3,"pontuacao","frase","Qual frase está pontuada corretamente?",["Lia chamou seu pai","Lia chamou, seu pai.","Lia chamou seu pai.","lia chamou seu pai."],"Lia chamou seu pai.",["Comece com letra maiúscula.","Termine a afirmação com ponto final.","Não use vírgula entre verbo e complemento."],"A frase correta é 'Lia chamou seu pai.'"),
    _q("por-305",3,"vocabulario","sinonimo","Qual palavra tem sentido parecido com 'assustado'?",["Alegre","Com medo","Cansado","Rápido"],"Com medo",["Procure um sentido semelhante.","Pense em quem levou um susto.","Assustado significa com medo."],"Com medo é expressão de sentido semelhante."),
    _q("por-306",3,"sequencia_acontecimentos","texto","O que aconteceu depois que o passarinho descansou?",["Ele voou","Ele dormiu","Lia foi à escola","Começou a chover"],"Ele voou",["Leia o final do texto.","Observe o que aconteceu depois do descanso.","Ele abriu as asas e voou."],"Depois de descansar, o passarinho voou."),
    _q("por-401",4,"classes_palavras","verbo","Na frase 'O passarinho abriu as asas', qual é o verbo?",["passarinho","abriu","asas","o"],"abriu",["O verbo indica ação.","Pergunte o que ele fez.","A ação foi abrir."],"Abriu é o verbo da frase."),
    _q("por-402",4,"interpretacao","inferencia","Por que Lia observou o passarinho de longe?",["Para não assustá-lo mais","Porque estava chovendo","Para chamar os amigos","Porque queria ir embora"],"Para não assustá-lo mais",["A resposta precisa ser concluída.","Pense no cuidado com um animal assustado.","A distância ajudava a não aumentar o medo."],"Lia manteve distância para não assustá-lo mais."),
    _q("por-403",4,"gramatica_aplicada","pronome","Na frase 'Ele estava assustado', a palavra 'Ele' refere-se a quem?",["Ao pai","Ao passarinho","À Lia","À árvore"],"Ao passarinho",["Procure o nome citado antes.","O pronome substitui esse nome.","Ele se refere ao passarinho."],"O pronome Ele retoma o passarinho."),
    _q("por-404",4,"formacao_frases","coesao","Qual palavra completa melhor: 'O passarinho descansou, ___ conseguiu voar.'",["porque","depois","mas","nunca"],"depois",["A frase mostra sequência.","Primeiro descansou e em seguida voou.","Depois indica o que ocorreu em seguida."],"Depois completa a sequência corretamente."),
    _q("por-405",4,"interpretacao","causa_consequencia","Qual foi a consequência do descanso do passarinho?",["Ele conseguiu voar","Lia ficou triste","O pai foi embora","A água acabou"],"Ele conseguiu voar",["Consequência é o que acontece depois.","Leia a última frase.","Após descansar, ele voou."],"O descanso ajudou o passarinho a conseguir voar."),
    _q("por-406",4,"classes_palavras","adjetivo","Qual palavra caracteriza o passarinho?",["passarinho","assustado","voar","água"],"assustado",["Procure a palavra que mostra como ele estava.","Ela apresenta uma característica.","Assustado caracteriza o passarinho."],"Assustado funciona como característica do passarinho."),
    _q("por-501",5,"interpretacao","ideia_principal","Qual é a ideia principal do texto?",["Lia cuidou de um passarinho até ele conseguir voar","Lia plantou uma árvore","O pai comprou uma ave","Lia perdeu uma vasilha"],"Lia cuidou de um passarinho até ele conseguir voar",["Resuma o texto inteiro.","Considere problema, cuidado e final.","A primeira opção reúne os fatos principais."],"A ideia principal é o cuidado de Lia até a recuperação da ave."),
    _q("por-502",5,"producao_textual","resumo","Qual frase resume melhor o final?",["Lia saiu correndo.","O passarinho descansou e voltou a voar.","O pai comprou água.","A árvore caiu."],"O passarinho descansou e voltou a voar.",["Procure o acontecimento final.","O descanso trouxe uma mudança.","Ele voltou a voar."],"Essa frase resume corretamente o desfecho."),
    _q("por-503",5,"gramatica_aplicada","conectivo","Qual conectivo indica oposição?",["e","porque","mas","depois"],"mas",["Oposição mostra contraste.","A palavra liga ideias contrárias.","Mas indica oposição."],"Mas é um conectivo de oposição."),
    _q("por-504",5,"interpretacao","intencao","Que atitude de Lia demonstra cuidado?",["Observar de longe e oferecer água","Prender o passarinho","Fazer barulho","Levá-lo para a escola"],"Observar de longe e oferecer água",["Procure ações que respeitam o animal.","Ela ajudou sem aumentar o medo.","Ofereceu água e manteve distância."],"Essas ações demonstram cuidado."),
    _q("por-505",5,"vocabulario","contexto","No texto, 'vasilha' significa:",["Um recipiente","Uma árvore","Um alimento","Uma janela"],"Um recipiente",["Observe o que foi colocado nela.","Ela recebeu água.","Vasilha é um recipiente."],"Vasilha é um recipiente usado para colocar algo."),
    _q("por-506",5,"producao_textual","titulo","Qual seria outro bom título para o texto?",["O cuidado de Lia","A escola vazia","A árvore perdida","O sábado chuvoso"],"O cuidado de Lia",["O título deve representar o assunto principal.","O texto mostra ajuda a um animal.","'O cuidado de Lia' resume o tema."],"Esse título representa o assunto central do texto."),
]


QUESTOES.extend([
    _q("por-107",1,"ortografia","alfabetizacao","Qual palavra começa com a letra M?",["Pato","Mesa","Bola","Sapo"],"Mesa",["Observe a primeira letra.","Procure a palavra iniciada por M.","Mesa começa com M."],"Mesa começa com a letra M."),
    _q("por-108",1,"vocabulario","cores","Qual palavra indica uma cor?",["Azul","Mesa","Correr","Gato"],"Azul",["Pense nas cores.","É uma cor do céu.","Azul indica uma cor."],"Azul é uma cor."),
    _q("por-109",1,"ortografia","silabas","Qual palavra tem uma sílaba?",["Casa","Sol","Boneca","Janela"],"Sol",["Fale devagar.","A palavra é dita de uma vez.","Sol tem uma sílaba."],"Sol possui uma sílaba."),
    _q("por-110",1,"localizacao_informacoes","leitura_curta","Leia: 'Beto usa boné.' O que Beto usa?",["Sapato","Boné","Camisa","Relógio"],"Boné",["A resposta está na frase.","Procure a palavra depois de usa.","Beto usa boné."],"Beto usa um boné."),
    _q("por-111",1,"formacao_frases","alfabetizacao","Qual opção apresenta uma ação completa?",["A menina corre.","Muito bonito","No jardim","E a bola"],"A menina corre.",["Procure quem faz algo.","A frase comunica uma ação.","A menina corre."],"A menina corre é uma frase completa."),
    _q("por-112",1,"sequencia_acontecimentos","rotina","Depois de escovar os dentes à noite, o que costuma acontecer?",["Acordar","Dormir","Almoçar","Ir à escola"],"Dormir",["Pense na rotina da noite.","É o momento de descansar.","Depois, costumamos dormir."],"Depois da higiene noturna, costuma-se dormir."),
    _q("por-113",1,"vocabulario","objetos","Qual palavra nomeia um objeto escolar?",["Lápis","Leão","Chuva","Correr"],"Lápis",["Pense no que usamos para escrever.","É levado à escola.","Lápis é um objeto escolar."],"Lápis é um objeto escolar."),
    _q("por-114",1,"ortografia","letras","Qual palavra termina com a letra A?",["Pato","Bola","Sol","Papel"],"Bola",["Observe a última letra.","Procure a palavra terminada em A.","Bola termina com A."],"Bola termina com a letra A."),
    _q("por-115",1,"localizacao_informacoes","leitura_curta","Leia: 'A flor é amarela.' Qual é a cor da flor?",["Azul","Verde","Amarela","Roxa"],"Amarela",["A resposta aparece na frase.","Procure como a flor é descrita.","A flor é amarela."],"A flor é amarela."),
    _q("por-207",2,"ortografia","grafia","Qual palavra está escrita corretamente?",["janella","janela","ganela","janelaa"],"janela",["Pense no objeto da casa.","A palavra possui apenas um l.","Janela é a grafia correta."],"Janela está escrita corretamente."),
    _q("por-208",2,"pontuacao","pergunta","Qual frase é uma pergunta corretamente pontuada?",["Você gosta de brincar.","Você gosta de brincar?","você gosta de brincar?","Você, gosta de brincar?"],"Você gosta de brincar?",["Perguntas terminam com ponto de interrogação.","Comece com maiúscula.","A segunda opção está correta."],"A pergunta correta termina com ponto de interrogação."),
    _q("por-209",2,"localizacao_informacoes","leitura_curta","Leia: 'Rita levou o livro para a escola.' O que Rita levou?",["Uma bola","O livro","Um lanche","Uma flor"],"O livro",["A resposta está na frase.","Procure o objeto após levou.","Rita levou o livro."],"Rita levou o livro."),
    _q("por-210",2,"sinonimos_antonimos","vocabulario","Qual é o contrário de rápido?",["Devagar","Forte","Alto","Perto"],"Devagar",["Procure o sentido oposto.","Pense em velocidade.","Devagar é o contrário de rápido."],"Devagar é o antônimo de rápido."),
    _q("por-211",2,"formacao_frases","ordem","Organize: 'menino / o / sorriu'.",["Sorriu o menino.","O menino sorriu.","Menino o sorriu.","O sorriu menino."],"O menino sorriu.",["Comece com O.","Depois diga quem.","O menino sorriu."],"A ordem correta é O menino sorriu."),
    _q("por-212",2,"vocabulario","contexto","Na frase 'O gelo está frio', como está o gelo?",["Quente","Frio","Macio","Doce"],"Frio",["A resposta está na frase.","Procure a característica.","O gelo está frio."],"O gelo está frio."),
    _q("por-213",2,"sequencia_acontecimentos","rotina","Qual ação acontece antes de sair para a escola?",["Guardar o material na mochila","Voltar da escola","Jantar","Dormir à noite"],"Guardar o material na mochila",["Pense na preparação.","O material precisa estar pronto.","Primeiro guardamos o material."],"Guardar o material acontece antes de sair."),
    _q("por-214",2,"ortografia","plural","Qual é o plural de 'gato'?",["Gatoes","Gatos","Gato","Gatas"],"Gatos",["Plural indica mais de um.","Acrescente s.","O plural é gatos."],"O plural de gato é gatos."),
    _q("por-215",2,"pontuacao","frase","Qual frase começa e termina corretamente?",["maria brinca.","Maria brinca","Maria brinca.","maria brinca"],"Maria brinca.",["Comece com letra maiúscula.","Termine com ponto final.","Maria brinca. está correta."],"A frase correta é Maria brinca."),
])


# Banco novo da metodologia por idade. As questões antigas permanecem acima para
# que atividades iniciadas antes da atualização continuem podendo ser concluídas.
QUESTOES.extend([
    # 4 a 5 anos: linguagem concreta, reconhecimento visual e vocabulário oral.
    _q("por-f45-01", 1, "vocabulario_visual", "animais", "Que bicho é este?",
       ["Cachorro", "Gato", "Peixe", "Pássaro"], "Cachorro",
       ["Olhe bem para o focinho e as orelhas.", "Ele pode latir.", "É um cachorro."],
       "A figura mostra um cachorro.", "4-5", "🐶"),
    _q("por-f45-02", 1, "vocabulario_visual", "cores", "Qual é a cor desta figura?",
       ["Azul", "Amarelo", "Verde", "Roxo"], "Azul",
       ["Observe a cor do círculo.", "É a cor que lembra o céu.", "A cor é azul."],
       "O círculo é azul.", "4-5", "🔵"),
    _q("por-f45-03", 1, "vocabulario_visual", "frutas", "Qual é o nome desta fruta?",
       ["Banana", "Maçã", "Uva", "Laranja"], "Banana",
       ["Observe a fruta amarela.", "Ela é comprida e tem casca.", "É uma banana."],
       "A figura mostra uma banana.", "4-5", "🍌"),
    _q("por-f45-04", 1, "som_inicial", "alfabetizacao", "BOLA começa com qual letra?",
       ["B", "M", "P", "T"], "B",
       ["Fale BOLA devagar.", "Escute o primeiro som.", "BOLA começa com B."],
       "A palavra BOLA começa com a letra B.", "4-5", "⚽"),
    _q("por-f45-05", 1, "vocabulario_visual", "acoes", "O que a menina está fazendo?",
       ["Correndo", "Dormindo", "Comendo", "Sentando"], "Correndo",
       ["Observe as pernas da menina.", "Ela está se movimentando depressa.", "Ela está correndo."],
       "A menina está correndo.", "4-5", "🏃‍♀️"),

    # 6 a 8 anos: alfabetização guiada, frases curtas e leitura dentro de Português.
    _q("por-f68-01", 2, "ortografia", "alfabetizacao", "Qual palavra combina com a figura?",
       ["Casa", "Cama", "Capa", "Cara"], "Casa",
       ["Observe o lugar onde as pessoas moram.", "A palavra começa com CA.", "A resposta é casa."],
       "A figura representa uma casa.", "6-8", "🏠"),
    _q("por-f68-02", 2, "formacao_frases", "ordem", "Organize: 'parque / brinca / no / Bia'.",
       ["Bia brinca no parque.", "No Bia parque brinca.", "Brinca parque no Bia.", "Parque Bia no brinca."],
       "Bia brinca no parque.", ["Comece por Bia.", "Depois diga a ação.", "Bia brinca no parque."],
       "A ordem correta é 'Bia brinca no parque.'.", "6-8"),
    _q("por-f68-03", 2, "localizacao_informacoes", "leitura_guiada",
       "Leia: 'Caio levou água para o passeio.' O que Caio levou?",
       ["Água", "Uma bola", "Um livro", "Uma flor"], "Água",
       ["A resposta está na frase.", "Procure a palavra depois de levou.", "Caio levou água."],
       "Caio levou água para o passeio.", "6-8"),
    _q("por-f68-04", 2, "pontuacao", "pergunta", "Qual frase é uma pergunta?",
       ["Onde está meu lápis?", "Meu lápis é azul.", "Guardei o lápis.", "O lápis caiu."],
       "Onde está meu lápis?", ["Procure o ponto de interrogação.", "A frase quer descobrir algo.",
       "'Onde está meu lápis?' é uma pergunta."], "Perguntas terminam com ponto de interrogação.", "6-8"),
    _q("por-f68-05", 2, "sinonimos_antonimos", "vocabulario", "Qual é o contrário de feliz?",
       ["Triste", "Rápido", "Bonito", "Pequeno"], "Triste",
       ["Pense em um sentimento oposto.", "É como alguém pode ficar quando algo ruim acontece.",
       "Triste é o contrário de feliz."], "Triste é o antônimo de feliz.", "6-8"),

    # 9 a 11 anos: consolidação gramatical, vocabulário e coesão.
    _q("por-f911-01", 3, "ortografia", "grafia", "Qual palavra está escrita corretamente?",
       ["Exceção", "Excessão", "Eceção", "Exessão"], "Exceção",
       ["A palavra começa com EX.", "O som central é escrito com Ç.", "A grafia correta é exceção."],
       "Exceção é a grafia correta.", "9-11"),
    _q("por-f911-02", 3, "classes_palavras", "verbo", "Na frase 'Os alunos organizaram a feira', qual é o verbo?",
       ["alunos", "organizaram", "feira", "os"], "organizaram",
       ["O verbo indica a ação.", "Pergunte o que os alunos fizeram.", "A ação foi organizar."],
       "Organizaram é o verbo da frase.", "9-11"),
    _q("por-f911-03", 3, "pontuacao", "dialogo", "Qual opção apresenta a fala corretamente?",
       ["Lia disse: — Vamos começar!", "Lia disse — vamos começar", "lia disse: Vamos começar.", "Lia, disse vamos começar!"],
       "Lia disse: — Vamos começar!", ["A fala é anunciada por dois-pontos.", "O travessão marca o início da fala.",
       "A primeira opção usa os sinais corretamente."], "Os dois-pontos anunciam e o travessão inicia a fala.", "9-11"),
    _q("por-f911-04", 3, "coesao", "conectivos", "Complete: 'Estudou com atenção, ___ resolveu o desafio.'",
       ["por isso", "embora", "porém", "enquanto"], "por isso",
       ["A segunda ação é resultado da primeira.", "Procure um conectivo de consequência.", "Por isso indica consequência."],
       "Por isso conecta a causa ao resultado.", "9-11"),
    _q("por-f911-05", 3, "vocabulario", "contexto", "Na frase 'A equipe agiu com cautela', o que significa cautela?",
       ["Cuidado", "Pressa", "Barulho", "Alegria"], "Cuidado",
       ["Observe como a equipe agiu.", "Pense em evitar riscos.", "Cautela significa cuidado."],
       "Cautela significa agir com cuidado.", "9-11"),

    # 12 a 13 anos: análise linguística e argumentação em contexto.
    _q("por-f1213-01", 5, "concordancia", "gramatica_aplicada", "Qual frase apresenta concordância correta?",
       ["As pesquisas foram concluídas.", "As pesquisa foi concluída.", "A pesquisas foram concluída.", "As pesquisas foi concluído."],
       "As pesquisas foram concluídas.", ["Observe o plural do sujeito.", "Verbo e adjetivo devem acompanhar o plural.",
       "Pesquisas, foram e concluídas estão no plural."], "A primeira frase mantém a concordância no plural.", "12-13"),
    _q("por-f1213-02", 5, "coesao", "conectivos", "Qual conectivo completa uma ideia de contraste? 'O plano era difícil, ___ a equipe não desistiu.'",
       ["mas", "porque", "portanto", "quando"], "mas",
       ["As duas ideias se opõem.", "Procure um conectivo adversativo.", "Mas expressa contraste."],
       "Mas estabelece contraste entre dificuldade e persistência.", "12-13"),
    _q("por-f1213-03", 5, "interpretacao", "argumentacao",
       "Leia: 'A escola ampliou a biblioteca porque o número de leitores cresceu.' Qual relação aparece?",
       ["Causa e consequência", "Comparação", "Oposição", "Enumeração"], "Causa e consequência",
       ["Observe a palavra porque.", "O crescimento motivou uma ação.", "Há uma causa e sua consequência."],
       "O aumento de leitores é a causa da ampliação da biblioteca.", "12-13"),
    _q("por-f1213-04", 5, "vocabulario", "linguagem_formal", "Qual expressão é mais adequada a um texto formal?",
       ["Os resultados demonstram avanço.", "Os resultados tão bem legais.", "Deu tudo supercerto.", "A parada melhorou muito."],
       "Os resultados demonstram avanço.", ["Textos formais evitam gírias.", "Procure precisão e impessoalidade.",
       "A primeira opção usa registro formal."], "A primeira frase é adequada ao registro formal.", "12-13"),
    _q("por-f1213-05", 5, "pontuacao", "argumentacao", "Qual frase usa a vírgula corretamente?",
       ["Se houver tempo, revisaremos o projeto.", "Se houver, tempo revisaremos o projeto.", "Se houver tempo revisaremos, o projeto.", "Se, houver tempo revisaremos o projeto."],
       "Se houver tempo, revisaremos o projeto.", ["A oração inicial indica uma condição.", "Separe a condição da ação principal.",
       "A vírgula vem depois de tempo."], "A vírgula separa a oração condicional antecipada.", "12-13"),
])

QUESTOES_COM_TEXTO = {
    "por-301", "por-302", "por-303", "por-304", "por-305", "por-306",
    "por-401", "por-402", "por-403", "por-404", "por-405", "por-406",
    "por-501", "por-502", "por-504", "por-505", "por-506",
}

for questao in QUESTOES:
    questao["usa_texto"] = questao["id"] in QUESTOES_COM_TEXTO


# Situações curtas com fatos verificáveis e perguntas de habilidades diferentes.
_CENARIOS_VARIADOS = [('levou', 'um livro', 'biblioteca', 'ler uma história'), ('levou', 'uma bola', 'quadra', 'jogar com os colegas'), ('levou', 'uma garrafa', 'parque', 'beber água'), ('levou', 'um caderno', 'escola', 'anotar a atividade'), ('levou', 'uma cesta', 'horta', 'colher verduras'), ('levou', 'uma toalha', 'praia', 'se secar'), ('levou', 'uma lanterna', 'acampamento', 'iluminar o caminho'), ('levou', 'um mapa', 'trilha', 'encontrar o caminho'), ('levou', 'um regador', 'jardim', 'regar as plantas'), ('levou', 'uma sacola', 'mercado', 'carregar as compras'), ('levou', 'um pincel', 'oficina de arte', 'pintar um quadro'), ('levou', 'um violão', 'aula de música', 'tocar uma canção'), ('levou', 'um capacete', 'pista', 'andar de bicicleta com proteção'), ('levou', 'um casaco', 'passeio', 'se proteger do frio'), ('levou', 'um ingresso', 'teatro', 'assistir à peça'), ('levou', 'uma lupa', 'laboratório', 'observar detalhes'), ('levou', 'um envelope', 'correio', 'enviar uma carta'), ('levou', 'uma caixa', 'feira', 'guardar os produtos'), ('levou', 'uma câmera', 'museu', 'registrar a visita permitida'), ('levou', 'um pote', 'cozinha', 'guardar os biscoitos'), ('levou', 'uma fita', 'sala', 'medir a mesa'), ('levou', 'um apito', 'campo', 'marcar o início do jogo'), ('levou', 'um prato', 'refeitório', 'servir a comida'), ('levou', 'uma pá', 'quintal', 'plantar uma muda'), ('levou', 'um lápis', 'aula de desenho', 'desenhar uma paisagem'), ('levou', 'um boné', 'praça', 'se proteger do sol'), ('levou', 'uma moeda', 'cantina', 'pagar o lanche'), ('levou', 'um relógio', 'treino', 'acompanhar o tempo'), ('levou', 'uma tesoura', 'aula de artes', 'recortar papel'), ('levou', 'uma mochila', 'viagem', 'transportar seus pertences')]
_NOMES_VARIADOS = ['Bia', 'Caio', 'Lia', 'Davi', 'Rita', 'Nina', 'Leo', 'Ana', 'Ivo', 'Luana', 'Pedro', 'Sofia']
for faixa in ("4-5", "6-8", "9-11", "12-13"):
    for indice, (acao, objeto, lugar, finalidade) in enumerate(_CENARIOS_VARIADOS):
        for pessoa, nome in enumerate(_NOMES_VARIADOS):
            nivel = 1 + (indice + pessoa) % 5
            texto = f"{nome} {acao} {objeto} para {lugar}. O objetivo era {finalidade}."
            perguntas = [
                ("localizacao_informacoes", f"Quem {acao} {objeto}?", nome,
                 [outro for outro in _NOMES_VARIADOS if outro != nome][:3]),
                ("localizacao_informacoes", f"O que {nome} levou?", objeto,
                 [c[1] for c in _CENARIOS_VARIADOS if c[1] != objeto][:3]),
                ("localizacao_informacoes", f"Para onde {nome} levou {objeto}?", lugar,
                 [c[2] for c in _CENARIOS_VARIADOS if c[2] != lugar][:3]),
            ]
            if faixa != "4-5" and nivel >= 2:
                perguntas.append(("interpretacao", f"Para que {nome} levou {objeto}?", finalidade,
                    [c[3] for c in _CENARIOS_VARIADOS if c[3] != finalidade][:3]))
            if faixa in {"9-11", "12-13"} and nivel >= 3:
                perguntas.append(("classes_palavras", "Qual palavra do texto indica a ação realizada?", acao,
                                  [nome, objeto, lugar]))
            for numero, (habilidade, pergunta, correta, erradas) in enumerate(perguntas):
                alternativas = [correta] + erradas
                giro = (indice+pessoa+numero) % len(alternativas)
                alternativas = alternativas[giro:] + alternativas[:giro]
                codigo = f"por-v2-{faixa}-{indice}-{pessoa}-{numero}"
                QUESTOES.append(_q(codigo, nivel, habilidade, "cotidiano",
                    f"Leia: {texto}\n{pergunta}" if faixa != "4-5" else f"Ouça: {texto}\n{pergunta}",
                    alternativas, correta, ["Retome a situação apresentada.",
                    "Procure a pessoa, o objeto, o lugar ou a ação perguntada.",
                    f"A resposta é {correta}."], f"Na situação: {texto} A resposta é {correta}.", faixa))



# Vocabulário visual para a faixa inicial.
QUESTOES.append(_q("por-v2-visual-0", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Cachorro', 'Gato', 'Peixe', 'Pássaro'], 'Cachorro', ["Observe a figura.", "Diga o nome em voz alta.", 'Cachorro'], 'A figura mostra: Cachorro.', "4-5", '🐶'))
QUESTOES.append(_q("por-v2-visual-1", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Gato', 'Peixe', 'Pássaro', 'Cavalo'], 'Gato', ["Observe a figura.", "Diga o nome em voz alta.", 'Gato'], 'A figura mostra: Gato.', "4-5", '🐱'))
QUESTOES.append(_q("por-v2-visual-2", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Peixe', 'Pássaro', 'Cavalo', 'Vaca'], 'Peixe', ["Observe a figura.", "Diga o nome em voz alta.", 'Peixe'], 'A figura mostra: Peixe.', "4-5", '🐟'))
QUESTOES.append(_q("por-v2-visual-3", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Pássaro', 'Cavalo', 'Vaca', 'Porco'], 'Pássaro', ["Observe a figura.", "Diga o nome em voz alta.", 'Pássaro'], 'A figura mostra: Pássaro.', "4-5", '🐦'))
QUESTOES.append(_q("por-v2-visual-4", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Cavalo', 'Vaca', 'Porco', 'Sapo'], 'Cavalo', ["Observe a figura.", "Diga o nome em voz alta.", 'Cavalo'], 'A figura mostra: Cavalo.', "4-5", '🐴'))
QUESTOES.append(_q("por-v2-visual-5", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Vaca', 'Porco', 'Sapo', 'Borboleta'], 'Vaca', ["Observe a figura.", "Diga o nome em voz alta.", 'Vaca'], 'A figura mostra: Vaca.', "4-5", '🐮'))
QUESTOES.append(_q("por-v2-visual-6", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Porco', 'Sapo', 'Borboleta', 'Tartaruga'], 'Porco', ["Observe a figura.", "Diga o nome em voz alta.", 'Porco'], 'A figura mostra: Porco.', "4-5", '🐷'))
QUESTOES.append(_q("por-v2-visual-7", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Sapo', 'Borboleta', 'Tartaruga', 'Coelho'], 'Sapo', ["Observe a figura.", "Diga o nome em voz alta.", 'Sapo'], 'A figura mostra: Sapo.', "4-5", '🐸'))
QUESTOES.append(_q("por-v2-visual-8", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Borboleta', 'Tartaruga', 'Coelho', 'Elefante'], 'Borboleta', ["Observe a figura.", "Diga o nome em voz alta.", 'Borboleta'], 'A figura mostra: Borboleta.', "4-5", '🦋'))
QUESTOES.append(_q("por-v2-visual-9", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Tartaruga', 'Coelho', 'Elefante', 'Maçã'], 'Tartaruga', ["Observe a figura.", "Diga o nome em voz alta.", 'Tartaruga'], 'A figura mostra: Tartaruga.', "4-5", '🐢'))
QUESTOES.append(_q("por-v2-visual-10", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Coelho', 'Elefante', 'Maçã', 'Banana'], 'Coelho', ["Observe a figura.", "Diga o nome em voz alta.", 'Coelho'], 'A figura mostra: Coelho.', "4-5", '🐰'))
QUESTOES.append(_q("por-v2-visual-11", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Elefante', 'Maçã', 'Banana', 'Uva'], 'Elefante', ["Observe a figura.", "Diga o nome em voz alta.", 'Elefante'], 'A figura mostra: Elefante.', "4-5", '🐘'))
QUESTOES.append(_q("por-v2-visual-12", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Maçã', 'Banana', 'Uva', 'Morango'], 'Maçã', ["Observe a figura.", "Diga o nome em voz alta.", 'Maçã'], 'A figura mostra: Maçã.', "4-5", '🍎'))
QUESTOES.append(_q("por-v2-visual-13", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Banana', 'Uva', 'Morango', 'Laranja'], 'Banana', ["Observe a figura.", "Diga o nome em voz alta.", 'Banana'], 'A figura mostra: Banana.', "4-5", '🍌'))
QUESTOES.append(_q("por-v2-visual-14", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Uva', 'Morango', 'Laranja', 'Abacaxi'], 'Uva', ["Observe a figura.", "Diga o nome em voz alta.", 'Uva'], 'A figura mostra: Uva.', "4-5", '🍇'))
QUESTOES.append(_q("por-v2-visual-15", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Morango', 'Laranja', 'Abacaxi', 'Melancia'], 'Morango', ["Observe a figura.", "Diga o nome em voz alta.", 'Morango'], 'A figura mostra: Morango.', "4-5", '🍓'))
QUESTOES.append(_q("por-v2-visual-16", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Laranja', 'Abacaxi', 'Melancia', 'Pera'], 'Laranja', ["Observe a figura.", "Diga o nome em voz alta.", 'Laranja'], 'A figura mostra: Laranja.', "4-5", '🍊'))
QUESTOES.append(_q("por-v2-visual-17", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Abacaxi', 'Melancia', 'Pera', 'Carro'], 'Abacaxi', ["Observe a figura.", "Diga o nome em voz alta.", 'Abacaxi'], 'A figura mostra: Abacaxi.', "4-5", '🍍'))
QUESTOES.append(_q("por-v2-visual-18", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Melancia', 'Pera', 'Carro', 'Ônibus'], 'Melancia', ["Observe a figura.", "Diga o nome em voz alta.", 'Melancia'], 'A figura mostra: Melancia.', "4-5", '🍉'))
QUESTOES.append(_q("por-v2-visual-19", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Pera', 'Carro', 'Ônibus', 'Bicicleta'], 'Pera', ["Observe a figura.", "Diga o nome em voz alta.", 'Pera'], 'A figura mostra: Pera.', "4-5", '🍐'))
QUESTOES.append(_q("por-v2-visual-20", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Carro', 'Cachorro', 'Gato', 'Peixe'], 'Carro', ["Observe a figura.", "Diga o nome em voz alta.", 'Carro'], 'A figura mostra: Carro.', "4-5", '🚗'))
QUESTOES.append(_q("por-v2-visual-21", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Ônibus', 'Gato', 'Peixe', 'Pássaro'], 'Ônibus', ["Observe a figura.", "Diga o nome em voz alta.", 'Ônibus'], 'A figura mostra: Ônibus.', "4-5", '🚌'))
QUESTOES.append(_q("por-v2-visual-22", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Bicicleta', 'Peixe', 'Pássaro', 'Cavalo'], 'Bicicleta', ["Observe a figura.", "Diga o nome em voz alta.", 'Bicicleta'], 'A figura mostra: Bicicleta.', "4-5", '🚲'))
QUESTOES.append(_q("por-v2-visual-23", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Avião', 'Pássaro', 'Cavalo', 'Vaca'], 'Avião', ["Observe a figura.", "Diga o nome em voz alta.", 'Avião'], 'A figura mostra: Avião.', "4-5", '✈️'))
QUESTOES.append(_q("por-v2-visual-24", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Barco', 'Cavalo', 'Vaca', 'Porco'], 'Barco', ["Observe a figura.", "Diga o nome em voz alta.", 'Barco'], 'A figura mostra: Barco.', "4-5", '🚤'))
QUESTOES.append(_q("por-v2-visual-25", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Trem', 'Vaca', 'Porco', 'Sapo'], 'Trem', ["Observe a figura.", "Diga o nome em voz alta.", 'Trem'], 'A figura mostra: Trem.', "4-5", '🚂'))
QUESTOES.append(_q("por-v2-visual-26", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Bola', 'Porco', 'Sapo', 'Borboleta'], 'Bola', ["Observe a figura.", "Diga o nome em voz alta.", 'Bola'], 'A figura mostra: Bola.', "4-5", '⚽'))
QUESTOES.append(_q("por-v2-visual-27", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Livros', 'Sapo', 'Borboleta', 'Tartaruga'], 'Livros', ["Observe a figura.", "Diga o nome em voz alta.", 'Livros'], 'A figura mostra: Livros.', "4-5", '📚'))
QUESTOES.append(_q("por-v2-visual-28", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Lápis', 'Borboleta', 'Tartaruga', 'Coelho'], 'Lápis', ["Observe a figura.", "Diga o nome em voz alta.", 'Lápis'], 'A figura mostra: Lápis.', "4-5", '✏️'))
QUESTOES.append(_q("por-v2-visual-29", 1, "vocabulario_visual", "figuras", "Qual é o nome desta figura?", ['Violão', 'Tartaruga', 'Coelho', 'Elefante'], 'Violão', ["Observe a figura.", "Diga o nome em voz alta.", 'Violão'], 'A figura mostra: Violão.', "4-5", '🎸'))



# Vocabulário e pontuação complementam as perguntas de localização.
_PARES_OPOSTOS = [('feliz', 'triste'), ('alto', 'baixo'), ('grande', 'pequeno'), ('quente', 'frio'), ('claro', 'escuro'), ('perto', 'longe'), ('cheio', 'vazio'), ('rápido', 'lento'), ('aberto', 'fechado'), ('novo', 'velho'), ('forte', 'fraco'), ('seco', 'molhado'), ('leve', 'pesado'), ('largo', 'estreito'), ('limpo', 'sujo'), ('comprido', 'curto'), ('cedo', 'tarde'), ('entrar', 'sair'), ('subir', 'descer'), ('começar', 'terminar')]
for faixa in ("6-8", "9-11", "12-13"):
    for indice, (palavra, oposto) in enumerate(_PARES_OPOSTOS):
        alternativas = [oposto] + [par[1] for par in _PARES_OPOSTOS if par[1] != oposto][:3]
        giro = indice % 4
        alternativas = alternativas[giro:] + alternativas[:giro]
        QUESTOES.append(_q(f"por-v2-oposto-{faixa}-{indice}", 2, "sinonimos_antonimos", "opostos",
            f"Qual é o contrário de {palavra}?", alternativas, oposto,
            ["Procure uma ideia oposta.", "Compare o sentido das palavras.", f"O contrário é {oposto}."],
            f"{palavra.capitalize()} e {oposto} têm sentidos opostos.", faixa))
    for indice, nome in enumerate(_NOMES_VARIADOS):
        for numero, (_, objeto, lugar, _) in enumerate(_CENARIOS_VARIADOS):
            correta = f"{nome} levou {objeto} para {lugar}."
            alternativas = [correta, correta[:-1], correta[0].lower()+correta[1:], correta.replace(" levou ", ", levou ")]
            giro = (indice+numero) % 4
            alternativas = alternativas[giro:] + alternativas[:giro]
            QUESTOES.append(_q(f"por-v2-pontuacao-{faixa}-{indice}-{numero}", 2, "pontuacao", "frases",
                "Qual frase começa com maiúscula, termina com ponto e não separa quem fez a ação do verbo?",
                alternativas, correta, ["Veja o início e o fim da frase.", "Não separe o nome do verbo por vírgula.", correta],
                "A frase começa com maiúscula, termina com ponto e mantém o nome junto ao verbo.", faixa))

QUESTOES_POR_ID = {questao["id"]: questao for questao in QUESTOES}


def obter_questao(codigo: str) -> dict[str, Any] | None:
    return QUESTOES_POR_ID.get(codigo)


def resposta_correta(questao: dict[str, Any], resposta: str) -> bool:
    return resposta == questao["correta"]


def enriquecer_resultado(resultado: dict[str, Any]) -> dict[str, Any]:
    detalhes = []
    for item in resultado["detalhes"]:
        questao = obter_questao(item["id"])
        if questao:
            detalhes.append({**questao, **item})
    return {**resultado, "detalhes": detalhes}
