from __future__ import annotations

import time
import pygame
from game_config import GameConfig

class BaseScene:

    # Inicializa cena base
    def __init__(self, tela, fontes):

        self.tela = tela
        self.fonte, self.fonte_peq = fontes

        self.botao_voltar = pygame.Rect(0, 0, 0, 0)

        self._toast_msg = ""
        self._toast_until = 0

        self._cursor = True
        self._cursor_timer = time.time()

    # Desenha fundo e título
    def desenhar_base(self, titulo: str | None = None):

        GameConfig.desenhar_fundo(self.tela)

        if titulo:

            GameConfig.desenhar_titulo(
                self.tela,
                titulo,
                self.fonte,
                self.tela.get_width(),
            )

    # Compatibilidade com código antigo
    def draw_base(self, titulo):

        self.desenhar_base(titulo)

    # Desenha cabeçalho padrão
    def desenhar_cabecalho(self, titulo: str, com_voltar: bool = True):

        self.desenhar_base(titulo)

        if com_voltar:
            self.desenhar_voltar()

    # Desenha botão voltar
    def desenhar_voltar(self):

        self.botao_voltar = GameConfig.desenhar_botao_voltar(
            self.tela,
            self.fonte_peq,
        )

        return self.botao_voltar

    # Compatibilidade com código antigo
    def draw_back(self):

        return self.desenhar_voltar()

    # Verifica clique no botão voltar
    def clicou_voltar(self, evento) -> bool:

        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.botao_voltar.collidepoint(evento.pos)
        )

    # Verifica clique voltar em lista de eventos
    def back_clicked(self, eventos) -> bool:

        mouse = pygame.mouse.get_pos()

        for e in eventos:

            if (
                e.type == pygame.MOUSEBUTTONDOWN
                and e.button == 1
                and self.botao_voltar.collidepoint(mouse)
            ):
                return True

        return False

    # Detecta voltar usando ESC
    def voltar_por_esc(self, eventos, destino: str):

        for e in eventos:

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return destino

        return None

    # Detecta voltar usando botão
    def voltar_por_botao(self, eventos, destino: str):

        for e in eventos:

            if self.clicou_voltar(e):
                return destino

        return None

    # Controla cursor piscando
    def cursor(self, intervalo: float = 0.5) -> bool:

        if time.time() - self._cursor_timer > intervalo:

            self._cursor = not self._cursor
            self._cursor_timer = time.time()

        return self._cursor

    # Compatibilidade com código antigo
    def cursor_tick(self, intervalo: float = 0.5) -> bool:

        return self.cursor(intervalo)

    # Mostra mensagem temporária
    def toast(self, texto: str, duracao_ms: int = 1500) -> None:

        self._toast_msg = texto
        self._toast_until = pygame.time.get_ticks() + duracao_ms

    # Desenha mensagem toast
    def desenhar_toast(self) -> None:

        if not self._toast_msg:
            return

        if pygame.time.get_ticks() > self._toast_until:

            self._toast_msg = ""
            return

        img = self.fonte_peq.render(
            self._toast_msg,
            True,
            GameConfig.AMARELO
        )

        self.tela.blit(
            img,
            img.get_rect(
                center=(
                    self.tela.get_width() // 2, 90
                )
            ),
        )

    # Compatibilidade com código antigo
    def draw_toast(self) -> None:

        self.desenhar_toast()

    # Gera rects centralizados horizontalmente
    def _rects_lado_a_lado(
        self,
        quantidade: int,
        y: int,
        largura: int,
        altura: int,
        espacamento: int = 40
    ):

        total_largura = quantidade * largura + (quantidade - 1) * espacamento

        inicio_x = (GameConfig.LARGURA - total_largura) // 2

        rects = []

        for i in range(quantidade):

            x = inicio_x + i * (largura + espacamento)

            rects.append(
                pygame.Rect(x, y, largura, altura)
            )

        return rects