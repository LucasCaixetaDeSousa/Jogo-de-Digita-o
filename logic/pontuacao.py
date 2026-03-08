from __future__ import annotations

# Calcula pontuação final do nível
def calcular_pontuacao(
    acertos: int,
    erros: int,
    tempo: float,
    combo_bonus: int = 0,
    tempo_ideal: int = 30
) -> int:

    if tempo <= 0:
        tempo = 1

    pontos = acertos * 10

    pontos -= erros * 5

    pontos += combo_bonus

    bonus_tempo = max(0, tempo_ideal - int(tempo)) * 2

    pontos += bonus_tempo

    if pontos < 0:
        pontos = 0

    return pontos