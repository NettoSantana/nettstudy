# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\modules\experiencia_aluno.py
# Data e hora do último recode: 25/11/2026 19:11 -0300
# Motivo da alteração: configurar orientação por faixa etária, preferências, revisão e sugestões adaptativas.

from database import conectar

MATERIAS = {"matematica": "Matemática", "portugues": "Português", "leitura": "Leitura"}
DIFICULDADES = {"facil": "Fácil", "normal": "Normal", "dificil": "Difícil"}
AVATARES = {"original": "Original", "verde": "Verde", "azul": "Azul", "violeta": "Violeta"}
AVALIACOES = {"facil": "Muito fácil", "normal": "Na medida", "dificil": "Muito difícil"}

AGENTES = (
    (5, "4–5", "Observe, aponte e diga o que descobriu.", 5),
    (7, "6–7", "Leia uma instrução de cada vez. Explique sua ideia com um exemplo.", 6),
    (9, "8–9", "Identifique as pistas e explique como chegou à resposta.", 7),
    (11, "10–11", "Compare duas ideias e sustente sua escolha com uma evidência.", 8),
    (14, "12–14", "Justifique sua resposta e confira se outra interpretação faz sentido.", 9),
    (17, "15–17", "Avalie as evidências e considere uma interpretação alternativa.", 10),
)


def agente(idade):
    for limite, faixa, orientacao, quantidade in AGENTES:
        if idade <= limite:
            return {"faixa": faixa, "orientacao": orientacao, "quantidade": quantidade}
    limite, faixa, orientacao, quantidade = AGENTES[-1]
    return {"faixa": faixa, "orientacao": orientacao, "quantidade": quantidade}


def inicializar_experiencia(caminho):
    with conectar(caminho) as banco:
        banco.executescript("""
            CREATE TABLE IF NOT EXISTS dificuldades_aluno (
                aluno_id INTEGER NOT NULL REFERENCES alunos(id),
                materia TEXT NOT NULL,
                dificuldade TEXT NOT NULL,
                PRIMARY KEY (aluno_id, materia)
            );
            CREATE TABLE IF NOT EXISTS avaliacoes_aluno (
                aluno_id INTEGER NOT NULL REFERENCES alunos(id),
                materia TEXT NOT NULL,
                dia TEXT NOT NULL,
                avaliacao TEXT NOT NULL,
                PRIMARY KEY (aluno_id, materia, dia)
            );
        """)


def preferencias(caminho, aluno_id):
    with conectar(caminho) as banco:
        rows = banco.execute("SELECT materia,dificuldade FROM dificuldades_aluno WHERE aluno_id=?", (aluno_id,))
        return {r["materia"]: r["dificuldade"] for r in rows}


def salvar_preferencias(caminho, aluno_id, avatar, dificuldades):
    if avatar not in AVATARES or any(valor not in DIFICULDADES for valor in dificuldades.values()):
        raise ValueError("Preferência inválida.")
    with conectar(caminho) as banco:
        banco.execute("UPDATE alunos SET avatar=? WHERE id=?", (avatar, aluno_id))
        banco.executemany(
            """INSERT INTO dificuldades_aluno VALUES (?, ?, ?) ON CONFLICT(aluno_id,materia)
               DO UPDATE SET dificuldade=excluded.dificuldade""",
            [(aluno_id, materia, dificuldades[materia]) for materia in MATERIAS],
        )


def avaliar_atividade(caminho, aluno_id, materia, dia, avaliacao):
    if materia not in MATERIAS or avaliacao not in AVALIACOES:
        raise ValueError("Avaliação inválida.")
    with conectar(caminho) as banco:
        banco.execute(
            """INSERT INTO avaliacoes_aluno VALUES (?, ?, ?, ?) ON CONFLICT(aluno_id,materia,dia)
               DO UPDATE SET avaliacao=excluded.avaliacao""",
            (aluno_id, materia, dia, avaliacao),
        )


def sugerir_dificuldades(caminho, aluno_id, desempenho):
    niveis = tuple(DIFICULDADES)
    atuais = preferencias(caminho, aluno_id)
    sugestoes = {}
    with conectar(caminho) as banco:
        for materia in MATERIAS:
            ultimas = banco.execute(
                "SELECT avaliacao FROM avaliacoes_aluno WHERE aluno_id=? AND materia=? ORDER BY dia DESC LIMIT 3",
                (aluno_id, materia),
            ).fetchall()
            if len(ultimas) < 3:
                continue
            respostas = [r["avaliacao"] for r in ultimas]
            nivel = niveis.index(atuais.get(materia, "normal"))
            dominio = desempenho.get(materia)
            if dominio is None:
                continue
            if respostas.count("facil") >= 2 and dominio >= 75 and nivel < 2:
                sugestoes[materia] = niveis[nivel + 1]
            if respostas.count("dificil") >= 2 and dominio <= 60 and nivel > 0:
                sugestoes[materia] = niveis[nivel - 1]
    return sugestoes


def revisar_plano(selecionadas, por_habilidade, faixa, assinatura, quantidade):
    if len(selecionadas) > quantidade:
        return []
    permitidos = {questao["id"] for grupo in por_habilidade.values() for questao in grupo}
    usados = set()
    revisadas = []
    for questao in selecionadas:
        chave = assinatura(questao)
        if questao["id"] in permitidos and questao.get("faixa_etaria") == faixa and chave not in usados:
            revisadas.append(questao)
            usados.add(chave)
    return revisadas
