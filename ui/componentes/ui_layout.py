from __future__ import annotations
import pygame
from game_config import GameConfig

class UILayout:

    # Centraliza elementos verticalmente
    @staticmethod
    def centralizar_vertical(
        quantidade: int,
        largura_tela: int | None = None,
        altura_tela: int | None = None,
        largura_item: int | None = None,
        altura_item: int | None = None,
        espaco: int | None = None,
    ) -> list[tuple[int, int]]:

        if largura_tela is None:
            largura_tela = GameConfig.LARGURA
        if altura_tela is None:
            altura_tela = GameConfig.ALTURA
        if largura_item is None:
            largura_item = GameConfig.BOTAO_LARGURA_PADRAO
        if altura_item is None:
            altura_item = GameConfig.BOTAO_ALTURA_PADRAO
        if espaco is None:
            espaco = GameConfig.BOTAO_ESPACAMENTO

        if quantidade <= 0:
            return []

        total_h = quantidade * altura_item + (quantidade - 1) * espaco
        inicio_y = (altura_tela - total_h) // 2
        x = (largura_tela - largura_item) // 2

        posicoes: list[tuple[int, int]] = []

        for i in range(quantidade):

            y = inicio_y + i * (altura_item + espaco)
            posicoes.append((x, y))

        return posicoes

    # Gera botões de turmas
    @staticmethod
    def gerar_botoes_turmas(
        turmas: list,
        largura_botao: int | None = None,
        altura_botao: int | None = None,
        largura_tela: int | None = None,
        altura_tela: int | None = None,
    ) -> list[tuple[object, pygame.Rect]]:

        if largura_botao is None:
            largura_botao = GameConfig.BOTAO_LARGURA_PADRAO
        if altura_botao is None:
            altura_botao = GameConfig.BOTAO_ALTURA_PADRAO
        if largura_tela is None:
            largura_tela = GameConfig.LARGURA
        if altura_tela is None:
            altura_tela = GameConfig.ALTURA

        posicoes = UILayout.centralizar_vertical(
            quantidade=len(turmas),
            largura_tela=largura_tela,
            altura_tela=altura_tela,
            largura_item=largura_botao,
            altura_item=altura_botao,
            espaco=GameConfig.BOTAO_ESPACAMENTO,
        )

        botoes: list[tuple[object, pygame.Rect]] = []

        for i, turma in enumerate(turmas):

            x, y = posicoes[i]
            botoes.append((turma, pygame.Rect(x, y, largura_botao, altura_botao)))

        return botoes

    # Gera grade de níveis
    @staticmethod
    def gerar_grade_niveis(
        quantidade: int,
        cols: int | None = None,
        tamanho: int | None = None,
        espaco: int | None = None,
        y_inicio: int | None = None,
        largura_tela: int | None = None,
    ) -> list[pygame.Rect]:

        if cols is None:
            cols = GameConfig.NIVEL_COLS
        if tamanho is None:
            tamanho = GameConfig.NIVEL_TAM
        if espaco is None:
            espaco = GameConfig.NIVEL_ESPACO
        if y_inicio is None:
            y_inicio = GameConfig.NIVEL_Y_INICIO
        if largura_tela is None:
            largura_tela = GameConfig.LARGURA

        if quantidade <= 0:
            return []

        total_largura = cols * tamanho + (cols - 1) * espaco
        inicio_x = (largura_tela - total_largura) // 2

        rects: list[pygame.Rect] = []

        for i in range(quantidade):

            col = i % cols
            lin = i // cols

            x = inicio_x + col * (tamanho + espaco)
            y = y_inicio + lin * (tamanho + espaco)

            rects.append(pygame.Rect(x, y, tamanho, tamanho))

        return rects

Layout = UILayout