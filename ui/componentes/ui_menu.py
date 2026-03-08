from __future__ import annotations
import pygame
from game_config import GameConfig
from ui.componentes.ui_layout import UILayout
from ui.componentes.ui_widgets import UIButton

class UIMenu:

    # Inicializa menu
    def __init__(self, tela, fonte) -> None:

        self.tela = tela
        self.fonte = fonte
        self.botoes: list[UIButton] = []

    # Cria botões do menu
    def criar(
        self,
        opcoes: list[tuple[str, object]],
        largura_botao: int | None = None,
        altura_botao: int | None = None,
        espaco: int | None = None,
    ) -> None:

        if largura_botao is None:
            largura_botao = GameConfig.BOTAO_LARGURA_PADRAO
        if altura_botao is None:
            altura_botao = GameConfig.BOTAO_ALTURA_PADRAO
        if espaco is None:
            espaco = GameConfig.BOTAO_ESPACAMENTO

        posicoes = UILayout.centralizar_vertical(
            quantidade=len(opcoes),
            largura_tela=self.tela.get_width(),
            altura_tela=self.tela.get_height(),
            largura_item=largura_botao,
            altura_item=altura_botao,
            espaco=espaco,
        )

        self.botoes = []

        for i, (texto, retorno) in enumerate(opcoes):

            x, y = posicoes[i]

            rect = pygame.Rect(x, y, largura_botao, altura_botao)

            botao = UIButton(texto=texto, fonte=self.fonte, rect=rect)

            botao.retorno = retorno

            self.botoes.append(botao)

    # Atualiza eventos do menu
    def atualizar(self, eventos):

        for e in eventos:

            for botao in self.botoes:

                if botao.clicado(e):
                    return botao.retorno

        return None

    # Desenha menu
    def desenhar(self) -> None:

        for botao in self.botoes:
            botao.desenhar(self.tela)