from __future__ import annotations

import pygame

from ui.base_scene import BaseScene
from game_config import GameConfig

class _RankingOnlineFallback:

    # Retorna ranking global
    def ranking_global(self, top=20):
        return []

    # Retorna ranking global por nível
    def ranking_global_nivel(self, nivel, top=20):
        return []

    # Retorna ranking por turma
    def ranking_turma(self, turma, top=20):
        return []

    # Retorna ranking por turma e nível
    def ranking_turma_nivel(self, turma, nivel, top=20):
        return []

    # Informa se servidor está online
    def servidor_online(self):
        return False

class TelaRanking(BaseScene):

    # Inicializa tela de ranking
    def __init__(self, tela, fontes, ranking, state, gerenciador_niveis):
        super().__init__(tela, fontes)

        self.ranking = ranking
        self.state = state
        self.gerenciador = gerenciador_niveis

        self.ranking_online = self._criar_ranking_online()

        self.estado = "tipo"
        self.pilha = []

        self.tipo = None
        self.sub = None
        self.categoria = None
        self.nivel = None

        self.lista = []
        self.scroll = 0

        self.scroll_niveis = 0
        self._grid_niveis_base = []
        self.botoes_niveis = []

        self.linha_altura = 28
        self.top_y = 0
        self.linhas_visiveis = 1

        self.botao_global = pygame.Rect(0, 0, 0, 0)
        self.botao_turma = pygame.Rect(0, 0, 0, 0)

        self.botao_geral = pygame.Rect(0, 0, 0, 0)
        self.botao_nivel = pygame.Rect(0, 0, 0, 0)

        self.botoes_categorias = {}

    # Reinicia tela
    def iniciar(self):
        self.estado = "tipo"
        self.pilha.clear()

        self.tipo = None
        self.sub = None
        self.categoria = None
        self.nivel = None

        self.lista = []
        self.scroll = 0

        self.scroll_niveis = 0
        self._grid_niveis_base = []
        self.botoes_niveis = []

    # Cria serviço de ranking online
    def _criar_ranking_online(self):
        try:
            from services.ranking_online import RankingOnline
            return RankingOnline()
        except Exception:
            return _RankingOnlineFallback()

    # Avança para novo estado
    def _ir(self, estado):
        self.pilha.append(self.estado)
        self.estado = estado

    # Volta para estado anterior
    def _voltar(self):
        if not self.pilha:
            return "niveis"

        self.estado = self.pilha.pop()

        if self.estado != "mostrar":
            self.scroll = 0

        if self.estado != "niveis":
            self.scroll_niveis = 0

        return None

    # Retorna título do resultado
    def _titulo_resultado(self):
        titulo_tipo = "Global" if self.tipo == "global" else "Por Turma"

        if self.sub == "geral":
            return f"Ranking {titulo_tipo} — Geral"

        return f"Ranking {titulo_tipo} — Nível {self.nivel}"

    # Retorna título da categoria
    def _titulo_categoria(self):
        titulos = {
            "basico": "Básicos",
            "intermediario": "Intermediários",
            "avancado": "Avançados",
        }
        return titulos.get(self.categoria, self.categoria)

    # Normaliza ranking vindo do online
    def _normalizar_online(self, dados):
        lista = []

        if not isinstance(dados, list):
            return lista

        for item in dados:
            if not isinstance(item, dict):
                continue

            nome = item.get("nome", "")
            turma = item.get("turma", "")
            pontos = int(item.get("pontos", 0))
            tempo = int(item.get("tempo", 9999))

            if pontos <= 0:
                continue

            lista.append((nome, turma, tempo, pontos))

        return lista

    # Verifica se ranking online está disponível
    def _ranking_online_disponivel(self):
        try:
            return self.ranking_online is not None and self.ranking_online.servidor_online()
        except Exception:
            return False

    # Gera ranking atual
    def _gerar_ranking(self):
        turma = self.state.turma
        lista_online = None

        if self._ranking_online_disponivel():
            try:
                if self.tipo == "global":
                    if self.sub == "geral":
                        lista_online = self._normalizar_online(
                            self.ranking_online.ranking_global(top=30)
                        )
                    else:
                        lista_online = self._normalizar_online(
                            self.ranking_online.ranking_global_nivel(self.nivel, top=30)
                        )
                else:
                    if self.sub == "geral":
                        lista_online = self._normalizar_online(
                            self.ranking_online.ranking_turma(turma, top=30)
                        )
                    else:
                        lista_online = self._normalizar_online(
                            self.ranking_online.ranking_turma_nivel(turma, self.nivel, top=30)
                        )
            except Exception:
                lista_online = None

        if lista_online is not None:
            self.lista = lista_online
        else:
            if self.tipo == "global":
                if self.sub == "geral":
                    self.lista = self.ranking.global_geral(top=30)
                else:
                    self.lista = self.ranking.global_nivel(self.nivel, top=30)
            else:
                if self.sub == "geral":
                    self.lista = self.ranking.turma_geral(turma)
                else:
                    self.lista = self.ranking.turma_nivel(turma, self.nivel)

        self.scroll = 0
        self._limitar_scroll()

    # Retorna scroll máximo dos resultados
    def _max_scroll(self):
        return max(0, len(self.lista) - self.linhas_visiveis)

    # Limita scroll dos resultados
    def _limitar_scroll(self):
        if self.scroll < 0:
            self.scroll = 0

        max_scroll = self._max_scroll()

        if self.scroll > max_scroll:
            self.scroll = max_scroll

    # Cria botões de categorias
    def _criar_botoes_categorias(self):
        categorias = [
            ("basico", "Básicos"),
            ("intermediario", "Intermediários"),
            ("avancado", "Avançados"),
        ]

        posicoes = GameConfig.calcular_posicoes_centralizadas(
            len(categorias),
            GameConfig.LARGURA,
            GameConfig.ALTURA
        )

        self.botoes_categorias.clear()

        for i, (chave, texto) in enumerate(categorias):
            rect = pygame.Rect(
                posicoes[i][0],
                posicoes[i][1],
                GameConfig.BOTAO_LARGURA_PADRAO,
                GameConfig.BOTAO_ALTURA_PADRAO
            )
            self.botoes_categorias[chave] = (texto, rect)

    # Cria grade de níveis
    def _criar_botoes_niveis(self):
        lista = self.gerenciador.niveis[self.categoria]
        rects = GameConfig.gerar_grade_niveis(len(lista))

        self._grid_niveis_base = []

        for i, nivel in enumerate(lista):
            base = rects[i]
            self._grid_niveis_base.append((base, nivel))

        self.scroll_niveis = 0
        self._atualizar_rects_niveis()

    # Calcula passo entre linhas de níveis
    def _passo_linha_niveis(self):
        ys = sorted({r.y for r, _ in self._grid_niveis_base})

        if len(ys) >= 2:
            diferencas = [
                ys[i + 1] - ys[i]
                for i in range(len(ys) - 1)
                if (ys[i + 1] - ys[i]) > 0
            ]
            if diferencas:
                return min(diferencas)

        if self._grid_niveis_base:
            rect = self._grid_niveis_base[0][0]
            return rect.height + 20

        return 70

    # Retorna total de linhas de níveis
    def _linhas_totais_niveis(self):
        ys = sorted({r.y for r, _ in self._grid_niveis_base})
        return len(ys)

    # Retorna linhas visíveis de níveis
    def _linhas_visiveis_niveis(self):
        if not self._grid_niveis_base:
            return 1

        passo = self._passo_linha_niveis()
        min_y = min(r.y for r, _ in self._grid_niveis_base)

        bottom = GameConfig.ALTURA - 40
        altura_disponivel = max(1, bottom - min_y)

        return max(1, altura_disponivel // passo)

    # Retorna scroll máximo dos níveis
    def _max_scroll_niveis(self):
        total = self._linhas_totais_niveis()
        visiveis = self._linhas_visiveis_niveis()
        return max(0, total - visiveis)

    # Limita scroll dos níveis
    def _limitar_scroll_niveis(self):
        if self.scroll_niveis < 0:
            self.scroll_niveis = 0

        max_scroll = self._max_scroll_niveis()

        if self.scroll_niveis > max_scroll:
            self.scroll_niveis = max_scroll

    # Atualiza posição dos botões de níveis
    def _atualizar_rects_niveis(self):
        passo = self._passo_linha_niveis()
        offset = self.scroll_niveis * passo

        self.botoes_niveis = []

        for base, nivel in self._grid_niveis_base:
            atual = base.move(0, -offset)
            self.botoes_niveis.append((atual, nivel))

    # Atualiza tela
    def atualizar(self, eventos):
        mouse = pygame.mouse.get_pos()

        if self.estado == "niveis":
            self._atualizar_rects_niveis()

        for e in eventos:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return self._voltar()

            if self.clicou_voltar(e):
                return self._voltar()

            if self.estado == "mostrar":
                if e.type == pygame.MOUSEWHEEL:
                    self.scroll -= e.y
                    self._limitar_scroll()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.scroll += 1
                        self._limitar_scroll()
                    elif e.key == pygame.K_UP:
                        self.scroll -= 1
                        self._limitar_scroll()

            if self.estado == "niveis":
                if e.type == pygame.MOUSEWHEEL:
                    self.scroll_niveis -= e.y
                    self._limitar_scroll_niveis()
                    self._atualizar_rects_niveis()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.scroll_niveis += 1
                        self._limitar_scroll_niveis()
                        self._atualizar_rects_niveis()
                    elif e.key == pygame.K_UP:
                        self.scroll_niveis -= 1
                        self._limitar_scroll_niveis()
                        self._atualizar_rects_niveis()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.estado == "tipo":
                    if self.botao_global.collidepoint(mouse):
                        self.tipo = "global"
                        self._ir("modo")

                    elif self.botao_turma.collidepoint(mouse):
                        self.tipo = "turma"
                        self._ir("modo")

                elif self.estado == "modo":
                    if self.botao_geral.collidepoint(mouse):
                        self.sub = "geral"
                        self._gerar_ranking()
                        self._ir("mostrar")

                    elif self.botao_nivel.collidepoint(mouse):
                        self.sub = "nivel"
                        self._criar_botoes_categorias()
                        self._ir("categoria")

                elif self.estado == "categoria":
                    for categoria, (_, rect) in self.botoes_categorias.items():
                        if rect.collidepoint(mouse):
                            self.categoria = categoria
                            self._criar_botoes_niveis()
                            self._ir("niveis")
                            break

                elif self.estado == "niveis":
                    for rect, nivel in self.botoes_niveis:
                        if rect and rect.collidepoint(mouse):
                            self.nivel = nivel.id
                            self._gerar_ranking()
                            self._ir("mostrar")
                            break

        return None

    # Desenha tela de escolha do tipo
    def _desenhar_estado_tipo(self):
        GameConfig.desenhar_titulo(
            self.tela,
            "Ranking",
            self.fonte,
            GameConfig.LARGURA
        )

        y = (GameConfig.ALTURA // 2) - (GameConfig.BOTAO_ALTURA_PADRAO // 2)

        rect_global, rect_turma = self._rects_lado_a_lado(
            2,
            y,
            GameConfig.BOTAO_LARGURA_PADRAO,
            GameConfig.BOTAO_ALTURA_PADRAO
        )

        self.botao_global = GameConfig.desenhar_botao(
            self.tela,
            "Global",
            self.fonte_peq,
            rect_global.x,
            rect_global.y,
            largura=rect_global.width,
            altura=rect_global.height
        )

        self.botao_turma = GameConfig.desenhar_botao(
            self.tela,
            "Turma",
            self.fonte_peq,
            rect_turma.x,
            rect_turma.y,
            largura=rect_turma.width,
            altura=rect_turma.height
        )

    # Desenha tela de escolha do modo
    def _desenhar_estado_modo(self):
        GameConfig.desenhar_titulo(
            self.tela,
            "Tipo de ranking",
            self.fonte,
            GameConfig.LARGURA
        )

        y = (GameConfig.ALTURA // 2) - (GameConfig.BOTAO_ALTURA_PADRAO // 2)

        rect_geral, rect_nivel = self._rects_lado_a_lado(
            2,
            y,
            GameConfig.BOTAO_LARGURA_PADRAO,
            GameConfig.BOTAO_ALTURA_PADRAO
        )

        self.botao_geral = GameConfig.desenhar_botao(
            self.tela,
            "Geral",
            self.fonte_peq,
            rect_geral.x,
            rect_geral.y,
            largura=rect_geral.width,
            altura=rect_geral.height
        )

        self.botao_nivel = GameConfig.desenhar_botao(
            self.tela,
            "Por nível",
            self.fonte_peq,
            rect_nivel.x,
            rect_nivel.y,
            largura=rect_nivel.width,
            altura=rect_nivel.height
        )

    # Desenha tela de categorias
    def _desenhar_estado_categoria(self):
        GameConfig.desenhar_titulo(
            self.tela,
            "Níveis",
            self.fonte,
            GameConfig.LARGURA
        )

        for texto, rect in self.botoes_categorias.values():
            GameConfig.desenhar_botao(
                self.tela,
                texto,
                self.fonte_peq,
                rect.x,
                rect.y,
                largura=rect.width,
                altura=rect.height
            )

    # Desenha tela de níveis
    def _desenhar_estado_niveis(self):
        GameConfig.desenhar_titulo(
            self.tela,
            self._titulo_categoria(),
            self.fonte,
            GameConfig.LARGURA
        )

        self._limitar_scroll_niveis()
        self._atualizar_rects_niveis()

        mouse = pygame.mouse.get_pos()

        for rect, nivel in self.botoes_niveis:
            if not rect:
                continue

            if rect.bottom < 120 or rect.top > GameConfig.ALTURA - 30:
                continue

            hover = rect.collidepoint(mouse)
            cor = GameConfig.VERDE if hover else GameConfig.BRANCO

            pygame.draw.rect(
                self.tela,
                cor,
                rect,
                3,
                border_radius=GameConfig.BOTAO_RAIO
            )

            texto = self.fonte_peq.render(str(nivel.id), True, cor)
            self.tela.blit(texto, texto.get_rect(center=rect.center))

    # Desenha resultados do ranking
    def _desenhar_estado_mostrar(self):
        GameConfig.desenhar_titulo(
            self.tela,
            self._titulo_resultado(),
            self.fonte,
            GameConfig.LARGURA
        )

        if not self.lista:
            msg = self.fonte_peq.render(
                "Sem dados no ranking ainda.",
                True,
                GameConfig.BRANCO
            )
            self.tela.blit(
                msg,
                msg.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2))
            )
            return

        x_rank = 70
        x_nome = 140
        x_turma = 520
        x_tempo = 640
        x_pontos = 780

        y = 130
        self.top_y = y + 34

        self.tela.blit(self.fonte_peq.render("#", True, GameConfig.BRANCO), (x_rank, y))
        self.tela.blit(self.fonte_peq.render("NOME", True, GameConfig.BRANCO), (x_nome, y))
        self.tela.blit(self.fonte_peq.render("Turma", True, GameConfig.BRANCO), (x_turma, y))
        self.tela.blit(self.fonte_peq.render("TEMPO", True, GameConfig.BRANCO), (x_tempo, y))
        self.tela.blit(self.fonte_peq.render("PONTOS", True, GameConfig.BRANCO), (x_pontos, y))

        y_inicio = self.top_y
        margem_baixo = 20

        self.linhas_visiveis = max(
            1,
            (GameConfig.ALTURA - y_inicio - margem_baixo) // self.linha_altura
        )

        self._limitar_scroll()

        inicio = self.scroll
        fim = min(len(self.lista), inicio + self.linhas_visiveis)

        y = y_inicio

        for i in range(inicio, fim):
            posicao = i + 1
            nome, turma, tempo, pontos = self.lista[i]

            try:
                tempo = int(tempo)
                if tempo >= 9999:
                    tempo_str = "--:--"
                else:
                    minutos = tempo // 60
                    segundos = tempo % 60
                    tempo_str = f"{minutos:02}:{segundos:02}"
            except Exception:
                tempo_str = "--:--"

            if posicao == 1:
                cor_pos = GameConfig.OURO
            elif posicao == 2:
                cor_pos = GameConfig.PRATA
            elif posicao == 3:
                cor_pos = GameConfig.BRONZE
            else:
                cor_pos = GameConfig.BRANCO

            self.tela.blit(self.fonte_peq.render(str(posicao), True, cor_pos), (x_rank, y))
            self.tela.blit(self.fonte_peq.render(str(nome), True, GameConfig.BRANCO), (x_nome, y))
            self.tela.blit(self.fonte_peq.render(str(turma), True, GameConfig.BRANCO), (x_turma, y))
            self.tela.blit(self.fonte_peq.render(str(tempo_str), True, GameConfig.BRANCO), (x_tempo, y))
            self.tela.blit(self.fonte_peq.render(str(pontos), True, GameConfig.AMARELO), (x_pontos, y))

            y += self.linha_altura

    # Desenha tela
    def desenhar(self):
        self.desenhar_base()
        self.desenhar_voltar()

        if self.estado == "tipo":
            self._desenhar_estado_tipo()
            return

        if self.estado == "modo":
            self._desenhar_estado_modo()
            return

        if self.estado == "categoria":
            self._desenhar_estado_categoria()
            return

        if self.estado == "niveis":
            self._desenhar_estado_niveis()
            return

        if self.estado == "mostrar":
            self._desenhar_estado_mostrar()