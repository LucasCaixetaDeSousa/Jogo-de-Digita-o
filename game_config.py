from __future__ import annotations

class GameConfig:

    LARGURA: int = 900
    ALTURA: int = 400

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA = (30, 30, 30)

    VERDE = (0, 200, 0)
    VERMELHO = (200, 0, 0)
    AMARELO = (240, 220, 0)
    AZUL_CLARO = (100, 200, 255)

    OURO = (255, 215, 0)
    PRATA = (192, 192, 192)
    BRONZE = (205, 127, 50)

    ARQUIVO_PROGRESSO: str = "data/progresso.json"
    ARQUIVO_RANKING: str = "data/ranking.json"
    ARQUIVO_NIVEIS: str = "data/niveis.json"
    ARQUIVO_CONFIG: str = "data/config.json"
    ARQUIVO_TURMAS: str = "data/turmas.json"

    BOTAO_LARGURA_PADRAO = 300
    BOTAO_ALTURA_PADRAO = 50
    BOTAO_ESPACAMENTO = 20
    BOTAO_BORDA = 2
    BOTAO_RAIO = 10

    VOLTAR_X = 30
    VOLTAR_Y = 30
    VOLTAR_L = 120
    VOLTAR_A = 40

    NIVEL_COLS = 6
    NIVEL_TAM = 60
    NIVEL_ESPACO = 20
    NIVEL_Y_INICIO = 130

    # Desenha fundo padrão
    @staticmethod
    def desenhar_fundo(tela) -> None:

        from ui.componentes.ui_widgets import UIRenderer

        UIRenderer.desenhar_fundo(tela)

    # Desenha título centralizado
    @staticmethod
    def desenhar_titulo(tela, texto: str, fonte, largura_tela: int | None = None) -> None:

        from ui.componentes.ui_widgets import UIRenderer

        UIRenderer.desenhar_titulo(tela, texto, fonte, largura_tela)

    # Desenha botão padrão
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
    ):

        from ui.componentes.ui_widgets import UIRenderer

        return UIRenderer.desenhar_botao(
            tela=tela,
            texto=texto,
            fonte=fonte,
            x=x,
            y=y,
            largura=largura,
            altura=altura,
            excluir=excluir,
            raio=raio,
            borda=borda,
        )

    # Desenha botão voltar
    @staticmethod
    def desenhar_botao_voltar(tela, fonte):

        from ui.componentes.ui_widgets import UIRenderer

        return UIRenderer.desenhar_botao_voltar(tela, fonte)

    # Calcula posições centralizadas
    @staticmethod
    def calcular_posicoes_centralizadas(
        quantidade: int,
        largura_tela: int | None = None,
        altura_tela: int | None = None,
        largura_botao: int | None = None,
        altura_botao: int | None = None,
        espaco: int | None = None,
    ):

        from ui.componentes.ui_layout import UILayout

        return UILayout.centralizar_vertical(
            quantidade=quantidade,
            largura_tela=largura_tela,
            altura_tela=altura_tela,
            largura_item=largura_botao,
            altura_item=altura_botao,
            espaco=espaco,
        )

    # Gera botões de turmas
    @staticmethod
    def gerar_botoes_turmas(
        turmas: list,
        largura_botao: int | None = None,
        altura_botao: int | None = None,
    ):

        from ui.componentes.ui_layout import UILayout

        return UILayout.gerar_botoes_turmas(
            turmas=turmas,
            largura_botao=largura_botao,
            altura_botao=altura_botao,
        )

    # Gera grade de níveis
    @staticmethod
    def gerar_grade_niveis(
        quantidade: int,
        cols: int | None = None,
        tamanho: int | None = None,
        espaco: int | None = None,
        y_inicio: int | None = None,
        largura_tela: int | None = None,
    ):

        from ui.componentes.ui_layout import UILayout

        return UILayout.gerar_grade_niveis(
            quantidade=quantidade,
            cols=cols,
            tamanho=tamanho,
            espaco=espaco,
            y_inicio=y_inicio,
            largura_tela=largura_tela,
        )


LARGURA = GameConfig.LARGURA
ALTURA = GameConfig.ALTURA

BRANCO = GameConfig.BRANCO
PRETO = GameConfig.PRETO
CINZA = GameConfig.CINZA
VERDE = GameConfig.VERDE
VERMELHO = GameConfig.VERMELHO
AMARELO = GameConfig.AMARELO
AZUL_CLARO = GameConfig.AZUL_CLARO

ARQUIVO_PROGRESSO = GameConfig.ARQUIVO_PROGRESSO
ARQUIVO_RANKING = GameConfig.ARQUIVO_RANKING
ARQUIVO_NIVEIS = GameConfig.ARQUIVO_NIVEIS
ARQUIVO_CONFIG = GameConfig.ARQUIVO_CONFIG
ARQUIVO_TURMAS = GameConfig.ARQUIVO_TURMAS