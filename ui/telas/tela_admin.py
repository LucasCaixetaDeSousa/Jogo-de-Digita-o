from __future__ import annotations
import pygame

from ui.base_scene import BaseScene
from ui.componentes.ui_menu import UIMenu

class TelaAdmin(BaseScene):

    # Inicializa tela admin
    def __init__(self, tela, fontes, state=None):

        super().__init__(tela, fontes)

        self.state = state
        self.menu = UIMenu(tela, self.fonte_peq)

        self._criar_menu()

    # Reinicia tela
    def iniciar(self):

        self._criar_menu()

    # Cria menu de editores
    def _criar_menu(self):

        opcoes = [
            ("ALUNOS", "editor_alunos"),
            ("TURMAS", "editor_turmas"),
            ("NÍVEIS", "editor_niveis"),
        ]

        self.menu.criar(opcoes)

        deslocamento = 40

        for botao in self.menu.botoes:
            botao.rect.y += deslocamento

    # Atualiza eventos da tela
    def atualizar(self, eventos):

        r = self.voltar_por_esc(eventos, "niveis")
        if r:
            return r

        r = self.voltar_por_botao(eventos, "niveis")
        if r:
            return r

        r = self.menu.atualizar(eventos)
        if r:
            return r

        return None

    # Desenha tela admin
    def desenhar(self):

        self.desenhar_cabecalho("Editores")

        self.menu.desenhar()