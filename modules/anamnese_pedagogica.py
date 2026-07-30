# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\anamnese_pedagogica.py
# Data e hora do último recode: 30/07/2026 18:41 -03:00
# Motivo da alteração: estruturar a anamnese em cinco etapas, múltiplas escolhas e resumo final.

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
        for chave, _ in LEITURA_HABILIDADES:
            valor = formulario.get(chave, '').strip()
            if not valor:
                raise ValueError('Avalie todas as habilidades de leitura e escrita.')
            _gravar(caminho_banco, aluno_id, 'leitura_escrita', chave, valor, 'unica')
        dificuldades = _lista_formulario(formulario, 'dificuldades_leitura')
        if not dificuldades:
            raise ValueError('Selecione ao menos uma opção em dificuldades percebidas.')
        _validar_exclusiva(dificuldades, 'nenhuma', 'Nenhuma dificuldade não pode ser marcada com outras opções.')
        _gravar(caminho_banco, aluno_id, 'leitura_escrita', 'dificuldades_leitura', dificuldades, 'multipla')
    elif etapa == 3:
        for chave, _ in MATEMATICA_HABILIDADES:
            valor = formulario.get(chave, '').strip()
            if not valor:
                raise ValueError('Avalie todas as habilidades de Matemática.')
            _gravar(caminho_banco, aluno_id, 'matematica', chave, valor, 'unica')
        dificuldades = _lista_formulario(formulario, 'dificuldades_matematica')
        if not dificuldades:
            raise ValueError('Selecione ao menos uma dificuldade de Matemática.')
        _validar_exclusiva(dificuldades, 'nenhuma', 'Nenhuma dificuldade não pode ser marcada com outras opções.')
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


def montar_resumo(respostas: dict[str, Any], nome_aluno: str) -> dict[str, Any]:
    leitura_ok, leitura_atencao = _separar_habilidades(respostas, LEITURA_HABILIDADES)
    matematica_ok, matematica_atencao = _separar_habilidades(respostas, MATEMATICA_HABILIDADES)
    concentracao = int(respostas.get('concentracao') or 10)
    questoes = 6 if concentracao <= 10 else 8 if concentracao <= 15 else 10
    return {
        'nome': nome_aluno,
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
    leitura_valores = [respostas.get(chave) for chave, _ in LEITURA_HABILIDADES]
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


def opcoes_template() -> dict[str, Any]:
    return {'escala': ESCALA, 'leitura_habilidades': LEITURA_HABILIDADES,
            'matematica_habilidades': MATEMATICA_HABILIDADES, **OPCOES}
