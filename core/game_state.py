from __future__ import annotations

class GameState:

    # Inicializa estado global do jogo
    def __init__(self) -> None:
        self.nome: str | None = None
        self.turma: str | None = None
        self.is_admin: bool = False

        self.nivel_atual: str | None = None
        self.dificuldade_atual: str | None = None

    # Registra login do jogador
    def login(self, nome: str, turma: str, is_admin: bool = False) -> None:
        self.nome = nome
        self.turma = turma
        self.is_admin = is_admin

    # Limpa estado ao sair
    def logout(self) -> None:
        self.nome = None
        self.turma = None
        self.is_admin = False
        self.nivel_atual = None
        self.dificuldade_atual = None

    # Define nível atual do jogo
    def iniciar_nivel(self, nivel_id: str, dificuldade: str | None = None) -> None:
        self.nivel_atual = str(nivel_id)
        self.dificuldade_atual = dificuldade