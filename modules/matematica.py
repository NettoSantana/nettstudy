# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\matematica.py
# Data e hora do último recode: 22/08/2026 01:23 -03:00
# Motivo da alteração: organizar cinco atividades de Matemática por faixa etária, com abordagem visual para crianças de 4 a 5 anos.

from typing import Any


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
    _q("mat-101",1,"numeros_quantidades","numeros","Qual número vem depois de 8?",["7","9","10","18"],"9",["Conte a partir do 8.","Depois de 8 vem o próximo número.","8, 9."],"O número que vem depois de 8 é 9."),
    _q("mat-102",1,"numeros_quantidades","numeros","Qual é o maior número?",["4","7","2","5"],"7",["Compare as quantidades.","Procure o número mais distante do zero.","7 é maior que 5, 4 e 2."],"O maior número é 7."),
    _q("mat-103",1,"adicao","brinquedos","Lia tinha 3 bolas e ganhou mais 2. Com quantas ficou?",["4","5","6","7"],"5",["Ela ganhou, então devemos juntar.","Conte 3 e depois mais 2.","3 + 2 = 5."],"Três mais dois é igual a cinco."),
    _q("mat-104",1,"subtracao","frutas","Havia 8 maçãs. Duas foram comidas. Quantas sobraram?",["5","6","7","10"],"6",["A quantidade diminuiu.","Retire 2 de 8.","8 - 2 = 6."],"Oito menos dois é igual a seis."),
    _q("mat-105",1,"sequencias","raciocinio","Complete: 2, 4, 6, ___.",["7","8","9","10"],"8",["Observe quanto aumenta.","A sequência aumenta de 2 em 2.","6 + 2 = 8."],"A sequência aumenta de dois em dois."),
    _q("mat-106",1,"geometria","formas","Qual forma tem três lados?",["Círculo","Quadrado","Triângulo","Retângulo"],"Triângulo",["Conte os lados.","A forma começa com tri.","O triângulo tem três lados."],"O triângulo possui três lados."),
    _q("mat-201",2,"adicao","numeros","Quanto é 24 + 13?",["27","37","47","35"],"37",["Some unidades e dezenas.","4 + 3 = 7 e 2 dezenas + 1 dezena = 3 dezenas.","24 + 13 = 37."],"Vinte e quatro mais treze é trinta e sete."),
    _q("mat-202",2,"subtracao","numeros","Quanto é 50 - 18?",["22","32","38","42"],"32",["Retire primeiro 10.","50 - 10 = 40; retire mais 8.","40 - 8 = 32."],"Cinquenta menos dezoito é trinta e dois."),
    _q("mat-203",2,"problemas","escola","Uma turma tem 12 meninas e 11 meninos. Quantos alunos há?",["21","22","23","24"],"23",["Junte os dois grupos.","12 + 11.","Doze mais onze é vinte e três."],"A turma tem 23 alunos."),
    _q("mat-204",2,"dinheiro","compras","Uma caneta custa R$ 4 e um caderno custa R$ 6. Quanto custam juntos?",["R$ 8","R$ 9","R$ 10","R$ 12"],"R$ 10",["Some os preços.","4 + 6.","Quatro mais seis é dez."],"Juntos custam dez reais."),
    _q("mat-205",2,"medidas","tempo","Uma hora tem quantos minutos?",["30","45","60","100"],"60",["Pense no relógio completo.","O ponteiro dos minutos dá uma volta.","Uma hora tem 60 minutos."],"Uma hora tem sessenta minutos."),
    _q("mat-206",2,"sequencias","raciocinio","Complete: 10, 20, 30, ___.",["35","40","45","50"],"40",["Observe o aumento.","Aumenta de 10 em 10.","30 + 10 = 40."],"A sequência aumenta de dez em dez."),
    _q("mat-301",3,"multiplicacao","grupos","Há 4 caixas com 3 carrinhos em cada. Quantos carrinhos há?",["7","10","12","14"],"12",["São quatro grupos de três.","Calcule 4 × 3.","3 + 3 + 3 + 3 = 12."],"Quatro grupos de três formam doze."),
    _q("mat-302",3,"multiplicacao","tabuada","Quanto é 5 × 6?",["25","30","35","40"],"30",["Pense em seis grupos de cinco.","Conte de 5 em 5 seis vezes.","5, 10, 15, 20, 25, 30."],"Cinco vezes seis é trinta."),
    _q("mat-303",3,"divisao","partilha","Doze balas foram divididas igualmente entre 3 crianças. Quantas cada uma recebeu?",["3","4","5","6"],"4",["Divida em três grupos iguais.","Procure 3 × qual número = 12.","3 × 4 = 12."],"Cada criança recebeu quatro balas."),
    _q("mat-304",3,"problemas","livros","João leu 18 páginas na segunda e 15 na terça. Quantas páginas leu?",["23","30","33","35"],"33",["Junte as páginas dos dois dias.","18 + 15.","18 + 10 = 28; mais 5 = 33."],"João leu trinta e três páginas."),
    _q("mat-305",3,"numeros_quantidades","valor_posicional","No número 347, qual algarismo ocupa a casa das dezenas?",["3","4","7","0"],"4",["As casas são centenas, dezenas e unidades.","O algarismo do meio está nas dezenas.","Em 347, o 4 representa quatro dezenas."],"O algarismo das dezenas é 4."),
    _q("mat-306",3,"dinheiro","troco","Você pagou R$ 20 por um brinquedo de R$ 13. Qual foi o troco?",["R$ 5","R$ 6","R$ 7","R$ 8"],"R$ 7",["Troco é o que sobra.","Calcule 20 - 13.","Vinte menos treze é sete."],"O troco é sete reais."),
    _q("mat-401",4,"adicao","numeros","Quanto é 247 + 136?",["373","383","393","403"],"383",["Some primeiro as unidades.","Depois some dezenas e centenas.","247 + 136 = 383."],"Somando as ordens, o resultado é 383."),
    _q("mat-402",4,"subtracao","numeros","Quanto é 500 - 278?",["212","222","232","242"],"222",["Retire 200 primeiro.","500 - 200 = 300; depois retire 78.","300 - 78 = 222."],"Quinhentos menos duzentos e setenta e oito é 222."),
    _q("mat-403",4,"divisao","escola","Uma escola recebeu 96 livros para dividir igualmente entre 4 turmas. Quantos livros cada turma recebeu?",["22","24","26","28"],"24",["Dividir igualmente indica divisão.","Procure um número que vezes 4 dê 96.","4 × 24 = 96."],"Cada turma recebeu 24 livros."),
    _q("mat-404",4,"problemas","material_escolar","Uma caixa tem 6 fileiras com 9 lápis em cada. Quantos lápis há?",["45","48","54","63"],"54",["São seis grupos de nove.","Calcule 6 × 9.","Seis vezes nove é 54."],"Há cinquenta e quatro lápis."),
    _q("mat-405",4,"medidas","comprimento","Uma fita de 2 metros foi cortada em 4 partes iguais. Quanto mede cada parte?",["25 cm","40 cm","50 cm","75 cm"],"50 cm",["Dois metros são 200 centímetros.","Divida 200 por 4.","200 ÷ 4 = 50."],"Cada parte mede cinquenta centímetros."),
    _q("mat-406",4,"fracoes","pizza","Uma pizza foi dividida em 8 partes e 3 foram comidas. Que fração foi comida?",["3/5","3/8","5/8","8/3"],"3/8",["O denominador é o total de partes.","O numerador é o número de partes comidas.","Três de oito partes é 3/8."],"A fração comida foi três oitavos."),
    _q("mat-501",5,"dinheiro","passeio","Um passeio custa R$ 18 por criança. Quanto custará para 7 crianças?",["R$ 116","R$ 126","R$ 136","R$ 146"],"R$ 126",["O valor se repete sete vezes.","Calcule 18 × 7.","10 × 7 + 8 × 7 = 70 + 56."],"O custo total é cento e vinte e seis reais."),
    _q("mat-502",5,"problemas","producao","Uma fábrica fez 125 peças de manhã e 98 à tarde. Vendeu 47. Quantas restaram?",["166","176","186","196"],"176",["Primeiro some a produção.","125 + 98 = 223.","Depois calcule 223 - 47."],"Restaram cento e setenta e seis peças."),
    _q("mat-503",5,"fracoes","receita","Uma receita usa 3/4 de xícara de leite. Se for feita pela metade, quanto leite será usado?",["1/4","3/8","1/2","2/3"],"3/8",["Metade significa dividir por 2.","Dividir 3/4 por 2 é multiplicar por 1/2.","3/4 × 1/2 = 3/8."],"A metade de três quartos é três oitavos."),
    _q("mat-504",5,"medidas","tempo","Um filme começou às 14h35 e durou 1h45. A que horas terminou?",["16h10","16h20","16h30","17h20"],"16h20",["Some uma hora primeiro.","14h35 + 1h = 15h35.","15h35 + 45 min = 16h20."],"O filme terminou às dezesseis horas e vinte."),
    _q("mat-505",5,"raciocinio_logico","padroes","Qual número completa: 3, 6, 12, 24, ___?",["30","36","42","48"],"48",["Observe a relação entre os termos.","Cada número é o dobro do anterior.","24 × 2 = 48."],"A sequência dobra a cada passo."),
    _q("mat-506",5,"geometria","area","Um retângulo mede 8 cm de comprimento e 5 cm de largura. Qual é a área?",["13 cm²","26 cm²","40 cm²","80 cm²"],"40 cm²",["Área do retângulo é comprimento vezes largura.","Calcule 8 × 5.","Oito vezes cinco é quarenta."],"A área é quarenta centímetros quadrados."),
]


QUESTOES.extend([
    _q("mat-107",1,"numeros_quantidades","numeros","Qual número vem antes de 10?",["8","9","11","12"],"9",["Conte até 10.","O número anterior fica uma posição antes.","Antes de 10 vem 9."],"O número anterior a 10 é 9."),
    _q("mat-108",1,"adicao","frutas","João tinha 4 bananas e ganhou 3. Quantas tem agora?",["5","6","7","8"],"7",["Junte as quantidades.","Calcule 4 + 3.","Quatro mais três é sete."],"João ficou com sete bananas."),
    _q("mat-109",1,"subtracao","brinquedos","Havia 9 carrinhos. Três foram guardados. Quantos ficaram?",["5","6","7","12"],"6",["A quantidade diminuiu.","Calcule 9 - 3.","Nove menos três é seis."],"Ficaram seis carrinhos."),
    _q("mat-110",1,"numeros_quantidades","comparacao","Qual número é menor?",["6","2","8","5"],"2",["Compare os números.","Procure o mais próximo do zero.","Dois é o menor."],"O menor número é 2."),
    _q("mat-111",1,"sequencias","raciocinio","Complete: 1, 3, 5, ___.",["6","7","8","9"],"7",["Observe o aumento.","Aumenta de dois em dois.","5 + 2 = 7."],"O próximo número é 7."),
    _q("mat-112",1,"geometria","formas","Qual forma é redonda e não tem lados?",["Triângulo","Quadrado","Círculo","Retângulo"],"Círculo",["Pense em uma bola desenhada.","Ela não tem lados.","O círculo é redondo."],"O círculo não possui lados."),
    _q("mat-113",1,"adicao","animais","Há 5 pássaros na árvore e chegam mais 2. Quantos ficam?",["6","7","8","9"],"7",["Eles se juntaram.","Calcule 5 + 2.","Cinco mais dois é sete."],"Ficam sete pássaros."),
    _q("mat-114",1,"subtracao","escola","Lia tinha 7 lápis e deu 1. Com quantos ficou?",["5","6","7","8"],"6",["Ela deu um lápis.","Calcule 7 - 1.","Sete menos um é seis."],"Lia ficou com seis lápis."),
    _q("mat-115",1,"medidas","comparacao","Qual objeto costuma ser mais comprido?",["Borracha","Lápis","Moeda","Botão"],"Lápis",["Compare os comprimentos.","Pense nos objetos escolares.","O lápis costuma ser mais comprido."],"O lápis costuma ser o mais comprido."),
    _q("mat-207",2,"adicao","escola","Quanto é 32 + 25?",["47","55","57","67"],"57",["Some dezenas e unidades.","30 + 20 e 2 + 5.","50 + 7 = 57."],"Trinta e dois mais vinte e cinco é 57."),
    _q("mat-208",2,"subtracao","numeros","Quanto é 74 - 22?",["42","50","52","62"],"52",["Retire duas dezenas.","74 - 20 = 54.","54 - 2 = 52."],"Setenta e quatro menos vinte e dois é 52."),
    _q("mat-209",2,"problemas","livros","Ana tinha 21 livros e ganhou 14. Quantos livros tem agora?",["25","35","37","45"],"35",["Ela ganhou livros.","Calcule 21 + 14.","Vinte e um mais quatorze é 35."],"Ana tem trinta e cinco livros."),
    _q("mat-210",2,"dinheiro","compras","Você tem R$ 15 e gasta R$ 6. Quanto sobra?",["R$ 7","R$ 8","R$ 9","R$ 11"],"R$ 9",["O valor diminui.","Calcule 15 - 6.","Quinze menos seis é nove."],"Sobram nove reais."),
    _q("mat-211",2,"medidas","tempo","Meia hora corresponde a quantos minutos?",["15","20","30","45"],"30",["Uma hora tem 60 minutos.","Meia hora é a metade.","Metade de 60 é 30."],"Meia hora tem trinta minutos."),
    _q("mat-212",2,"sequencias","raciocinio","Complete: 5, 10, 15, ___.",["18","20","25","30"],"20",["Observe o aumento.","Aumenta de cinco em cinco.","15 + 5 = 20."],"O próximo número é 20."),
    _q("mat-213",2,"geometria","formas","Qual forma tem quatro lados iguais?",["Círculo","Triângulo","Quadrado","Oval"],"Quadrado",["Conte os lados.","Eles possuem o mesmo tamanho.","O quadrado tem quatro lados iguais."],"O quadrado possui quatro lados iguais."),
    _q("mat-214",2,"numeros_quantidades","valor_posicional","No número 46, quantas dezenas há?",["4","6","40","46"],"4",["Observe o algarismo das dezenas.","Ele fica à esquerda.","Em 46 há quatro dezenas."],"O número 46 possui quatro dezenas."),
    _q("mat-215",2,"problemas","frutas","Há 28 laranjas em uma caixa e 10 são retiradas. Quantas ficam?",["8","18","20","38"],"18",["A quantidade diminui.","Calcule 28 - 10.","Vinte e oito menos dez é dezoito."],"Ficam dezoito laranjas."),
])


# Banco novo da metodologia por idade. As questões antigas permanecem acima para
# que atividades iniciadas antes da atualização continuem podendo ser concluídas.
QUESTOES.extend([
    # 4 a 5 anos: contagem, comparação, formas e padrões com apoio visual.
    _q("mat-f45-01", 1, "numeros_quantidades", "contagem", "Quantas maçãs aparecem?",
       ["2", "3", "4", "5"], "3",
       ["Aponte para cada maçã.", "Conte uma de cada vez.", "Há três maçãs."],
       "A figura tem três maçãs.", "4-5", "🍎 🍎 🍎"),
    _q("mat-f45-02", 1, "numeros_quantidades", "comparacao", "Qual grupo tem MAIS figuras?",
       ["⭐ ⭐ ⭐ ⭐", "🍀 🍀", "🚗", "🌙 🌙 🌙"], "⭐ ⭐ ⭐ ⭐",
       ["Conte as figuras de cada grupo.", "Procure o grupo com a maior quantidade.", "Quatro estrelas formam o maior grupo."],
       "O grupo com quatro estrelas tem mais figuras.", "4-5", "🔎"),
    _q("mat-f45-03", 1, "geometria", "formas", "Qual é o nome desta forma?",
       ["Triângulo", "Círculo", "Quadrado", "Retângulo"], "Triângulo",
       ["Conte as pontas.", "A figura tem três lados.", "É um triângulo."],
       "A figura é um triângulo.", "4-5", "🔺"),
    _q("mat-f45-04", 1, "adicao_visual", "juntar", "Havia 2 patinhos e chegou mais 1. Quantos ficaram?",
       ["2", "3", "4", "5"], "3",
       ["Conte os dois primeiros.", "Junte o patinho que chegou.", "Dois mais um são três."],
       "Ficaram três patinhos.", "4-5", "🦆 🦆  +  🦆"),
    _q("mat-f45-05", 1, "sequencias", "padroes", "Qual figura vem depois?",
       ["🔴", "🔵", "🟢", "🟡"], "🔴",
       ["Observe as cores que se repetem.", "Depois do azul volta a primeira cor.", "A próxima figura é vermelha."],
       "O padrão alterna vermelho e azul.", "4-5", "🔴 🔵 🔴 🔵 ❓"),

    # 6 a 8 anos: cálculo guiado e problemas curtos do cotidiano.
    _q("mat-f68-01", 2, "adicao", "numeros", "Quanto é 7 + 5?",
       ["10", "11", "12", "13"], "12",
       ["Comece no 7.", "Conte mais cinco: 8, 9, 10, 11, 12.", "Sete mais cinco é doze."],
       "7 + 5 = 12.", "6-8"),
    _q("mat-f68-02", 2, "subtracao", "numeros", "Quanto é 14 - 6?",
       ["6", "7", "8", "9"], "8",
       ["A quantidade vai diminuir.", "Retire seis de quatorze.", "Quatorze menos seis é oito."],
       "14 - 6 = 8.", "6-8"),
    _q("mat-f68-03", 2, "sequencias", "padroes", "Complete: 5, 10, 15, ___.",
       ["18", "20", "25", "30"], "20",
       ["Observe quanto aumenta.", "A sequência cresce de cinco em cinco.", "Depois de 15 vem 20."],
       "A sequência aumenta de cinco em cinco.", "6-8"),
    _q("mat-f68-04", 2, "dinheiro", "compras", "Um suco custa R$ 6 e um pão custa R$ 4. Quanto custam juntos?",
       ["R$ 8", "R$ 9", "R$ 10", "R$ 12"], "R$ 10",
       ["Junte os dois preços.", "Calcule 6 + 4.", "Seis mais quatro é dez."],
       "A compra custa dez reais.", "6-8"),
    _q("mat-f68-05", 2, "medidas", "tempo", "A aula começa às 8h e termina às 10h. Quanto tempo dura?",
       ["1 hora", "2 horas", "3 horas", "4 horas"], "2 horas",
       ["Conte de 8h até 9h.", "Depois conte de 9h até 10h.", "São duas horas."],
       "Das 8h às 10h passam duas horas.", "6-8"),

    # 9 a 11 anos: operações, frações, medidas e resolução de problemas.
    _q("mat-f911-01", 3, "multiplicacao", "grupos", "Uma estante tem 6 prateleiras com 8 livros em cada. Quantos livros há?",
       ["42", "46", "48", "54"], "48",
       ["São seis grupos de oito.", "Calcule 6 × 8.", "Seis vezes oito é quarenta e oito."],
       "A estante tem 48 livros.", "9-11"),
    _q("mat-f911-02", 3, "divisao", "partilha", "Quarenta e cinco figurinhas foram divididas entre 5 crianças. Quantas cada uma recebeu?",
       ["7", "8", "9", "10"], "9",
       ["Divida em cinco grupos iguais.", "Procure 5 × qual número = 45.", "5 × 9 = 45."],
       "Cada criança recebeu nove figurinhas.", "9-11"),
    _q("mat-f911-03", 3, "fracoes", "representacao", "Qual fração representa 3 partes de um total de 8?",
       ["3/5", "3/8", "5/8", "8/3"], "3/8",
       ["O total fica embaixo.", "As partes escolhidas ficam em cima.", "Três de oito é 3/8."],
       "A fração é três oitavos.", "9-11"),
    _q("mat-f911-04", 3, "geometria", "perimetro", "Um quadrado tem lados de 7 cm. Qual é o perímetro?",
       ["14 cm", "21 cm", "28 cm", "49 cm"], "28 cm",
       ["O quadrado tem quatro lados iguais.", "Some 7 quatro vezes.", "4 × 7 = 28."],
       "O perímetro mede 28 centímetros.", "9-11"),
    _q("mat-f911-05", 3, "problemas", "planejamento", "Uma turma arrecadou 135 livros e doou 48. Quantos restaram?",
       ["77", "87", "93", "97"], "87",
       ["A quantidade diminuiu.", "Calcule 135 - 48.", "Cento e trinta e cinco menos quarenta e oito é 87."],
       "Restaram 87 livros.", "9-11"),

    # 12 a 13 anos: proporcionalidade, porcentagem, álgebra e geometria.
    _q("mat-f1213-01", 5, "porcentagem", "desconto", "Uma mochila de R$ 120 recebeu 25% de desconto. Qual é o novo preço?",
       ["R$ 80", "R$ 90", "R$ 95", "R$ 100"], "R$ 90",
       ["Calcule um quarto de 120.", "25% de 120 é 30.", "Retire 30 de 120."],
       "Com desconto de R$ 30, a mochila custa R$ 90.", "12-13"),
    _q("mat-f1213-02", 5, "algebra", "equacao", "Qual valor de x resolve 3x + 5 = 20?",
       ["3", "4", "5", "6"], "5",
       ["Retire 5 dos dois lados.", "Assim, 3x = 15.", "Divida 15 por 3."],
       "O valor de x é 5.", "12-13"),
    _q("mat-f1213-03", 5, "proporcionalidade", "receita", "Uma receita para 4 pessoas usa 2 xícaras de farinha. Quantas xícaras são necessárias para 10 pessoas?",
       ["4", "5", "6", "8"], "5",
       ["Duas xícaras servem quatro pessoas.", "Cada duas pessoas usam uma xícara.", "Dez pessoas usam cinco xícaras."],
       "São necessárias cinco xícaras.", "12-13"),
    _q("mat-f1213-04", 5, "geometria", "area", "Um triângulo tem base de 12 cm e altura de 7 cm. Qual é a área?",
       ["42 cm²", "56 cm²", "84 cm²", "96 cm²"], "42 cm²",
       ["Use base × altura ÷ 2.", "Calcule 12 × 7 = 84.", "Divida 84 por 2."],
       "A área do triângulo é 42 cm².", "12-13"),
    _q("mat-f1213-05", 5, "raciocinio_logico", "padroes", "Qual número completa: 2, 6, 12, 20, 30, ___?",
       ["36", "40", "42", "48"], "42",
       ["Observe as diferenças: 4, 6, 8, 10.", "A próxima diferença é 12.", "30 + 12 = 42."],
       "A sequência cresce somando números pares consecutivos.", "12-13"),
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
