from __future__ import annotations
import pygame

class UIScroll:

    # Inicializa scroll
    def __init__(
        self,
        item_altura: int,
        topo: int,
        altura_tela: int,
        margem_inferior: int = 20,
    ):

        self.scroll = 0

        self.item_altura = max(1, item_altura)
        self.topo = topo
        self.altura_tela = altura_tela
        self.margem_inferior = margem_inferior

    # Reseta scroll
    def reset(self):

        self.scroll = 0

    # Aplica evento de scroll
    def aplicar_evento(self, evento):

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 4:
                self.scroll = max(0, self.scroll - 1)

            elif evento.button == 5:
                self.scroll += 1

    # Calcula linhas visíveis
    def linhas_visiveis(self):

        area_visivel = self.altura_tela - self.topo - self.margem_inferior

        return max(1, area_visivel // self.item_altura)

    # Limita scroll
    def limitar(self, total_itens):

        linhas_visiveis = self.linhas_visiveis()

        max_scroll = max(0, total_itens - linhas_visiveis)

        if self.scroll > max_scroll:
            self.scroll = max_scroll

    # Aplica offset vertical
    def aplicar_offset(self, y_base):

        return y_base - self.scroll * self.item_altura

    # Verifica visibilidade
    def visivel(self, y):

        return self.topo <= y <= self.altura_tela