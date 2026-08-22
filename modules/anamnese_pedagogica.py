# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\anamnese_pedagogica.py
# Data e hora do último recode: 22/08/2026 02:25 -03:00
# Motivo da alteração: adaptar a avaliação inicial por faixa etária e calcular níveis iniciais por matéria.

import json
import sqlite3
from typing import Any

from database import conectar

SCHEMA = """
CREATE TABLE IF NOT EXISTS anamneses_estruturadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL UNIQUE,
    etapa_atual INTEGER NOT NULL DEFAULT 1 CHECK (etapa_atual BETWEEN 1 AND 6),
    concluida INTEGER NOT NULL DEFAULT 0 CHECK (concluida IN (0, 1)),
    resumo_json TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    concluida_em TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS anamnese_respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    secao TEXT NOT NULL,
    chave TEXT NOT NULL,
    valor TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('unica', 'multipla', 'texto')),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT,
    UNIQUE (aluno_id, secao, chave, valor),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_anamnese_respostas_aluno
    ON anamnese_respostas (aluno_id, secao, chave);
"""

ESCALA = [
    ('nao_consegue', 'Ainda não consegue'),
    ('muita_dificuldade', 'Consegue com muita dificuldade'),
    ('alguma_dificuldade', 'Consegue com alguma dificuldade'),
    ('consegue_bem', 'Consegue bem'),
    ('nao_sei', 'Não sei avaliar'),
]

LEITURA_HABILIDADES = [
    ('reconhece_letras', 'Reconhece letras e sons'),
    ('le_palavras', 'Lê palavras'),
    ('le_frases', 'Lê frases'),
    ('le_textos_curtos', 'Lê textos curtos'),
    ('le_fluencia', 'Lê com fluência'),
    ('entende_leitura', 'Entende o que acabou de ler'),
    ('identifica_personagens', 'Identifica personagens'),
    ('identifica_evento_principal', 'Identifica o acontecimento principal'),
    ('reconta_historia', 'Conta a história com as próprias palavras'),
    ('faz_inferencias', 'Faz inferências simples'),
    ('escreve_palavras', 'Escreve palavras'),
    ('escreve_frases', 'Escreve frases completas'),
    ('organiza_texto', 'Organiza começo, meio e fim'),
    ('usa_pontuacao', 'Usa pontuação'),
    ('produz_resumo', 'Produz um pequeno resumo'),
    ('revisa_texto', 'Revisa o próprio texto'),
]

MATEMATICA_HABILIDADES = [
    ('reconhece_numeros', 'Reconhece e compara números'),
    ('adicao', 'Realiza adição'),
    ('subtracao', 'Realiza subtração'),
    ('tabuada', 'Conhece a tabuada'),
    ('multiplicacao', 'Realiza multiplicação'),
    ('divisao', 'Realiza divisão'),
    ('problemas', 'Resolve problemas escritos'),
    ('dinheiro', 'Entende dinheiro e troco'),
    ('horas', 'Compreende horas'),
    ('medidas', 'Compreende medidas'),
    ('geometria', 'Reconhece formas geométricas'),
    ('sequencias', 'Identifica sequências e padrões'),
    ('calculo_mental', 'Realiza cálculo mental'),
]

HABILIDADES_POR_FAIXA = {
    '4-5': {
        'titulo_portugues': 'Português com apoio visual',
        'descricao_portugues': 'Considere situações simples, com figuras, objetos e comandos falados.',
        'portugues': [
            ('pt45_nomeia_figuras', 'Nomeia animais e objetos mostrados em figuras'),
            ('pt45_reconhece_cores', 'Reconhece e nomeia cores básicas'),
            ('pt45_reconhece_letras', 'Reconhece algumas letras, especialmente as do próprio nome'),
            ('pt45_som_inicial', 'Percebe quando duas palavras começam com o mesmo som'),
            ('pt45_compreende_comando', 'Compreende um comando simples, como “marque o gato”'),
        ],
        'matematica': [
            ('mat45_conta_ate_10', 'Conta objetos até 10 com apoio visual'),
            ('mat45_numero_quantidade', 'Relaciona um número pequeno à quantidade mostrada'),
            ('mat45_compara_quantidades', 'Percebe onde há mais ou menos objetos'),
            ('mat45_reconhece_formas', 'Reconhece círculo, quadrado e triângulo'),
            ('mat45_sequencia_visual', 'Completa uma sequência simples de cores ou figuras'),
        ],
    },
    '6-8': {
        'titulo_portugues': 'Português',
        'descricao_portugues': 'Nesta faixa, leitura e escrita são trabalhadas dentro de Português.',
        'portugues': [
            ('pt68_le_palavras', 'Lê palavras curtas e familiares'),
            ('pt68_le_frases', 'Lê frases curtas sem perder a sequência'),
            ('pt68_compreende_frase', 'Entende uma informação direta em uma frase'),
            ('pt68_escreve_palavras', 'Escreve palavras conhecidas de forma compreensível'),
            ('pt68_organiza_frase', 'Organiza palavras para formar uma frase com sentido'),
        ],
        'matematica': [
            ('mat68_numeros', 'Reconhece, ordena e compara números'),
            ('mat68_adicao', 'Resolve adições simples, com ou sem apoio visual'),
            ('mat68_subtracao', 'Resolve subtrações simples, com ou sem apoio visual'),
            ('mat68_sequencias', 'Completa sequências numéricas simples'),
            ('mat68_problemas', 'Entende e resolve um problema curto do cotidiano'),
        ],
    },
    '9-11': {
        'titulo_portugues': 'Português e leitura',
        'descricao_portugues': 'Considere leitura, interpretação e produção de textos curtos.',
        'portugues': [
            ('pt911_le_texto', 'Lê um texto curto com autonomia'),
            ('pt911_localiza_informacao', 'Localiza informações explícitas no texto'),
            ('pt911_sequencia', 'Organiza os acontecimentos na ordem correta'),
            ('pt911_ideia_principal', 'Identifica a ideia principal do texto'),
            ('pt911_produz_resumo', 'Escreve um pequeno resumo com começo, meio e fim'),
        ],
        'matematica': [
            ('mat911_multiplicacao', 'Resolve multiplicações adequadas ao ano escolar'),
            ('mat911_divisao', 'Resolve divisões simples e compreende o resultado'),
            ('mat911_problemas', 'Escolhe a operação correta em problemas escritos'),
            ('mat911_fracoes', 'Reconhece e compara frações simples'),
            ('mat911_medidas', 'Usa dinheiro, horas e medidas em situações práticas'),
        ],
    },
    '12-13': {
        'titulo_portugues': 'Português e leitura',
        'descricao_portugues': 'Considere interpretação, argumentação e escrita compatíveis com a idade.',
        'portugues': [
            ('pt1213_interpreta_texto', 'Interpreta textos com informações explícitas e implícitas'),
            ('pt1213_faz_inferencia', 'Deduz informações que não estão escritas diretamente'),
            ('pt1213_argumenta', 'Defende uma opinião usando uma justificativa'),
            ('pt1213_organiza_paragrafo', 'Organiza ideias em parágrafos coerentes'),
            ('pt1213_revisa_texto', 'Revisa ortografia, pontuação e concordância do próprio texto'),
        ],
        'matematica': [
            ('mat1213_operacoes', 'Resolve operações combinadas com autonomia'),
            ('mat1213_porcentagem', 'Resolve situações simples com porcentagem'),
            ('mat1213_proporcionalidade', 'Reconhece relações de proporção em problemas'),
            ('mat1213_equacoes', 'Resolve uma equação simples com valor desconhecido'),
            ('mat1213_logica', 'Explica o raciocínio usado em desafios matemáticos'),
        ],
    },
}


def faixa_por_idade(idade: Any) -> str:
    idade_numero = int(idade or 0)
    if idade_numero <= 5:
        return '4-5'
    if idade_numero <= 8:
        return '6-8'
    if idade_numero <= 11:
        return '9-11'
    return '12-13'


def habilidades_por_idade(idade: Any) -> dict[str, Any]:
    faixa = faixa_por_idade(idade)
    return {'faixa': faixa, **HABILIDADES_POR_FAIXA[faixa]}

OPCOES = {
    'tipo_escola': [('publica', 'Pública'), ('particular', 'Particular'), ('outra', 'Outra')],
    'situacao_escolar': [
        ('acompanha', 'Está acompanhando a turma'),
        ('algumas_dificuldades', 'Apresenta algumas dificuldades'),
        ('dificuldades_frequentes', 'Apresenta dificuldades frequentes'),
        ('muito_abaixo', 'Está muito abaixo do esperado'),
        ('nao_sei', 'Não sei avaliar'),
    ],
    'acompanhamentos': [
        ('reforco', 'Reforço escolar'), ('psicopedagogo', 'Psicopedagogo'),
        ('fonoaudiologo', 'Fonoaudiólogo'), ('psicologo', 'Psicólogo'),
        ('professor_particular', 'Professor particular'), ('nenhum', 'Nenhum'),
        ('outro', 'Outro'),
    ],
    'dificuldades_leitura': [
        ('leitura_lenta', 'Leitura lenta'), ('troca_letras', 'Troca de letras'),
        ('interpretacao', 'Dificuldade de interpretação'),
        ('escrita', 'Dificuldade para escrever'), ('ortografia', 'Ortografia'),
        ('pontuacao', 'Pontuação'), ('organizacao_ideias', 'Organização das ideias'),
        ('vocabulario', 'Vocabulário'), ('evita_leitura', 'Evita leitura'),
        ('nenhuma', 'Nenhuma dificuldade percebida'), ('outra', 'Outra'),
    ],
    'dificuldades_matematica': [
        ('adicao', 'Adição'), ('subtracao', 'Subtração'),
        ('multiplicacao', 'Multiplicação'), ('tabuada', 'Tabuada'),
        ('divisao', 'Divisão'), ('problemas', 'Problemas matemáticos'),
        ('calculo_mental', 'Cálculo mental'), ('dinheiro', 'Dinheiro'),
        ('horas_medidas', 'Horas e medidas'), ('geometria', 'Geometria'),
        ('raciocinio_logico', 'Raciocínio lógico'),
        ('nenhuma', 'Nenhuma dificuldade percebida'), ('outra', 'Outra'),
    ],
    'concentracao': [
        ('5', 'Até 5 minutos'), ('10', 'De 6 a 10 minutos'),
        ('15', 'De 11 a 15 minutos'), ('20', 'De 16 a 20 minutos'),
        ('25', 'Mais de 20 minutos'), ('0', 'Não sei avaliar'),
    ],
    'reacoes': [
        ('ajuda_comecar', 'Precisa de ajuda para começar'),
        ('ajuda_constante', 'Precisa de ajuda durante toda a atividade'),
        ('desiste_erro', 'Desiste quando erra'), ('frustra', 'Fica frustrado facilmente'),
        ('medo_responder', 'Tem medo de responder'), ('pressa', 'Responde com pressa'),
        ('distrai', 'Distrai-se facilmente'), ('aceita_dicas', 'Aceita dicas'),
        ('tenta_novamente', 'Tenta novamente'), ('gosta_desafios', 'Gosta de desafios'),
        ('estuda_sozinho', 'Consegue estudar sozinho'), ('nenhuma', 'Nenhuma dessas situações'),
    ],
    'formas_aprender': [
        ('texto', 'Texto'), ('imagens', 'Imagens'), ('audio', 'Áudio'),
        ('exemplos', 'Exemplos'), ('passo_a_passo', 'Passo a passo'),
        ('pratica', 'Exercícios práticos'), ('historias', 'Histórias'),
        ('jogos', 'Jogos e desafios'), ('nao_sei', 'Não sei avaliar'),
    ],
    'periodos': [('manha', 'Manhã'), ('tarde', 'Tarde'), ('noite', 'Noite'), ('varia', 'Varia'), ('nao_sei', 'Não sei')],
    'companhia': [
        ('sozinho', 'Prefere estudar sozinho'), ('adulto_perto', 'Prefere um adulto por perto'),
        ('constante', 'Precisa de acompanhamento constante'),
        ('depende', 'Depende da atividade'), ('nao_sei', 'Não sei avaliar'),
    ],
    'interesses': [
        ('animais', 'Animais'), ('ciencia', 'Ciência'), ('espaco', 'Espaço'),
        ('esportes', 'Futebol e esportes'), ('jogos', 'Jogos'),
        ('tecnologia', 'Tecnologia'), ('dinheiro', 'Dinheiro e compras'),
        ('historia', 'História'), ('natureza', 'Natureza'), ('musica', 'Música'),
        ('aventuras', 'Aventuras'), ('misterio', 'Mistério'), ('culinaria', 'Culinária'),
        ('maquinas', 'Veículos e máquinas'), ('outros', 'Outros'),
    ],
    'objetivos': [
        ('melhorar_notas', 'Melhorar as notas'), ('alfabetizacao', 'Reforçar a alfabetização'),
        ('melhorar_leitura', 'Melhorar a leitura'), ('interpretacao', 'Melhorar a interpretação'),
        ('melhorar_escrita', 'Melhorar a escrita'), ('matematica_basica', 'Aprender matemática básica'),
        ('tabuada', 'Reforçar tabuada'), ('problemas', 'Resolver problemas matemáticos'),
        ('rotina', 'Criar rotina de estudo'), ('autonomia', 'Aumentar autonomia'),
        ('provas', 'Preparar para provas'), ('recuperar', 'Recuperar conteúdos anteriores'),
        ('outro', 'Outro'),
    ],
    'condicoes': [
        ('visual', 'Dificuldade visual'), ('auditiva', 'Dificuldade auditiva'),
        ('tdah', 'TDAH informado pelo responsável'),
        ('dislexia', 'Dislexia informada pelo responsável'),
        ('psicopedagogico', 'Acompanhamento psicopedagógico'),
        ('ansiedade', 'Ansiedade diante de atividades'), ('outra', 'Outra necessidade'),
        ('nao_informar', 'Prefiro não informar'), ('nenhuma', 'Nenhuma'),
    ],
}

ROTULOS = {valor: rotulo for lista in OPCOES.values() for valor, rotulo in lista}
ROTULOS.update({valor: rotulo for valor, rotulo in ESCALA})
ROTULOS.update({chave: rotulo for chave, rotulo in LEITURA_HABILIDADES + MATEMATICA_HABILIDADES})
for configuracao in HABILIDADES_POR_FAIXA.values():
    ROTULOS.update({chave: rotulo for chave, rotulo in configuracao['portugues'] + configuracao['matematica']})


def inicializar_anamnese_pedagogica(caminho_banco: str) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA)


def _registro_base(caminho_banco: str, aluno_id: int) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            "INSERT OR IGNORE INTO anamneses_estruturadas (aluno_id) VALUES (?)",
            (aluno_id,),
        )


def obter_estado(caminho_banco: str, aluno_id: int) -> dict[str, Any]:
    _registro_base(caminho_banco, aluno_id)
    with conectar(caminho_banco) as conexao:
        cabecalho = conexao.execute(
            "SELECT * FROM anamneses_estruturadas WHERE aluno_id = ?", (aluno_id,)
        ).fetchone()
        linhas = conexao.execute(
            "SELECT secao, chave, valor, tipo FROM anamnese_respostas WHERE aluno_id = ? ORDER BY id",
            (aluno_id,),
        ).fetchall()
    respostas: dict[str, Any] = {}
    for linha in linhas:
        chave = linha['chave']
        if linha['tipo'] == 'multipla':
            respostas.setdefault(chave, []).append(linha['valor'])
        else:
            respostas[chave] = linha['valor']
    estado = dict(cabecalho)
    estado['respostas'] = respostas
    return estado


def _gravar(caminho_banco: str, aluno_id: int, secao: str, chave: str, valor: Any, tipo: str) -> None:
    valores = valor if isinstance(valor, list) else [valor]
    valores = [str(item).strip() for item in valores if str(item).strip()]
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            "DELETE FROM anamnese_respostas WHERE aluno_id = ? AND secao = ? AND chave = ?",
            (aluno_id, secao, chave),
        )
        for item in valores:
            conexao.execute(
                """INSERT INTO anamnese_respostas (aluno_id, secao, chave, valor, tipo)
                   VALUES (?, ?, ?, ?, ?)""",
                (aluno_id, secao, chave, item, tipo),
            )


def _lista_formulario(formulario: Any, nome: str) -> list[str]:
    return [item.strip() for item in formulario.getlist(nome) if item.strip()]


def _validar_exclusiva(valores: list[str], exclusiva: str, mensagem: str) -> None:
    if exclusiva in valores and len(valores) > 1:
        raise ValueError(mensagem)


def _limpar_secao(caminho_banco: str, aluno_id: int, secao: str) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            "DELETE FROM anamnese_respostas WHERE aluno_id = ? AND secao = ?",
            (aluno_id, secao),
        )


def salvar_etapa(caminho_banco: str, aluno_id: int, etapa: int, formulario: Any) -> None:
    _registro_base(caminho_banco, aluno_id)
    if etapa == 1:
        idade = formulario.get('idade', '').strip()
        ano = formulario.get('ano_escolar', '').strip()
        escola = formulario.get('tipo_escola', '').strip()
        situacao = formulario.get('situacao_escolar', '').strip()
        acompanhamentos = _lista_formulario(formulario, 'acompanhamentos')
        if not idade or not ano or not escola or not situacao or not acompanhamentos:
            raise ValueError('Preencha todos os dados escolares e selecione o acompanhamento atual.')
        if int(idade) < 4 or int(idade) > 18:
            raise ValueError('Informe uma idade entre 4 e 18 anos.')
        _validar_exclusiva(acompanhamentos, 'nenhum', 'Nenhum acompanhamento não pode ser marcado com outras opções.')
        for chave, valor in [('idade', idade), ('ano_escolar', ano), ('tipo_escola', escola), ('situacao_escolar', situacao)]:
            _gravar(caminho_banco, aluno_id, 'escolar', chave, valor, 'unica')
        _gravar(caminho_banco, aluno_id, 'escolar', 'acompanhamentos', acompanhamentos, 'multipla')
    elif etapa == 2:
        respostas = obter_estado(caminho_banco, aluno_id)['respostas']
        habilidades = habilidades_por_idade(respostas.get('idade'))['portugues']
        valores = []
        for chave, _ in habilidades:
            valor = formulario.get(chave, '').strip()
            if not valor:
                raise ValueError('Avalie todas as habilidades de Português apresentadas.')
            valores.append((chave, valor))
        dificuldades = _lista_formulario(formulario, 'dificuldades_leitura')
        if not dificuldades:
            raise ValueError('Selecione ao menos uma opção em dificuldades percebidas.')
        _validar_exclusiva(dificuldades, 'nenhuma', 'Nenhuma dificuldade não pode ser marcada com outras opções.')
        _limpar_secao(caminho_banco, aluno_id, 'leitura_escrita')
        for chave, valor in valores:
            _gravar(caminho_banco, aluno_id, 'leitura_escrita', chave, valor, 'unica')
        _gravar(caminho_banco, aluno_id, 'leitura_escrita', 'dificuldades_leitura', dificuldades, 'multipla')
    elif etapa == 3:
        respostas = obter_estado(caminho_banco, aluno_id)['respostas']
        habilidades = habilidades_por_idade(respostas.get('idade'))['matematica']
        valores = []
        for chave, _ in habilidades:
            valor = formulario.get(chave, '').strip()
            if not valor:
                raise ValueError('Avalie todas as habilidades de Matemática.')
            valores.append((chave, valor))
        dificuldades = _lista_formulario(formulario, 'dificuldades_matematica')
        if not dificuldades:
            raise ValueError('Selecione ao menos uma dificuldade de Matemática.')
        _validar_exclusiva(dificuldades, 'nenhuma', 'Nenhuma dificuldade não pode ser marcada com outras opções.')
        _limpar_secao(caminho_banco, aluno_id, 'matematica')
        for chave, valor in valores:
            _gravar(caminho_banco, aluno_id, 'matematica', chave, valor, 'unica')
        _gravar(caminho_banco, aluno_id, 'matematica', 'dificuldades_matematica', dificuldades, 'multipla')
    elif etapa == 4:
        concentracao = formulario.get('concentracao', '').strip()
        periodo = formulario.get('melhor_periodo', '').strip()
        companhia = formulario.get('companhia', '').strip()
        reacoes = _lista_formulario(formulario, 'reacoes')
        formas = _lista_formulario(formulario, 'formas_aprender')
        if not concentracao or not periodo or not companhia or not reacoes or not formas:
            raise ValueError('Preencha a concentração, a rotina e as preferências de aprendizagem.')
        _validar_exclusiva(reacoes, 'nenhuma', 'Nenhuma situação não pode ser marcada com outras reações.')
        _gravar(caminho_banco, aluno_id, 'rotina', 'concentracao', concentracao, 'unica')
        _gravar(caminho_banco, aluno_id, 'rotina', 'melhor_periodo', periodo, 'unica')
        _gravar(caminho_banco, aluno_id, 'rotina', 'companhia', companhia, 'unica')
        _gravar(caminho_banco, aluno_id, 'rotina', 'reacoes', reacoes, 'multipla')
        _gravar(caminho_banco, aluno_id, 'rotina', 'formas_aprender', formas, 'multipla')
    elif etapa == 5:
        interesses = _lista_formulario(formulario, 'interesses')
        objetivos = _lista_formulario(formulario, 'objetivos')
        condicoes = _lista_formulario(formulario, 'condicoes')
        observacoes = formulario.get('observacoes', '').strip()
        if not interesses or not objetivos or not condicoes:
            raise ValueError('Selecione interesses, objetivos e uma opção sobre condições relevantes.')
        if len(interesses) > 5:
            raise ValueError('Selecione no máximo cinco interesses.')
        if len(objetivos) > 4:
            raise ValueError('Selecione no máximo quatro objetivos.')
        _validar_exclusiva(condicoes, 'nenhuma', 'Nenhuma condição não pode ser marcada com outras opções.')
        _validar_exclusiva(condicoes, 'nao_informar', 'Prefiro não informar não pode ser marcado com outras opções.')
        _gravar(caminho_banco, aluno_id, 'interesses_objetivos', 'interesses', interesses, 'multipla')
        _gravar(caminho_banco, aluno_id, 'interesses_objetivos', 'objetivos', objetivos, 'multipla')
        _gravar(caminho_banco, aluno_id, 'interesses_objetivos', 'condicoes', condicoes, 'multipla')
        _gravar(caminho_banco, aluno_id, 'interesses_objetivos', 'observacoes', observacoes, 'texto')
    else:
        raise ValueError('Etapa inválida.')
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            "UPDATE anamneses_estruturadas SET etapa_atual = ?, atualizado_em = CURRENT_TIMESTAMP WHERE aluno_id = ?",
            (min(6, etapa + 1), aluno_id),
        )


def _rotulos(valores: Any) -> list[str]:
    if not isinstance(valores, list):
        valores = [valores] if valores else []
    return [ROTULOS.get(item, item) for item in valores]


def _separar_habilidades(respostas: dict[str, Any], habilidades: list[tuple[str, str]]) -> tuple[list[str], list[str]]:
    positivos, atencao = [], []
    for chave, rotulo in habilidades:
        valor = respostas.get(chave)
        if valor == 'consegue_bem': positivos.append(rotulo)
        elif valor in {'nao_consegue', 'muita_dificuldade', 'alguma_dificuldade'}: atencao.append(rotulo)
    return positivos, atencao


def _habilidades_da_resposta(respostas: dict[str, Any], materia: str) -> list[tuple[str, str]]:
    atuais = habilidades_por_idade(respostas.get('idade'))[materia]
    if any(respostas.get(chave) for chave, _ in atuais):
        return atuais
    return LEITURA_HABILIDADES if materia == 'portugues' else MATEMATICA_HABILIDADES


def _ano_numero(ano_escolar: Any) -> int:
    texto = str(ano_escolar or '')
    digitos = ''.join(caractere for caractere in texto if caractere.isdigit())
    return max(1, min(5, int(digitos[:1]))) if digitos else 1


def _nivel_por_habilidades(respostas: dict[str, Any], habilidades: list[tuple[str, str]]) -> int:
    pontuacao = {
        'nao_consegue': 1,
        'muita_dificuldade': 2,
        'alguma_dificuldade': 3,
        'consegue_bem': 4,
        'nao_sei': 2.5,
    }
    valores = [pontuacao[respostas[chave]] for chave, _ in habilidades if respostas.get(chave) in pontuacao]
    referencia = _ano_numero(respostas.get('ano_escolar'))
    if not valores:
        return referencia
    media = sum(valores) / len(valores)
    ajuste = -1 if media < 2.5 else 1 if media >= 3.6 else 0
    return max(1, min(5, referencia + ajuste))


def calcular_niveis_iniciais(respostas: dict[str, Any]) -> dict[str, int]:
    portugues = _habilidades_da_resposta(respostas, 'portugues')
    matematica = _habilidades_da_resposta(respostas, 'matematica')
    nivel_portugues = _nivel_por_habilidades(respostas, portugues)
    nivel_matematica = _nivel_por_habilidades(respostas, matematica)
    return {
        'portugues': nivel_portugues,
        'matematica': nivel_matematica,
        'leitura': nivel_portugues,
    }


def montar_resumo(respostas: dict[str, Any], nome_aluno: str) -> dict[str, Any]:
    portugues = _habilidades_da_resposta(respostas, 'portugues')
    matematica = _habilidades_da_resposta(respostas, 'matematica')
    leitura_ok, leitura_atencao = _separar_habilidades(respostas, portugues)
    matematica_ok, matematica_atencao = _separar_habilidades(respostas, matematica)
    concentracao = int(respostas.get('concentracao') or 10)
    questoes = 6 if concentracao <= 10 else 8 if concentracao <= 15 else 10
    return {
        'nome': nome_aluno,
        'faixa_etaria': faixa_por_idade(respostas.get('idade')),
        'niveis_iniciais': calcular_niveis_iniciais(respostas),
        'escolar': {
            'idade': respostas.get('idade', ''), 'ano': respostas.get('ano_escolar', ''),
            'escola': ROTULOS.get(respostas.get('tipo_escola', ''), ''),
            'situacao': ROTULOS.get(respostas.get('situacao_escolar', ''), ''),
            'acompanhamentos': _rotulos(respostas.get('acompanhamentos', [])),
        },
        'leitura': {'positivos': leitura_ok, 'atencao': leitura_atencao,
                    'dificuldades': _rotulos(respostas.get('dificuldades_leitura', []))},
        'matematica': {'positivos': matematica_ok, 'atencao': matematica_atencao,
                       'dificuldades': _rotulos(respostas.get('dificuldades_matematica', []))},
        'rotina': {
            'concentracao': ROTULOS.get(respostas.get('concentracao', ''), ''),
            'questoes': questoes, 'periodo': ROTULOS.get(respostas.get('melhor_periodo', ''), ''),
            'companhia': ROTULOS.get(respostas.get('companhia', ''), ''),
            'reacoes': _rotulos(respostas.get('reacoes', [])),
            'formas': _rotulos(respostas.get('formas_aprender', [])),
        },
        'interesses': _rotulos(respostas.get('interesses', [])),
        'objetivos': _rotulos(respostas.get('objetivos', [])),
        'condicoes': _rotulos(respostas.get('condicoes', [])),
        'observacoes': respostas.get('observacoes', ''),
    }


def converter_para_anamnese_legada(respostas: dict[str, Any]) -> dict[str, Any]:
    dificuldades = _rotulos(respostas.get('dificuldades_leitura', [])) + _rotulos(respostas.get('dificuldades_matematica', []))
    dificuldades = [item for item in dificuldades if not item.startswith('Nenhuma')]
    leitura_valores = [respostas.get(chave) for chave, _ in _habilidades_da_resposta(respostas, 'portugues')]
    pontuacao = {'nao_consegue': 1, 'muita_dificuldade': 2, 'alguma_dificuldade': 3, 'consegue_bem': 4, 'nao_sei': 2.5}
    media = sum(pontuacao.get(v, 2.5) for v in leitura_valores) / max(1, len(leitura_valores))
    nivel = 'iniciante' if media < 1.8 else 'basico' if media < 2.7 else 'intermediario' if media < 3.6 else 'avancado'
    formas = respostas.get('formas_aprender', [])
    preferencia = 'ambos' if 'audio' in formas and 'texto' in formas else 'voz' if 'audio' in formas else 'texto'
    concentracao = int(respostas.get('concentracao') or 10)
    if concentracao == 0: concentracao = 10
    return {
        'idade': int(respostas['idade']), 'ano_escolar': respostas['ano_escolar'],
        'dificuldades': ', '.join(dificuldades) or 'Nenhuma dificuldade específica informada',
        'materias_preferidas': ', '.join(_rotulos(respostas.get('interesses', []))),
        'nivel_leitura': nivel, 'tempo_concentracao': concentracao,
        'preferencia_interacao': preferencia,
        'objetivo_principal': ', '.join(_rotulos(respostas.get('objetivos', []))),
        'observacoes': respostas.get('observacoes', ''),
    }


def concluir(caminho_banco: str, aluno_id: int, resumo: dict[str, Any]) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.execute(
            """UPDATE anamneses_estruturadas
               SET etapa_atual = 6, concluida = 1, resumo_json = ?,
                   atualizado_em = CURRENT_TIMESTAMP, concluida_em = CURRENT_TIMESTAMP
               WHERE aluno_id = ?""",
            (json.dumps(resumo, ensure_ascii=False), aluno_id),
        )


def opcoes_template(respostas: dict[str, Any] | None = None) -> dict[str, Any]:
    respostas = respostas or {}
    habilidades = habilidades_por_idade(respostas.get('idade'))
    return {
        'escala': ESCALA,
        'faixa_etaria': habilidades['faixa'],
        'titulo_portugues': habilidades['titulo_portugues'],
        'descricao_portugues': habilidades['descricao_portugues'],
        'leitura_habilidades': habilidades['portugues'],
        'matematica_habilidades': habilidades['matematica'],
        **OPCOES,
    }
