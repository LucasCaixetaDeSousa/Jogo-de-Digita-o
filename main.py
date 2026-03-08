from __future__ import annotations

import pygame
from core.game import Game

# Encerra pygame com segurança
def encerrar_tudo() -> None:

    try:
        pygame.mixer.quit()
    except Exception:
        pass

    try:
        pygame.quit()
    except Exception:
        pass

# Executa jogo
def main() -> None:

    try:

        jogo = Game()
        jogo.executar()

    finally:

        encerrar_tudo()

if __name__ == "__main__":
    main()