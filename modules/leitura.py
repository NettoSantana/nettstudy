# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\leitura.py
# Data e hora do último recode: 30/07/2026 21:17 -03:00
# Motivo da alteração: adicionar histórias de nível 1 e unificar a regra do resumo por nível.

from datetime import date
from typing import Any


HISTORIAS = [
    {
        "id": "ini-01", "colecao": "Primeiras leituras", "tema": "Animais",
        "titulo": "Bia e o gato", "nivel": "iniciante",
        "vocabulario": ["gato", "leite", "feliz"],
        "paginas": [
            "Bia viu um gato no jardim.",
            "Ela colocou leite em um pote.",
            "O gato bebeu e ficou feliz.",
        ],
        "perguntas": [
            {"id":"ini-01-q1","enunciado":"Quem Bia viu?","alternativas":["Um gato","Um peixe","Um pato","Um cão"],"correta":"Um gato"},
            {"id":"ini-01-q2","enunciado":"O que Bia colocou no pote?","alternativas":["Água","Leite","Suco","Areia"],"correta":"Leite"},
            {"id":"ini-01-q3","enunciado":"Como o gato ficou?","alternativas":["Triste","Bravo","Feliz","Com sono"],"correta":"Feliz"},
        ],
        "reflexao": "Como você cuidaria de um animal?",
    },
    {
        "id": "ini-02", "colecao": "Primeiras leituras", "tema": "Escola",
        "titulo": "O lápis de Leo", "nivel": "iniciante",
        "vocabulario": ["lápis", "azul", "desenho"],
        "paginas": [
            "Leo ganhou um lápis azul.",
            "Ele desenhou uma casa.",
            "Depois, mostrou o desenho à mãe.",
        ],
        "perguntas": [
            {"id":"ini-02-q1","enunciado":"Qual era a cor do lápis?","alternativas":["Azul","Verde","Amarelo","Roxo"],"correta":"Azul"},
            {"id":"ini-02-q2","enunciado":"O que Leo desenhou?","alternativas":["Uma bola","Uma casa","Um gato","Uma flor"],"correta":"Uma casa"},
            {"id":"ini-02-q3","enunciado":"Para quem Leo mostrou o desenho?","alternativas":["Para a mãe","Para o pai","Para a professora","Para o amigo"],"correta":"Para a mãe"},
        ],
        "reflexao": "O que você gosta de desenhar?",
    },
    {
        "id": "ini-03", "colecao": "Primeiras leituras", "tema": "Natureza",
        "titulo": "A flor amarela", "nivel": "iniciante",
        "vocabulario": ["flor", "amarela", "água"],
        "paginas": [
            "Uma flor amarela nasceu no vaso.",
            "Luna colocou água na terra.",
            "A flor abriu suas pétalas.",
        ],
        "perguntas": [
            {"id":"ini-03-q1","enunciado":"Qual era a cor da flor?","alternativas":["Azul","Amarela","Branca","Roxa"],"correta":"Amarela"},
            {"id":"ini-03-q2","enunciado":"Quem colocou água na terra?","alternativas":["Luna","Bia","Leo","Davi"],"correta":"Luna"},
            {"id":"ini-03-q3","enunciado":"O que a flor abriu?","alternativas":["As folhas","As pétalas","A porta","As asas"],"correta":"As pétalas"},
        ],
        "reflexao": "O que uma planta precisa para crescer?",
    },
    {
        "id": "ini-04", "colecao": "Primeiras leituras", "tema": "Rotina",
        "titulo": "A mochila pronta", "nivel": "iniciante",
        "vocabulario": ["mochila", "caderno", "escola"],
        "paginas": [
            "Nina colocou o caderno na mochila.",
            "Depois, guardou o lápis.",
            "A mochila ficou pronta para a escola.",
        ],
        "perguntas": [
            {"id":"ini-04-q1","enunciado":"O que Nina colocou na mochila?","alternativas":["O caderno","O prato","A bola","O sapato"],"correta":"O caderno"},
            {"id":"ini-04-q2","enunciado":"O que ela guardou depois?","alternativas":["O lápis","O livro","A régua","O lanche"],"correta":"O lápis"},
            {"id":"ini-04-q3","enunciado":"Para onde Nina iria?","alternativas":["Para a escola","Para a praia","Para o mercado","Para o parque"],"correta":"Para a escola"},
        ],
        "reflexao": "O que você coloca na mochila?",
    },
    {
        "id": "ini-05", "colecao": "Primeiras leituras", "tema": "Amizade",
        "titulo": "A bola de Rui", "nivel": "iniciante",
        "vocabulario": ["bola", "amigo", "brincar"],
        "paginas": [
            "Rui levou uma bola ao parque.",
            "Ele chamou seu amigo Caio.",
            "Os dois brincaram juntos.",
        ],
        "perguntas": [
            {"id":"ini-05-q1","enunciado":"O que Rui levou?","alternativas":["Uma bola","Um livro","Um carrinho","Uma pipa"],"correta":"Uma bola"},
            {"id":"ini-05-q2","enunciado":"Quem Rui chamou?","alternativas":["Caio","Leo","Davi","Beto"],"correta":"Caio"},
            {"id":"ini-05-q3","enunciado":"O que os dois fizeram?","alternativas":["Dormiram","Brincaram","Estudaram","Comeram"],"correta":"Brincaram"},
        ],
        "reflexao": "Do que você gosta de brincar com seus amigos?",
    },
    {
        "id": "emo-01",
        "colecao": "Emoções",
        "tema": "Frustração e persistência",
        "titulo": "O castelo que caiu sete vezes",
        "nivel": "basico",
        "vocabulario": ["persistir", "equilíbrio", "frustração"],
        "paginas": [
            "Davi decidiu construir um castelo com blocos de madeira. Ele queria que a torre ficasse mais alta que sua mochila. Quando colocou a última peça, tudo caiu no tapete.",
            "Na segunda tentativa, o castelo caiu outra vez. Davi sentiu o rosto esquentar e pensou em guardar os blocos. Sua irmã sugeriu que ele observasse onde a torre começava a balançar.",
            "Davi fez uma base mais larga e tentou novamente. O castelo caiu outras vezes, mas cada queda ensinou algo. Na sétima tentativa, a torre ficou em pé. Davi percebeu que insistir não é repetir igual: é aprender e tentar melhor.",
        ],
        "perguntas": [
            {"id": "emo-01-q1", "enunciado": "Por que o castelo de Davi caía?", "alternativas": ["Os blocos estavam molhados", "A base precisava de mais equilíbrio", "A irmã derrubava", "Faltavam blocos"], "correta": "A base precisava de mais equilíbrio"},
            {"id": "emo-01-q2", "enunciado": "O que a irmã sugeriu?", "alternativas": ["Guardar os blocos", "Comprar outro brinquedo", "Observar onde a torre balançava", "Fazer uma torre menor sem tentar"], "correta": "Observar onde a torre balançava"},
            {"id": "emo-01-q3", "enunciado": "Qual é a principal ideia da história?", "alternativas": ["Errar sempre é ruim", "Persistir é aprender e tentar melhor", "Só adultos resolvem problemas", "Torres altas são perigosas"], "correta": "Persistir é aprender e tentar melhor"},
        ],
        "reflexao": "Conte uma situação em que você precisou tentar mais de uma vez.",
    },
    {
        "id": "emo-02",
        "colecao": "Emoções",
        "tema": "Medo e coragem",
        "titulo": "A apresentação de Lia",
        "nivel": "basico",
        "vocabulario": ["coragem", "plateia", "respirar"],
        "paginas": [
            "Lia conhecia toda a pesquisa sobre os planetas, mas ficou com medo quando soube que apresentaria o trabalho diante da turma. Na manhã da apresentação, suas mãos estavam frias.",
            "A professora explicou que coragem não significa ausência de medo. Lia respirou devagar, segurou seu cartão com as palavras principais e começou pela parte que mais gostava: os anéis de Saturno.",
            "No início, sua voz saiu baixa. Depois, ela olhou para o desenho do planeta e lembrou do que havia estudado. Ao terminar, Lia ainda sentia o coração acelerado, mas estava orgulhosa por ter continuado.",
        ],
        "perguntas": [
            {"id": "emo-02-q1", "enunciado": "Por que Lia estava com medo?", "alternativas": ["Não tinha feito o trabalho", "Precisava apresentar diante da turma", "Não gostava de planetas", "Tinha perdido o desenho"], "correta": "Precisava apresentar diante da turma"},
            {"id": "emo-02-q2", "enunciado": "O que ajudou Lia a começar?", "alternativas": ["Falar sobre Saturno", "Sair da sala", "Pedir que outra pessoa apresentasse", "Apagar o desenho"], "correta": "Falar sobre Saturno"},
            {"id": "emo-02-q3", "enunciado": "O que a história ensina sobre coragem?", "alternativas": ["Coragem é nunca sentir medo", "Coragem é continuar mesmo sentindo medo", "Coragem é falar muito alto", "Coragem é evitar desafios"], "correta": "Coragem é continuar mesmo sentindo medo"},
        ],
        "reflexao": "O que costuma ajudar você quando sente medo de fazer algo?",
    },
    {
        "id": "emo-03",
        "colecao": "Emoções",
        "tema": "Empatia e amizade",
        "titulo": "O banco vazio",
        "nivel": "intermediario",
        "vocabulario": ["empatia", "acolher", "perceber"],
        "paginas": [
            "Durante o recreio, Miguel percebeu que Ravi estava sentado sozinho no banco perto da quadra. Nos outros dias, Ravi jogava bola, mas naquele dia apenas olhava para o chão.",
            "Miguel pensou em chamar o amigo para brincar, porém resolveu primeiro perguntar se estava tudo bem. Ravi contou que seu cachorro estava doente e que não tinha vontade de correr.",
            "Miguel sentou ao lado dele. Não tentou inventar uma solução nem disse que a tristeza passaria rápido. Apenas ouviu. Depois de alguns minutos, Ravi agradeceu. Miguel descobriu que ajudar alguém também pode significar permanecer por perto.",
        ],
        "perguntas": [
            {"id": "emo-03-q1", "enunciado": "O que Miguel percebeu no recreio?", "alternativas": ["Ravi havia faltado", "Ravi estava sozinho e triste", "A quadra estava fechada", "O cachorro estava na escola"], "correta": "Ravi estava sozinho e triste"},
            {"id": "emo-03-q2", "enunciado": "Como Miguel ajudou Ravi?", "alternativas": ["Deu um presente", "Resolveu o problema", "Ouviu e permaneceu ao lado", "Chamou a professora imediatamente"], "correta": "Ouviu e permaneceu ao lado"},
            {"id": "emo-03-q3", "enunciado": "Qual atitude demonstra empatia?", "alternativas": ["Ignorar a tristeza", "Mandar a pessoa parar de chorar", "Tentar entender e acolher", "Mudar de assunto sempre"], "correta": "Tentar entender e acolher"},
        ],
        "reflexao": "Como você pode demonstrar que está disponível para ouvir um amigo?",
    },
    {
        "id": "din-01",
        "colecao": "Dinheiro e escolhas",
        "tema": "Querer e precisar",
        "titulo": "As três moedas de Luna",
        "nivel": "basico",
        "vocabulario": ["prioridade", "economizar", "escolha"],
        "paginas": [
            "Luna recebeu três moedas por ajudar a organizar os livros da tia. No caminho para casa, viu um adesivo brilhante e um caderno de que precisava para a escola.",
            "O adesivo custava duas moedas. O caderno custava três. Luna queria comprar o adesivo imediatamente, mas lembrou que seu caderno antigo estava quase sem páginas.",
            "Ela escolheu comprar o caderno. Não foi fácil deixar o adesivo na loja, mas Luna entendeu que escolher uma prioridade não significa que o outro desejo era ruim. Significa decidir o que é mais importante naquele momento.",
        ],
        "perguntas": [
            {"id": "din-01-q1", "enunciado": "Quantas moedas Luna recebeu?", "alternativas": ["Duas", "Três", "Quatro", "Cinco"], "correta": "Três"},
            {"id": "din-01-q2", "enunciado": "Por que ela escolheu o caderno?", "alternativas": ["Era mais bonito", "A tia mandou", "Ela precisava dele para a escola", "O adesivo havia acabado"], "correta": "Ela precisava dele para a escola"},
            {"id": "din-01-q3", "enunciado": "O que é prioridade na história?", "alternativas": ["Comprar tudo", "Escolher o mais importante naquele momento", "Nunca gastar dinheiro", "Escolher sempre o mais barato"], "correta": "Escolher o mais importante naquele momento"},
        ],
        "reflexao": "Pense em algo que você quer e algo de que precisa. Qual seria sua prioridade?",
    },
    {
        "id": "din-02",
        "colecao": "Dinheiro e escolhas",
        "tema": "Planejamento",
        "titulo": "O plano da bicicleta azul",
        "nivel": "intermediario",
        "vocabulario": ["meta", "planejamento", "acompanhar"],
        "paginas": [
            "Samuel queria comprar uma bicicleta usada que custava cento e vinte reais. Ele tinha vinte reais guardados e percebeu que ainda faltava bastante.",
            "Com a ajuda do pai, Samuel desenhou uma tabela. Toda semana, registraria quanto conseguia guardar ao ajudar em pequenas tarefas combinadas. Também decidiu não gastar todo o dinheiro que recebia em lanches.",
            "Depois de algumas semanas, Samuel ainda não tinha o valor completo, mas já conseguia ver o progresso. Ele descobriu que uma meta grande fica menos assustadora quando é dividida em passos menores e acompanhada com paciência.",
        ],
        "perguntas": [
            {"id": "din-02-q1", "enunciado": "Quanto custava a bicicleta?", "alternativas": ["20 reais", "100 reais", "120 reais", "140 reais"], "correta": "120 reais"},
            {"id": "din-02-q2", "enunciado": "Para que servia a tabela?", "alternativas": ["Desenhar bicicletas", "Registrar o dinheiro guardado", "Anotar notas escolares", "Escolher lanches"], "correta": "Registrar o dinheiro guardado"},
            {"id": "din-02-q3", "enunciado": "Qual foi a principal aprendizagem de Samuel?", "alternativas": ["Metas grandes são impossíveis", "É melhor pedir tudo aos adultos", "Dividir uma meta em passos ajuda", "Guardar dinheiro deve ser segredo"], "correta": "Dividir uma meta em passos ajuda"},
        ],
        "reflexao": "Qual meta você gostaria de dividir em pequenos passos?",
    },
    {
        "id": "din-03",
        "colecao": "Dinheiro e escolhas",
        "tema": "Preço e valor",
        "titulo": "A feira de trocas",
        "nivel": "intermediario",
        "vocabulario": ["valor", "troca", "conservar"],
        "paginas": [
            "A escola organizou uma feira de trocas. Cada aluno poderia levar livros e brinquedos bem conservados que já não usava.",
            "Nina levou um quebra-cabeça completo. Um colega ofereceu dois carrinhos pequenos. Outro ofereceu um livro de aventuras que ela desejava ler. Não havia etiquetas de preço.",
            "Nina escolheu o livro. Ela percebeu que valor não é apenas a quantidade de objetos ou o preço pago na loja. O valor também depende da utilidade, do cuidado e da importância que algo tem para cada pessoa.",
        ],
        "perguntas": [
            {"id": "din-03-q1", "enunciado": "O que Nina levou à feira?", "alternativas": ["Um livro", "Dois carrinhos", "Um quebra-cabeça", "Uma bicicleta"], "correta": "Um quebra-cabeça"},
            {"id": "din-03-q2", "enunciado": "O que ela escolheu receber?", "alternativas": ["Dinheiro", "O livro de aventuras", "Os dois carrinhos", "Outro quebra-cabeça"], "correta": "O livro de aventuras"},
            {"id": "din-03-q3", "enunciado": "Segundo a história, o valor de algo depende apenas do preço?", "alternativas": ["Sim, sempre", "Não, também depende da utilidade e importância", "Sim, quando é novo", "Não, porque nada tem valor"], "correta": "Não, também depende da utilidade e importância"},
        ],
        "reflexao": "Que objeto seu tem muito valor para você, mesmo sem ser caro?",
    },
    {
        "id": "cul-01",
        "colecao": "Cultura brasileira",
        "tema": "Música e pertencimento",
        "titulo": "O som que vinha do Pelourinho",
        "nivel": "basico",
        "vocabulario": ["ritmo", "patrimônio", "tradição"],
        "paginas": [
            "Ana caminhava com o avô pelas ruas do Pelourinho quando ouviu tambores. O som parecia conversar com as paredes coloridas e fazia muitas pessoas diminuírem o passo.",
            "O avô explicou que aqueles ritmos guardavam histórias de povos africanos e de gerações que construíram parte da cultura da Bahia. Ana percebeu que a música podia carregar memória.",
            "Ela ficou observando os músicos e tentou acompanhar a batida com as mãos. Ao voltar para casa, desenhou os instrumentos que tinha visto. Ana entendeu que conhecer a cultura de um lugar é também aprender a respeitar quem ajudou a formá-lo.",
        ],
        "perguntas": [
            {"id": "cul-01-q1", "enunciado": "Onde Ana ouviu os tambores?", "alternativas": ["Na escola", "No Pelourinho", "Na praia", "Em casa"], "correta": "No Pelourinho"},
            {"id": "cul-01-q2", "enunciado": "O que os ritmos carregavam?", "alternativas": ["Apenas barulho", "Memórias e histórias culturais", "Notícias do dia", "Regras de trânsito"], "correta": "Memórias e histórias culturais"},
            {"id": "cul-01-q3", "enunciado": "O que Ana compreendeu?", "alternativas": ["Cultura deve ficar no passado", "Conhecer a cultura ajuda a respeitar sua formação", "Somente músicos têm cultura", "Todo instrumento é igual"], "correta": "Conhecer a cultura ajuda a respeitar sua formação"},
        ],
        "reflexao": "Qual manifestação cultural existe na sua cidade ou família?",
    },
    {
        "id": "cul-02",
        "colecao": "Cultura brasileira",
        "tema": "Culinária e memória",
        "titulo": "A receita sem medida",
        "nivel": "intermediario",
        "vocabulario": ["receita", "ancestral", "memória"],
        "paginas": [
            "Bia queria aprender a fazer o bolo de aipim da bisavó. Quando perguntou as quantidades, a avó respondeu: um pouco disso, um tanto daquilo e leite até a massa ficar certa.",
            "Bia achou estranho cozinhar sem medidas exatas. A avó explicou que havia aprendido observando, repetindo e sentindo a textura. Mesmo assim, permitiu que Bia anotasse aproximações para não esquecer.",
            "Enquanto preparavam o bolo, a avó contou histórias da infância. Bia descobriu que uma receita pode guardar mais que ingredientes: pode levar lembranças, costumes e conhecimentos de uma geração para outra.",
        ],
        "perguntas": [
            {"id": "cul-02-q1", "enunciado": "Qual prato Bia queria aprender?", "alternativas": ["Acarajé", "Bolo de aipim", "Pão de queijo", "Cuscuz"], "correta": "Bolo de aipim"},
            {"id": "cul-02-q2", "enunciado": "Como a avó havia aprendido a receita?", "alternativas": ["Em um vídeo", "Observando e repetindo", "Em um livro escolar", "Comprando pronta"], "correta": "Observando e repetindo"},
            {"id": "cul-02-q3", "enunciado": "O que uma receita pode guardar além de ingredientes?", "alternativas": ["Somente preços", "Memórias e costumes", "Segredos perigosos", "Notas escolares"], "correta": "Memórias e costumes"},
        ],
        "reflexao": "Existe alguma comida que lembra sua família? Explique.",
    },
    {
        "id": "cul-03",
        "colecao": "Cultura brasileira",
        "tema": "Diversidade regional",
        "titulo": "A mala de cinco regiões",
        "nivel": "intermediario",
        "vocabulario": ["região", "diversidade", "paisagem"],
        "paginas": [
            "Para a feira cultural, a turma de Sofia criou uma mala imaginária que viajaria pelas cinco regiões do Brasil. Cada grupo colocou dentro dela uma imagem, uma palavra e uma história.",
            "A mala recebeu uma fotografia da Floresta Amazônica, um desenho do sertão, uma miniatura de viola, uma receita escrita e uma imagem dos pampas. Nenhum objeto conseguia representar sozinho toda uma região.",
            "Sofia percebeu que o Brasil era grande demais para caber em uma única descrição. As paisagens, os sotaques e os costumes mudavam, mas todos faziam parte do mesmo país.",
        ],
        "perguntas": [
            {"id": "cul-03-q1", "enunciado": "Quantas regiões a mala visitaria?", "alternativas": ["Três", "Quatro", "Cinco", "Seis"], "correta": "Cinco"},
            {"id": "cul-03-q2", "enunciado": "Por que um objeto não representava toda uma região?", "alternativas": ["Porque os objetos eram pequenos", "Porque cada região possui muita diversidade", "Porque a mala estava cheia", "Porque ninguém conhecia o Brasil"], "correta": "Porque cada região possui muita diversidade"},
            {"id": "cul-03-q3", "enunciado": "Qual conclusão Sofia teve?", "alternativas": ["Todas as regiões são iguais", "Somente uma região representa o país", "A diversidade também forma o Brasil", "Sotaques devem desaparecer"], "correta": "A diversidade também forma o Brasil"},
        ],
        "reflexao": "Qual região do Brasil você gostaria de conhecer e por quê?",
    },
    {
        "id": "evo-01",
        "colecao": "Evolução e responsabilidade",
        "tema": "Organização",
        "titulo": "A mochila que ficava para amanhã",
        "nivel": "basico",
        "vocabulario": ["rotina", "organizar", "responsabilidade"],
        "paginas": [
            "Todas as noites, Pedro dizia que arrumaria a mochila depois. Pela manhã, procurava o caderno, a garrafa e o estojo enquanto o relógio corria.",
            "Depois de esquecer uma atividade importante, Pedro decidiu testar uma rotina. Antes de brincar à noite, olharia o horário do dia seguinte e separaria os materiais.",
            "Nos primeiros dias, ele ainda precisava de um lembrete. Depois, a organização ficou mais fácil. Pedro não passou a gostar de arrumar a mochila, mas gostou de começar as manhãs sem correria.",
        ],
        "perguntas": [
            {"id": "evo-01-q1", "enunciado": "Quando Pedro costumava arrumar a mochila?", "alternativas": ["Sempre à noite", "Na escola", "Deixava para depois e procurava pela manhã", "Durante o almoço"], "correta": "Deixava para depois e procurava pela manhã"},
            {"id": "evo-01-q2", "enunciado": "Qual rotina ele criou?", "alternativas": ["Comprar material novo", "Separar os materiais na noite anterior", "Acordar mais tarde", "Levar todos os cadernos"], "correta": "Separar os materiais na noite anterior"},
            {"id": "evo-01-q3", "enunciado": "Qual benefício Pedro percebeu?", "alternativas": ["Nunca mais estudou", "As manhãs ficaram menos corridas", "A mochila ficou mais pesada", "Não precisava olhar o horário"], "correta": "As manhãs ficaram menos corridas"},
        ],
        "reflexao": "Que pequena rotina poderia facilitar seu dia?",
    },
    {
        "id": "evo-02",
        "colecao": "Evolução e responsabilidade",
        "tema": "Assumir erros",
        "titulo": "O vaso da sala",
        "nivel": "intermediario",
        "vocabulario": ["consequência", "honestidade", "reparar"],
        "paginas": [
            "Enquanto brincava com uma bola dentro de casa, Caio acertou o vaso da sala. O objeto caiu e quebrou. Por alguns segundos, ele pensou em dizer que o gato havia derrubado.",
            "Caio chamou a mãe e contou o que aconteceu. Ela ficou chateada porque a regra era brincar com bola apenas no quintal, mas agradeceu por ele ter falado a verdade.",
            "Juntos, recolheram os pedaços com cuidado. Caio usou parte de sua mesada para comprar uma pequena planta para o vaso novo. Ele aprendeu que assumir um erro não apaga a consequência, mas permite reparar o dano.",
        ],
        "perguntas": [
            {"id": "evo-02-q1", "enunciado": "Como o vaso quebrou?", "alternativas": ["O gato derrubou", "Caio acertou com a bola", "A mãe deixou cair", "O vento empurrou"], "correta": "Caio acertou com a bola"},
            {"id": "evo-02-q2", "enunciado": "Por que a mãe agradeceu?", "alternativas": ["Porque ele comprou uma bola", "Porque ele contou a verdade", "Porque o vaso era velho", "Porque o gato fugiu"], "correta": "Porque ele contou a verdade"},
            {"id": "evo-02-q3", "enunciado": "O que significa reparar um erro?", "alternativas": ["Fingir que não aconteceu", "Culpar outra pessoa", "Tentar corrigir ou diminuir o dano", "Esquecer imediatamente"], "correta": "Tentar corrigir ou diminuir o dano"},
        ],
        "reflexao": "Por que falar a verdade pode ser difícil e importante ao mesmo tempo?",
    },
    {
        "id": "evo-03",
        "colecao": "Evolução e responsabilidade",
        "tema": "Hábito de estudo",
        "titulo": "De quinze em quinze minutos",
        "nivel": "intermediario",
        "vocabulario": ["constância", "concentração", "intervalo"],
        "paginas": [
            "Marina queria melhorar em matemática, mas sempre tentava estudar tudo na véspera da prova. Depois de muito tempo sentada, ficava cansada e confundia as contas.",
            "Ela começou a estudar quinze minutos por dia. Durante esse tempo, deixava o celular longe, resolvia poucos exercícios e marcava as dúvidas. Depois, fazia um intervalo.",
            "Em algumas semanas, Marina percebeu que não precisava estudar por horas para evoluir. A constância ajudava seu cérebro a lembrar e dava tempo para corrigir dificuldades antes da prova.",
        ],
        "perguntas": [
            {"id": "evo-03-q1", "enunciado": "Como Marina estudava antes?", "alternativas": ["Pouco todos os dias", "Somente na véspera da prova", "Com amigos toda manhã", "Nunca estudava matemática"], "correta": "Somente na véspera da prova"},
            {"id": "evo-03-q2", "enunciado": "Qual nova estratégia ela adotou?", "alternativas": ["Quinze minutos por dia", "Quatro horas sem intervalo", "Somente assistir vídeos", "Copiar as respostas"], "correta": "Quinze minutos por dia"},
            {"id": "evo-03-q3", "enunciado": "Por que a constância ajudou?", "alternativas": ["Eliminou todas as provas", "Deu tempo para aprender e corrigir dúvidas", "Fez as contas desaparecerem", "Permitiu usar o celular durante o estudo"], "correta": "Deu tempo para aprender e corrigir dúvidas"},
        ],
        "reflexao": "Que atividade você poderia praticar um pouco todos os dias?",
    },
    {
        "id": "cie-01",
        "colecao": "Ciência e curiosidade",
        "tema": "Ciclo da água",
        "titulo": "A gota que voltou para a nuvem",
        "nivel": "basico",
        "vocabulario": ["evaporação", "condensação", "precipitação"],
        "paginas": [
            "Uma pequena gota descansava em uma poça quando o sol aqueceu o chão. Ela ficou leve, transformou-se em vapor e subiu pelo ar.",
            "Lá no alto, o ar estava mais frio. O vapor se juntou a outras gotinhas e formou uma nuvem. Com o tempo, a nuvem ficou pesada.",
            "A gota caiu novamente em forma de chuva e seguiu por uma calha até o jardim. Sua viagem não tinha terminado. A água circula pela natureza, mudando de lugar e de estado.",
        ],
        "perguntas": [
            {"id": "cie-01-q1", "enunciado": "O que fez a gota subir?", "alternativas": ["O vento frio", "O calor do sol", "A chuva", "A calha"], "correta": "O calor do sol"},
            {"id": "cie-01-q2", "enunciado": "O que aconteceu no ar frio?", "alternativas": ["A água desapareceu", "As gotinhas formaram uma nuvem", "A gota virou pedra", "O sol ficou mais quente"], "correta": "As gotinhas formaram uma nuvem"},
            {"id": "cie-01-q3", "enunciado": "Qual processo a história apresenta?", "alternativas": ["Ciclo da água", "Crescimento das plantas", "Formação do solo", "Movimento dos planetas"], "correta": "Ciclo da água"},
        ],
        "reflexao": "Onde você observa água mudando de estado no dia a dia?",
    },
    {
        "id": "cie-02",
        "colecao": "Ciência e curiosidade",
        "tema": "Máquinas simples",
        "titulo": "A tábua e a caixa pesada",
        "nivel": "intermediario",
        "vocabulario": ["inclinação", "força", "máquina simples"],
        "paginas": [
            "Na oficina do tio, Júlia tentou levantar uma caixa pesada para colocá-la sobre uma plataforma. Mesmo usando muita força, a caixa quase não saiu do chão.",
            "O tio apoiou uma tábua entre o chão e a plataforma. Em vez de levantar a caixa de uma vez, eles a empurraram pela superfície inclinada.",
            "O caminho ficou mais longo, mas o esforço necessário diminuiu. Júlia aprendeu que uma rampa é uma máquina simples: ela ajuda a realizar uma tarefa trocando força por distância.",
        ],
        "perguntas": [
            {"id": "cie-02-q1", "enunciado": "Qual era o problema de Júlia?", "alternativas": ["A caixa estava vazia", "Ela não conseguia levantar a caixa pesada", "A plataforma era baixa", "A tábua estava quebrada"], "correta": "Ela não conseguia levantar a caixa pesada"},
            {"id": "cie-02-q2", "enunciado": "Como eles moveram a caixa?", "alternativas": ["Usando uma rampa", "Jogando para cima", "Abrindo a caixa", "Puxando com uma bicicleta"], "correta": "Usando uma rampa"},
            {"id": "cie-02-q3", "enunciado": "O que a rampa modificou?", "alternativas": ["A caixa ficou mais leve de verdade", "O caminho aumentou e o esforço diminuiu", "A plataforma desapareceu", "A força e a distância diminuíram igualmente"], "correta": "O caminho aumentou e o esforço diminuiu"},
        ],
        "reflexao": "Onde você já viu uma rampa facilitar uma tarefa?",
    },
    {
        "id": "cie-03",
        "colecao": "Ciência e curiosidade",
        "tema": "Observação da natureza",
        "titulo": "O caderno das sombras",
        "nivel": "intermediario",
        "vocabulario": ["posição", "observar", "registro"],
        "paginas": [
            "Rafael desenhou a sombra de uma árvore às oito horas da manhã. Ao meio-dia, voltou ao mesmo lugar e percebeu que a sombra estava menor e apontava para outra direção.",
            "Ele repetiu o desenho no fim da tarde. A sombra estava longa novamente, mas do lado oposto. Rafael anotou o horário em cada página.",
            "Comparando os registros, concluiu que a sombra mudava porque a posição aparente do Sol no céu também mudava ao longo do dia. O caderno transformou uma curiosidade em uma investigação.",
        ],
        "perguntas": [
            {"id": "cie-03-q1", "enunciado": "Quando a sombra estava menor?", "alternativas": ["À noite", "Ao meio-dia", "No início da manhã", "No fim da tarde"], "correta": "Ao meio-dia"},
            {"id": "cie-03-q2", "enunciado": "O que Rafael registrou?", "alternativas": ["Somente a árvore", "A sombra e os horários", "A temperatura da água", "Os nomes dos colegas"], "correta": "A sombra e os horários"},
            {"id": "cie-03-q3", "enunciado": "Por que a sombra mudou?", "alternativas": ["A árvore caminhou", "A posição aparente do Sol mudou", "O chão girou sozinho", "Rafael apagou o desenho"], "correta": "A posição aparente do Sol mudou"},
        ],
        "reflexao": "Que fenômeno do seu dia a dia você gostaria de observar e registrar?",
    },
]


NIVEL_NUMERICO = {"iniciante": 1, "basico": 2, "intermediario": 4}

HABILIDADES_PERGUNTAS = (
    "localizacao_informacoes",
    "causa_consequencia",
    "ideia_principal",
)


def _nivel_historia(historia: dict[str, Any]) -> int:
    return NIVEL_NUMERICO.get(historia.get("nivel", "basico"), 2)



def _texto_simples(texto: str) -> str:
    import unicodedata
    base = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in base if not unicodedata.combining(c)).lower()

def _interesses_normalizados(interesses: str | None) -> set[str]:
    texto = (interesses or "").lower()
    mapa = {
        "animais": {"animal", "cachorro", "natureza"},
        "ciencia": {"ciência", "água", "máquina", "sombra"},
        "espaco": {"planeta", "saturno", "espaço"},
        "esportes": {"bola", "quadra", "futebol"},
        "dinheiro": {"moeda", "dinheiro", "troca", "bicicleta"},
        "historia": {"cultura", "brasil", "pelourinho", "região"},
        "maquinas": {"máquina", "oficina", "rampa"},
    }
    encontrados = set()
    for interesse, termos in mapa.items():
        if interesse in texto or any(termo in texto for termo in termos):
            encontrados.add(interesse)
    return encontrados

def _sentenca_evidencia(historia: dict[str, Any], resposta_correta: str) -> tuple[int, str]:
    palavras_resposta = set(
        palavra
        for palavra in resposta_correta.lower().split()
        if len(palavra) >= 4
    )

    melhor_pagina = 1
    melhor_sentenca = historia["paginas"][0]
    melhor_pontuacao = -1

    for numero_pagina, pagina in enumerate(historia["paginas"], start=1):
        sentencas = [
            sentenca.strip()
            for sentenca in pagina.replace("!", ".").replace("?", ".").split(".")
            if sentenca.strip()
        ]

        for sentenca in sentencas:
            palavras_sentenca = set(sentenca.lower().split())
            pontuacao = len(palavras_resposta & palavras_sentenca)

            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_pagina = numero_pagina
                melhor_sentenca = sentenca

    return melhor_pagina, melhor_sentenca


def enriquecer_historia(historia: dict[str, Any]) -> dict[str, Any]:
    historia_enriquecida = {
        chave: valor
        for chave, valor in historia.items()
        if chave != "perguntas"
    }
    perguntas_enriquecidas = []

    for indice, pergunta in enumerate(historia["perguntas"], start=1):
        pagina, evidencia = _sentenca_evidencia(
            historia,
            pergunta["correta"],
        )
        perguntas_enriquecidas.append(
            {
                **pergunta,
                "pagina_evidencia": pagina,
                "evidencia": evidencia,
                "dicas": [
                    f"Releia a página {pagina}.",
                    f"Procure a parte que fala sobre: {evidencia[:80]}...",
                    "Compare cada alternativa com o que realmente aconteceu no texto.",
                ],
                "explicacao": (
                    f"A resposta correta é “{pergunta['correta']}”. "
                    f"Na página {pagina}, o texto mostra: “{evidencia}”."
                ),
                "ordem_original": indice,
                "nivel": min(5, _nivel_historia(historia) + (1 if indice == 3 else 0)),
                "habilidade": HABILIDADES_PERGUNTAS[min(indice - 1, len(HABILIDADES_PERGUNTAS) - 1)],
                "tema": historia.get("tema", ""),
            }
        )

    historia_enriquecida["perguntas"] = perguntas_enriquecidas
    return historia_enriquecida


def obter_pergunta(historia: dict[str, Any], codigo: str) -> dict[str, Any] | None:
    for pergunta in historia["perguntas"]:
        if pergunta["id"] == codigo:
            return pergunta
    return None


def resposta_correta(pergunta: dict[str, Any], resposta: str) -> bool:
    return resposta == pergunta["correta"]


def obter_historia_do_dia(
    aluno_id: int,
    nivel_leitura: str | int | None = None,
    data_referencia: date | None = None,
    interesses: str | None = None,
    historias_excluidas: set[str] | None = None,
) -> dict[str, Any]:
    if isinstance(nivel_leitura, int):
        nivel_alvo = max(1, min(5, nivel_leitura))
    else:
        mapa = {"iniciante": 1, "basico": 2, "intermediario": 4, "avancado": 5}
        nivel_alvo = mapa.get((nivel_leitura or "basico").strip().lower(), 2)

    excluidas = historias_excluidas or set()
    candidatas = [
        historia
        for historia in HISTORIAS
        if _nivel_historia(historia) <= nivel_alvo + 1
        and historia["id"] not in excluidas
    ]
    if not candidatas:
        candidatas = [
            historia
            for historia in HISTORIAS
            if _nivel_historia(historia) <= nivel_alvo + 1
        ]
    if not candidatas:
        candidatas = [historia for historia in HISTORIAS if _nivel_historia(historia) == 2]

    preferidos = _interesses_normalizados(interesses)
    if preferidos:
        relacionadas = []
        for historia in candidatas:
            base = _texto_simples(f"{historia['colecao']} {historia['tema']} {historia['titulo']}")
            if any(interesse in base for interesse in preferidos):
                relacionadas.append(historia)
        if relacionadas:
            candidatas = relacionadas

    candidatas.sort(key=lambda historia: (abs(_nivel_historia(historia) - nivel_alvo), historia["id"]))
    referencia = data_referencia or date.today()
    faixa = candidatas[: max(1, min(5, len(candidatas)))]
    indice = (referencia.toordinal() + int(aluno_id)) % len(faixa)
    historia = enriquecer_historia(faixa[indice])
    historia["nivel_numerico"] = _nivel_historia(historia)
    return historia


def corrigir(
    historia: dict[str, Any],
    respostas: dict[str, str],
    resumo: str,
    nivel_aluno: int = 3,
) -> dict[str, Any]:
    detalhes = []
    acertos = 0

    for questao in historia["perguntas"]:
        resposta = respostas.get(questao["id"], "")
        correta = resposta == questao["correta"]
        acertos += int(correta)
        detalhes.append(
            {
                **questao,
                "resposta": resposta,
                "acertou": correta,
            }
        )

    resumo_limpo = resumo.strip()
    total_palavras = len(resumo_limpo.split())
    nivel_aluno = max(1, min(5, int(nivel_aluno or 3)))
    minimo_palavras = {1: 5, 2: 8, 3: 12, 4: 15, 5: 18}[nivel_aluno]
    resumo_valido = total_palavras >= minimo_palavras
    pontos = acertos * 20 + (40 if resumo_valido else 0)

    return {
        "acertos": acertos,
        "total": len(historia["perguntas"]),
        "pontos": pontos,
        "detalhes": detalhes,
        "resumo": resumo_limpo,
        "resumo_valido": resumo_valido,
        "total_palavras": total_palavras,
        "minimo_palavras": minimo_palavras,
        "nivel_aluno": nivel_aluno,
        "historia_id": historia["id"],
        "titulo": historia["titulo"],
        "colecao": historia["colecao"],
        "tema": historia["tema"],
    }
