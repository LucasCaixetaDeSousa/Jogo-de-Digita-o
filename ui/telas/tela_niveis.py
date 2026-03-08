from __future__ import annotations
import pygame

from ui.base_scene import BaseScene
from game_config import GameConfig

class TelaNiveis(BaseScene):

    # Inicializa tela de níveis
    def __init__(self, tela, fontes, gerenciador, progresso, state):

        super().__init__(tela, fontes)

        self.gerenciador = gerenciador
        self.progresso = progresso
        self.state = state

        self.categoria = None

        self.botoes_categorias = {}

        self.botao_voltar = pygame.Rect(0, 0, 0, 0)
        self.botao_ranking = pygame.Rect(0, 0, 0, 0)
        self.botao_admin = pygame.Rect(0, 0, 0, 0)

        self.scroll_niveis = 0
        self._base_rects_niveis = []

    # Reinicia tela
    def iniciar(self):

        self.categoria = None
        self.scroll_niveis = 0
        self._base_rects_niveis = []

        self._criar_botoes_categorias()

    # Verifica se usuário é admin
    def _admin(self):

        return self.state.is_admin

    # Cria botões das categorias
    def _criar_botoes_categorias(self):

        categorias = [
            ("basico", "Básicos"),
            ("intermediario", "Intermediários"),
            ("avancado", "Avançados")
        ]

        pos = GameConfig.calcular_posicoes_centralizadas(
            len(categorias),
            GameConfig.LARGURA,
            GameConfig.ALTURA
        )

        self.botoes_categorias.clear()

        for i, (cat, txt) in enumerate(categorias):

            rect = pygame.Rect(
                pos[i][0],
                pos[i][1],
                GameConfig.BOTAO_LARGURA_PADRAO,
                GameConfig.BOTAO_ALTURA_PADRAO
            )

            self.botoes_categorias[cat] = (txt, rect)

    # Retorna título da categoria
    def _titulo_categoria(self):

        titulos = {
            "basico": "Básicos",
            "intermediario": "Intermediários",
            "avancado": "Avançados",
        }

        return titulos.get(self.categoria, self.categoria)

    # Cria botões dos níveis
    def _criar_botoes_niveis(self):

        lista = self.gerenciador.niveis[self.categoria]

        rects = GameConfig.gerar_grade_niveis(len(lista))

        self._base_rects_niveis = []

        for i, nivel in enumerate(lista):

            nivel.rect = rects[i]

            self._base_rects_niveis.append((rects[i], nivel))

        self.scroll_niveis = 0

        self._aplicar_scroll_niveis()

    # Verifica se scroll está ativo
    def _scroll_ativo(self) -> bool:

        return self.categoria == "avancado"

    # Calcula passo de linha dos níveis
    def _passo_linha_niveis(self) -> int:

        if not self._base_rects_niveis:
            return 70

        ys = sorted({r.y for r, _ in self._base_rects_niveis})

        if len(ys) >= 2:

            diffs = [
                ys[i + 1] - ys[i]
                for i in range(len(ys) - 1)
                if (ys[i + 1] - ys[i]) > 0
            ]

            if diffs:
                return min(diffs)

        r0 = self._base_rects_niveis[0][0]

        return r0.height + 20

    # Calcula total de linhas de níveis
    def _linhas_totais_niveis(self) -> int:

        if not self._base_rects_niveis:
            return 0

        ys = sorted({r.y for r, _ in self._base_rects_niveis})

        return len(ys)

    # Calcula linhas visíveis
    def _linhas_visiveis_niveis(self) -> int:

        if not self._base_rects_niveis:
            return 1

        passo = self._passo_linha_niveis()

        min_y = min(r.y for r, _ in self._base_rects_niveis)

        bottom = GameConfig.ALTURA - 40

        altura_disp = max(1, bottom - min_y)

        return max(1, altura_disp // passo)

    # Calcula scroll máximo
    def _max_scroll_niveis(self) -> int:

        total = self._linhas_totais_niveis()

        vis = self._linhas_visiveis_niveis()

        return max(0, total - vis)

    # Limita scroll
    def _limitar_scroll_niveis(self):

        if self.scroll_niveis < 0:
            self.scroll_niveis = 0

        mx = self._max_scroll_niveis()

        if self.scroll_niveis > mx:
            self.scroll_niveis = mx

    # Aplica scroll nos níveis
    def _aplicar_scroll_niveis(self):

        if not self._scroll_ativo():
            return

        self._limitar_scroll_niveis()

        passo = self._passo_linha_niveis()

        offset = self.scroll_niveis * passo

        for rect_base, nivel in self._base_rects_niveis:

            nivel.rect = rect_base.move(0, -offset)

    # Atualiza lógica da tela
    def atualizar(self, eventos):

        nome = self.state.nome
        turma = self.state.turma
        admin = self._admin()

        progresso_atual = 999999 if admin else self.progresso.obter_nivel(nome, turma)

        if self.categoria and self._scroll_ativo():
            self._aplicar_scroll_niveis()

        for e in eventos:

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:

                if self.categoria:
                    self.categoria = None
                    self.scroll_niveis = 0
                else:
                    self.state.logout()
                    return "login"

            if self.clicou_voltar(e):

                if self.categoria:
                    self.categoria = None
                    self.scroll_niveis = 0
                else:
                    self.state.logout()
                    return "login"

            if self.categoria and self._scroll_ativo():

                if e.type == pygame.MOUSEWHEEL:

                    self.scroll_niveis -= e.y
                    self._aplicar_scroll_niveis()

                if e.type == pygame.KEYDOWN:

                    if e.key == pygame.K_DOWN:
                        self.scroll_niveis += 1
                        self._aplicar_scroll_niveis()

                    elif e.key == pygame.K_UP:
                        self.scroll_niveis -= 1
                        self._aplicar_scroll_niveis()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                if self.botao_ranking.collidepoint(e.pos):
                    return "ranking"

                if admin and self.botao_admin.collidepoint(e.pos):
                    return "admin"

                if not self.categoria:

                    for chave, (_, rect) in self.botoes_categorias.items():

                        if rect.collidepoint(e.pos):

                            self.categoria = chave

                            self._criar_botoes_niveis()

                            break

                else:

                    if self._scroll_ativo():
                        self._aplicar_scroll_niveis()

                    for nivel in self.gerenciador.niveis[self.categoria]:

                        if not nivel.rect or not nivel.rect.collidepoint(e.pos):
                            continue

                        indice = self.gerenciador.indice_global(nivel.id)

                        if indice is None:
                            continue

                        if indice <= progresso_atual:

                            self.state.iniciar_nivel(nivel.id, self.categoria)

                            return "jogo"

        return None

    # Desenha botões fixos
    def _desenhar_botoes_fixos(self, admin: bool):

        self.botao_voltar = self.desenhar_voltar()

        self.botao_ranking = GameConfig.desenhar_botao(
            self.tela,
            "Ranking",
            self.fonte_peq,
            GameConfig.LARGURA - 230,
            GameConfig.VOLTAR_Y,
            largura=200,
            altura=40
        )

        if admin:

            self.botao_admin = GameConfig.desenhar_botao(
                self.tela,
                "Editores",
                self.fonte_peq,
                GameConfig.LARGURA - 230,
                GameConfig.VOLTAR_Y + 50,
                largura=200,
                altura=40
            )

    # Desenha menu de categorias
    def _desenhar_menu_categorias(self):

        GameConfig.desenhar_titulo(
            self.tela,
            "Níveis",
            self.fonte,
            GameConfig.LARGURA
        )

        for txt, rect in self.botoes_categorias.values():

            GameConfig.desenhar_botao(
                self.tela,
                txt,
                self.fonte_peq,
                rect.x,
                rect.y,
                largura=rect.width,
                altura=rect.height
            )

    # Desenha grade de níveis
    def _desenhar_grade_niveis(self, progresso_atual: int):

        GameConfig.desenhar_titulo(
            self.tela,
            self._titulo_categoria(),
            self.fonte,
            GameConfig.LARGURA
        )

        if self._scroll_ativo():
            self._aplicar_scroll_niveis()

        mouse = pygame.mouse.get_pos()

        for nivel in self.gerenciador.niveis[self.categoria]:

            if not nivel.rect:
                continue

            if self._scroll_ativo():
                if nivel.rect.bottom < 120 or nivel.rect.top > GameConfig.ALTURA - 30:
                    continue

            indice = self.gerenciador.indice_global(nivel.id)

            if indice is None:
                continue

            bloqueado = indice > progresso_atual
            concluido = indice < progresso_atual

            hover = nivel.rect.collidepoint(mouse)

            if bloqueado:
                cor = GameConfig.VERMELHO
            elif concluido:
                cor = GameConfig.VERDE
            else:
                cor = GameConfig.VERDE if hover else GameConfig.BRANCO

            pygame.draw.rect(
                self.tela,
                cor,
                nivel.rect,
                3,
                border_radius=GameConfig.BOTAO_RAIO
            )

            txt = self.fonte_peq.render(str(nivel.id), True, cor)

            self.tela.blit(
                txt,
                txt.get_rect(center=nivel.rect.center)
            )

    # Desenha tela
    def desenhar(self):

        self.desenhar_base()

        nome = self.state.nome
        turma = self.state.turma
        admin = self._admin()

        progresso_atual = 999999 if admin else self.progresso.obter_nivel(nome, turma)

        self._desenhar_botoes_fixos(admin)

        if not self.categoria:
            self._desenhar_menu_categorias()
        else:
            self._desenhar_grade_niveis(progresso_atual)