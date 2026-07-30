# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\matematica.py
# Data e hora do último recode: 30/07/2026 20:21 -03:00
# Motivo da alteração: criar banco de Matemática por níveis 1 a 5, habilidades e progressão compatível com o perfil pedagógico.

from typing import Any


def _q(codigo: str, nivel: int, habilidade: str, tema: str, enunciado: str,
       alternativas: list[str], correta: str, dicas: list[str], explicacao: str) -> dict[str, Any]:
    return {
        "id": codigo, "nivel": nivel, "habilidade": habilidade, "tema": tema,
        "enunciado": enunciado, "alternativas": alternativas, "correta": correta,
        "dicas": dicas, "explicacao": explicacao,
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
