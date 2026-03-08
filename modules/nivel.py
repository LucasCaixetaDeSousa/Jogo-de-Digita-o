from __future__ import annotations

class Nivel:

    # Inicializa nível
    def __init__(self, id, nome, palavras, repeticoes, dificuldade=None):

        self.id = id
        self.nome = nome
        self.palavras = palavras
        self.repeticoes = repeticoes
        self.dificuldade = dificuldade

        self.rect = None

    # Cria nível a partir de dict
    @staticmethod
    def from_dict(d, dificuldade=None):

        return Nivel(
            id=d["id"],
            nome=d["nome"],
            palavras=d["palavras"],
            repeticoes=d.get("repeticoes", 1),
            dificuldade=dificuldade
        )

    # Converte nível para dict
    def to_dict(self):

        return {
            "id": self.id,
            "nome": self.nome,
            "palavras": self.palavras,
            "repeticoes": self.repeticoes
        }