# Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\scripts\validar_ciclo_pedagogico.py
# Data e hora do último recode: 30/07/2026 21:17 -03:00
# Motivo da alteração: validar quantidade, níveis e capacidade de cinco dias sem repetição.

from modules.leitura import HISTORIAS
from modules.matematica import QUESTOES as QUESTOES_MATEMATICA
from modules.portugues import QUESTOES as QUESTOES_PORTUGUES


def validar_banco(nome: str, questoes: list[dict]) -> None:
    codigos = [item["id"] for item in questoes]
    if len(codigos) != len(set(codigos)):
        raise AssertionError(f"{nome}: há códigos duplicados.")

    for nivel in range(1, 6):
        total_nivel = sum(1 for item in questoes if int(item["nivel"]) == nivel)
        if total_nivel < 6:
            raise AssertionError(
                f"{nome}: nível {nivel} possui apenas {total_nivel} questões."
            )

    elegiveis_nivel_1 = [
        item for item in questoes if int(item["nivel"]) <= 2
    ]
    if len(elegiveis_nivel_1) < 30:
        raise AssertionError(
            f"{nome}: nível 1 não possui 30 questões elegíveis para cinco dias."
        )

    for item in questoes:
        obrigatorios = {
            "id", "nivel", "habilidade", "tema", "enunciado",
            "alternativas", "correta", "dicas", "explicacao",
        }
        faltando = obrigatorios - set(item)
        if faltando:
            raise AssertionError(
                f"{nome}: {item.get('id')} sem campos {sorted(faltando)}."
            )
        if item["correta"] not in item["alternativas"]:
            raise AssertionError(
                f"{nome}: resposta correta fora das alternativas em {item['id']}."
            )
        if len(item["dicas"]) < 3:
            raise AssertionError(
                f"{nome}: {item['id']} precisa de três dicas."
            )


def validar_leitura() -> None:
    codigos = [item["id"] for item in HISTORIAS]
    if len(codigos) != len(set(codigos)):
        raise AssertionError("Leitura: há histórias duplicadas.")
    if len(HISTORIAS) < 15:
        raise AssertionError("Leitura: são necessárias ao menos 15 histórias.")
    for historia in HISTORIAS:
        if len(historia.get("paginas", [])) != 3:
            raise AssertionError(
                f"Leitura: {historia['id']} deve possuir três páginas."
            )
        if len(historia.get("perguntas", [])) != 3:
            raise AssertionError(
                f"Leitura: {historia['id']} deve possuir três perguntas."
            )


if __name__ == "__main__":
    validar_banco("Matemática", QUESTOES_MATEMATICA)
    validar_banco("Português", QUESTOES_PORTUGUES)
    validar_leitura()
    print("VALIDAÇÃO PEDAGÓGICA: OK")
    print(f"Matemática: {len(QUESTOES_MATEMATICA)} questões")
    print(f"Português: {len(QUESTOES_PORTUGUES)} questões")
    print(f"Leitura: {len(HISTORIAS)} histórias")

# Validações de coerência entre enunciado e apoio
from modules.portugues import QUESTOES as QUESTOES_PORTUGUES, QUESTOES_COM_TEXTO
from modules.leitura import HISTORIAS, NIVEL_NUMERICO

assert all(q.get("usa_texto") == (q["id"] in QUESTOES_COM_TEXTO) for q in QUESTOES_PORTUGUES)
assert not next(q for q in QUESTOES_PORTUGUES if q["id"] == "por-115")["usa_texto"]
assert next(q for q in QUESTOES_PORTUGUES if q["id"] == "por-301")["usa_texto"]
assert len([h for h in HISTORIAS if h.get("nivel") == "iniciante"]) >= 5
assert NIVEL_NUMERICO["iniciante"] == 1
print("Apoio de Português e Leitura nível 1: OK")
