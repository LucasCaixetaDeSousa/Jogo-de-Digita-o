from __future__ import annotations
import time

class Estatisticas:

    # Inicializa estatísticas do nível
    def __init__(self) -> None:
        self.reset()

    # Reinicia todas as estatísticas
    def reset(self) -> None:

        self.inicio = time.time()
        self.fim = None

        self.total_digitado = 0
        self.acertos = 0
        self.erros = 0

    # Registra acerto de digitação
    def registrar_acerto(self) -> None:
        self.acertos += 1
        self.total_digitado += 1

    # Registra erro de digitação
    def registrar_erro(self) -> None:
        self.erros += 1
        self.total_digitado += 1

    # Finaliza contagem de tempo
    def finalizar(self) -> None:
        if self.fim is None:
            self.fim = time.time()

    # Retorna tempo decorrido
    def tempo(self) -> float:

        if self.fim:
            return self.fim - self.inicio

        return time.time() - self.inicio

    # Retorna tempo formatado mm:ss
    def tempo_formatado(self) -> str:

        t = int(self.tempo())

        minutos = t // 60
        segundos = t % 60

        return f"{minutos:02}:{segundos:02}"

    # Calcula precisão da digitação
    def precisao(self) -> int:

        if self.total_digitado == 0:
            return 100

        return int((self.acertos / self.total_digitado) * 100)