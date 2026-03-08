from __future__ import annotations
import pygame
from game_config import GameConfig

class UIListItemRenderer:

    # Desenha item de lista
    @staticmethod
    def draw(tela, rect, texto, fonte, selecionado, hover):

        cor = (
            GameConfig.VERDE
            if hover
            else GameConfig.AMARELO
            if selecionado
            else GameConfig.BRANCO
        )

        pygame.draw.rect(tela, GameConfig.CINZA, rect)
        pygame.draw.rect(tela, cor, rect, 2, border_radius=8)

        img = fonte.render(texto, True, cor)

        tela.blit(img, (rect.x + 12, rect.y + 6))