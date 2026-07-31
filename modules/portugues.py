# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\portugues.py
# Data e hora do último recode: 30/07/2026 20:56 -03:00
# Motivo da alteração: ampliar níveis 1 e 2 para cinco dias sem repetição e manter progressão adaptativa.

from typing import Any


TEXTO = "Na manhã de sábado, Lia encontrou um passarinho no quintal. Ele estava assustado e não conseguia voar. Lia chamou seu pai, colocou água em uma pequena vasilha e ficou observando de longe. Depois de descansar, o passarinho abriu as asas e voou até uma árvore."


def _q(codigo: str, nivel: int, habilidade: str, tema: str, enunciado: str,
       alternativas: list[str], correta: str, dicas: list[str], explicacao: str) -> dict[str, Any]:
    return {
        "id": codigo, "nivel": nivel, "habilidade": habilidade, "tema": tema,
        "enunciado": enunciado, "alternativas": alternativas, "correta": correta,
        "dicas": dicas, "explicacao": explicacao,
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
