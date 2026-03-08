from __future__ import annotations
import pygame
from game_config import GameConfig

class UIInput:

    # Inicializa campo de entrada
    def __init__(
        self,
        rect: pygame.Rect,
        fonte,
        max_chars: int = 40,
        apenas_numeros: bool = False,
    ):

        self.rect = rect
        self.fonte = fonte

        self.texto = ""
        self.max_chars = max_chars
        self.apenas_numeros = apenas_numeros

        self.ativo = False

        self._cursor = True
        self._cursor_last = pygame.time.get_ticks()
        self._cursor_interval = 450

    # Atualiza entrada de texto
    def update(self, eventos):

        for e in eventos:

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.ativo = self.rect.collidepoint(e.pos)

            if not self.ativo:
                continue

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_BACKSPACE:

                    self.texto = self.texto[:-1]
                    return

                if not e.unicode:
                    return

                if self.apenas_numeros and not e.unicode.isdigit():
                    return

                if len(self.texto) < self.max_chars:
                    self.texto += e.unicode

    # Controla cursor piscando
    def _cursor_tick(self):

        agora = pygame.time.get_ticks()

        if agora - self._cursor_last > self._cursor_interval:

            self._cursor = not self._cursor
            self._cursor_last = agora

    # Desenha campo de entrada
    def draw(self, tela):

        self._cursor_tick()

        cor = GameConfig.AMARELO if self.ativo else GameConfig.BRANCO

        pygame.draw.rect(tela, GameConfig.CINZA, self.rect)
        pygame.draw.rect(tela, cor, self.rect, 2, border_radius=8)

        texto = self.texto

        if self.ativo and self._cursor:
            texto += "_"

        img = self.fonte.render(texto, True, GameConfig.BRANCO)

        tela.blit(img, (self.rect.x + 12, self.rect.y + 12))