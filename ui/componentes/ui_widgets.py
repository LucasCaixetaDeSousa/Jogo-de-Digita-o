from __future__ import annotations

import pygame
from game_config import GameConfig

class UIRenderer:

    # Desenha fundo
    @staticmethod
    def desenhar_fundo(tela) -> None:
        tela.fill(GameConfig.CINZA)

    # Desenha título
    @staticmethod
    def desenhar_titulo(tela, texto: str, fonte, largura_tela: int | None = None) -> None:

        if largura_tela is None:
            largura_tela = tela.get_width()

        img = fonte.render(texto, True, GameConfig.AMARELO)

        rect = img.get_rect(
            center=(largura_tela // 2, GameConfig.VOLTAR_Y + GameConfig.VOLTAR_A // 2)
        )

        tela.blit(img, rect)

    # Desenha botão
    @staticmethod
    def desenhar_botao(
        tela,
        texto: str,
        fonte,
        x: int,
        y: int,
        largura: int | None = None,
        altura: int | None = None,
        excluir: bool = False,
        raio: int | None = None,
        borda: int | None = None,
    ) -> pygame.Rect:

        if largura is None:
            largura = GameConfig.BOTAO_LARGURA_PADRAO
        if altura is None:
            altura = GameConfig.BOTAO_ALTURA_PADRAO
        if raio is None:
            raio = GameConfig.BOTAO_RAIO
        if borda is None:
            borda = GameConfig.BOTAO_BORDA

        rect = pygame.Rect(x, y, largura, altura)

        mouse = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse)

        cor = GameConfig.BRANCO

        if hover:
            cor = GameConfig.VERMELHO if excluir else GameConfig.VERDE

        pygame.draw.rect(tela, cor, rect, borda, border_radius=raio)

        img = fonte.render(texto, True, cor)
        tela.blit(img, img.get_rect(center=rect.center))

        return rect

    # Desenha botão voltar
    @staticmethod
    def desenhar_botao_voltar(tela, fonte) -> pygame.Rect:

        return UIRenderer.desenhar_botao(
            tela=tela,
            texto="Voltar",
            fonte=fonte,
            x=GameConfig.VOLTAR_X,
            y=GameConfig.VOLTAR_Y,
            largura=GameConfig.VOLTAR_L,
            altura=GameConfig.VOLTAR_A,
            excluir=False,
        )


class UIButton:

    # Inicializa botão
    def __init__(
        self,
        texto: str,
        fonte,
        rect: pygame.Rect,
        excluir: bool = False,
    ) -> None:

        self.texto = texto
        self.fonte = fonte
        self.rect = rect
        self.excluir = excluir

        self.hover = False
        self._cache_render: dict[tuple[str, tuple[int, int, int]], pygame.Surface] = {}

    # Atualiza estado do botão
    def atualizar(self) -> None:

        mouse = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse)

    # Retorna cor atual do botão
    def _cor_atual(self):

        if not self.hover:
            return GameConfig.BRANCO

        return GameConfig.VERMELHO if self.excluir else GameConfig.VERDE

    # Renderiza texto com cache
    def _render_texto(self, cor):

        chave = (self.texto, cor)

        if chave not in self._cache_render:
            self._cache_render[chave] = self.fonte.render(self.texto, True, cor)

        return self._cache_render[chave]

    # Desenha botão
    def desenhar(self, tela) -> None:

        self.atualizar()

        cor = self._cor_atual()

        pygame.draw.rect(
            tela,
            cor,
            self.rect,
            GameConfig.BOTAO_BORDA,
            border_radius=GameConfig.BOTAO_RAIO,
        )

        texto_img = self._render_texto(cor)
        tela.blit(texto_img, texto_img.get_rect(center=self.rect.center))

    # Verifica clique no botão
    def clicado(self, evento) -> bool:

        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )

    # Atualiza texto do botão
    def set_texto(self, texto: str) -> None:

        if texto != self.texto:
            self.texto = texto
            self._cache_render.clear()