from __future__ import annotations
import pygame

from game_config import GameConfig
from ui.base_editor_scene import BaseEditorScene

class BaseListScene(BaseEditorScene):

    # Inicializa cena de lista
    def __init__(self, tela, fontes):

        super().__init__(tela, fontes)

        self.itens_rects = []

        self.linha_h = 34
        self.top_y = 140

        self.idx_sel = 0
        self.item_sel_id = None

        self.scroll.item_altura = self.linha_h
        self.scroll.topo = self.top_y
        self.scroll.altura_tela = tela.get_height()

    # Reconstrói lista de itens
    def rebuild_lista(self, itens):

        self.itens_rects.clear()

        x = 40
        y = self.top_y
        w = GameConfig.LARGURA - 220

        for i, item in enumerate(itens):

            r = pygame.Rect(x, y + i * self.linha_h, w, 30)

            self.itens_rects.append((item, r))

    # Detecta seleção de item
    def detectar_selecao(self, eventos):

        for e in eventos:

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                offset = -self.scroll.scroll * self.linha_h

                for i, (item, rect) in enumerate(self.itens_rects):

                    r = rect.move(0, offset)

                    if r.collidepoint(e.pos):

                        self.idx_sel = i
                        self.item_sel_id = item

                        return item

        return None

    # Desenha lista de itens
    def desenhar_lista(self, draw_item):

        offset = -self.scroll.scroll * self.linha_h
        mouse = pygame.mouse.get_pos()

        for item, rect in self.itens_rects:

            r = rect.move(0, offset)

            if r.bottom < self.top_y or r.top > GameConfig.ALTURA:
                continue

            selecionado = item == self.item_sel_id
            hover = r.collidepoint(mouse)

            draw_item(item, r, selecionado, hover)