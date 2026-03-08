from __future__ import annotations

class MotorDigitacao:

    # Inicializa motor de digitação
    def __init__(self, texto: str, repeticoes: int):

        self.texto = texto
        self.repeticoes = int(repeticoes)

        self.reset()

    # Reinicia estado do motor
    def reset(self):

        self.indice = 0
        self.reps = 0

        self.erro = False
        self.concluido = False

        self.acertos = 0
        self.erros = 0

        self.combo = 0
        self.combo_bonus = 0

    # Processa caractere digitado
    def digitar(self, char: str):

        if self.concluido:
            return "bloqueado"

        if self.indice >= len(self.texto):
            return None

        if char == self.texto[self.indice]:

            self.indice += 1
            self.erro = False

            self.acertos += 1
            self.combo += 1

            if self.combo % 5 == 0:
                self.combo_bonus += 10

            resultado = "acerto"

        else:

            self.erro = True

            self.erros += 1
            self.combo = 0

            resultado = "erro"

        if self.indice == len(self.texto):

            self.reps += 1
            self.indice = 0
            self.erro = False

            if self.reps >= self.repeticoes:

                self.concluido = True
                return "nivel_concluido"

        return resultado