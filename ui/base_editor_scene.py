from __future__ import annotations

from ui.base_scene import BaseScene
from ui.componentes.ui_scroll import UIScroll

class BaseEditorScene(BaseScene):

    # Inicializa cena de editor
    def __init__(self, tela, fontes):

        super().__init__(tela, fontes)

        self.estado: str = "lista"

        self.selecionado: int | None = None

        self.scroll = UIScroll(
            item_altura=40,
            topo=130,
            altura_tela=tela.get_height()
        )

    # Volta para lista
    def voltar_lista(self):

        self.estado = "lista"
        self.selecionado = None

    # Reseta editor
    def reset_editor(self):

        self.estado = "lista"
        self.selecionado = None
        self.scroll.scroll = 0

    # Aplica scroll da lista
    def aplicar_scroll(self, eventos, total_itens):

        for e in eventos:
            self.scroll.aplicar_evento(e)

        self.scroll.limitar(total_itens)

    # Calcula offset do scroll
    def offset(self, y):

        return self.scroll.aplicar_offset(y)

    # Verifica se item está visível
    def item_visivel(self, y):

        return self.scroll.visivel(y)

    # Detecta clique em item da lista
    def detectar_clique_lista(self, eventos, rects):

        import pygame

        for e in eventos:

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                for i, r in enumerate(rects):

                    if r.collidepoint(e.pos):
                        return i

        return None