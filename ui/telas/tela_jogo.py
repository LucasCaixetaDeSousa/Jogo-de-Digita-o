from __future__ import annotations

import pygame

from ui.base_scene import BaseScene
from game_config import GameConfig
from logic.motor_digitacao import MotorDigitacao
from logic.estatisticas import Estatisticas
from logic.pontuacao import calcular_pontuacao

class TelaJogo(BaseScene):

    # Inicializa a tela do jogo
    def __init__(self, tela, fontes, sons, gerenciador_niveis, state, events):
        super().__init__(tela, fontes)

        self.state = state
        self.events = events
        self.gerenciador = gerenciador_niveis

        self.som_acerto, self.som_erro = sons

        self.motor = None
        self.nivel = None

        self.stats = Estatisticas()

        self.pontos = 0
        self.erros = 0
        self._ultimo_combo_bonus = 0

        self.nivel_concluido = False
        self.finalizado = False

        self.botao_proximo = pygame.Rect(
            GameConfig.LARGURA // 2 - 90,
            GameConfig.ALTURA // 2 + 80,
            180,
            50
        )

    # Inicia um nível
    def iniciar(self):

        nivel_id = self.state.nivel_atual
        self.nivel = self.gerenciador.obter_nivel_por_id(nivel_id)

        self.motor = MotorDigitacao(
            self.nivel.palavras,
            self.nivel.repeticoes
        )

        self.stats.reset()

        self.pontos = 0
        self.erros = 0
        self._ultimo_combo_bonus = 0

        self.nivel_concluido = False
        self.finalizado = False

    # Finaliza o nível atual
    def _finalizar_nivel(self):

        if self.finalizado:
            return

        self.stats.finalizar()
        tempo_total = self.stats.tempo()

        pontos = calcular_pontuacao(
            self.motor.acertos,
            self.motor.erros,
            tempo_total,
            self.motor.combo_bonus
        )

        self.pontos = pontos

        self.events.emit(
            "nivel_completo",
            {
                "nome": self.state.nome,
                "turma": self.state.turma,
                "nivel": self.nivel.id,
                "pontos": pontos,
                "tempo": tempo_total
            }
        )

        self.finalizado = True

    # Avança para o próximo nível
    def _proximo_nivel(self):

        indice = self.gerenciador.indice_global(self.nivel.id)
        prox = self.gerenciador.obter_nivel_por_indice(indice + 1)

        if prox:
            self.state.iniciar_nivel(prox.id)
            return "jogo"

        return "niveis"

    # Atualiza pontuação durante o jogo
    def _aplicar_pontuacao_ao_vivo(self, resultado: str):

        if resultado == "acerto":

            self.pontos += 10

            bonus_atual = int(getattr(self.motor, "combo_bonus", 0))
            delta = bonus_atual - self._ultimo_combo_bonus

            if delta > 0:
                self.pontos += delta
                self._ultimo_combo_bonus = bonus_atual

        elif resultado == "erro":

            self.pontos -= 5

            if self.pontos < 0:
                self.pontos = 0

    # Atualiza lógica do jogo
    def atualizar(self, eventos):

        if not self.motor:
            return None

        for e in eventos:

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "niveis"

            if self.clicou_voltar(e):
                return "niveis"

            if self.nivel_concluido:

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                    if self.botao_proximo.collidepoint(e.pos):
                        return self._proximo_nivel()

                continue

            if e.type == pygame.KEYDOWN and e.unicode:

                resultado = self.motor.digitar(e.unicode)

                if resultado == "acerto":

                    self.som_acerto.play()
                    self.stats.registrar_acerto()

                    self._aplicar_pontuacao_ao_vivo("acerto")

                elif resultado == "erro":

                    self.som_erro.play()
                    self.stats.registrar_erro()

                    self.erros += 1

                    self._aplicar_pontuacao_ao_vivo("erro")

                elif resultado == "nivel_concluido":

                    self.nivel_concluido = True

                    self._finalizar_nivel()

        return None

    # Desenha topo da tela
    def _desenhar_topo(self):

        self.desenhar_voltar()

        titulo = self.fonte.render(
            f"NÍVEL {self.nivel.id}",
            True,
            GameConfig.VERDE
        )

        self.tela.blit(
            titulo,
            titulo.get_rect(center=(GameConfig.LARGURA // 2, 50))
        )

        pontos_txt = self.fonte_peq.render(
            f"Pontos: {self.pontos}",
            True,
            GameConfig.AMARELO
        )

        self.tela.blit(
            pontos_txt,
            (GameConfig.LARGURA - pontos_txt.get_width() - 20, 20)
        )

        tempo_txt = self.fonte_peq.render(
            f"Tempo: {self.stats.tempo_formatado()}",
            True,
            GameConfig.AMARELO
        )

        self.tela.blit(
            tempo_txt,
            (GameConfig.LARGURA - tempo_txt.get_width() - 20, 45)
        )

    # Desenha rodapé da tela
    def _desenhar_rodape(self):

        aluno_txt = self.fonte_peq.render(
            f"{self.state.nome} - Turma {self.state.turma}",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(
            aluno_txt,
            aluno_txt.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA - 40))
        )

    # Desenha texto de digitação
    def _desenhar_jogo(self):

        texto = self.motor.texto
        indice = self.motor.indice

        antes = texto[:indice]
        atual = texto[indice:indice + 1]
        depois = texto[indice + 1:]

        y = GameConfig.ALTURA // 2 - 40

        img_antes = self.fonte.render(antes, True, GameConfig.VERDE)

        cor_atual = GameConfig.VERMELHO if self.motor.erro else GameConfig.AMARELO
        img_atual = self.fonte.render(atual, True, cor_atual)

        img_depois = self.fonte.render(depois, True, GameConfig.BRANCO)

        largura = (
            img_antes.get_width()
            + img_atual.get_width()
            + img_depois.get_width()
        )

        x = (GameConfig.LARGURA - largura) // 2

        self.tela.blit(img_antes, (x, y))
        x += img_antes.get_width()

        self.tela.blit(img_atual, (x, y))
        x += img_atual.get_width()

        self.tela.blit(img_depois, (x, y))

        rep_txt = self.fonte_peq.render(
            f"Repetição {self.motor.reps}/{self.motor.repeticoes}",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(
            rep_txt,
            rep_txt.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2 + 20))
        )

    # Desenha tela final do nível
    def _desenhar_tela_final(self):

        msg = self.fonte.render(
            "NÍVEL CONCLUÍDO!",
            True,
            GameConfig.VERDE
        )

        self.tela.blit(
            msg,
            msg.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2 - 60))
        )

        precisao = self.stats.precisao()

        stats = self.fonte_peq.render(
            f"Erros: {self.erros}    Precisão: {precisao}%",
            True,
            GameConfig.AMARELO
        )

        self.tela.blit(
            stats,
            stats.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2 - 20))
        )

        GameConfig.desenhar_botao(
            self.tela,
            "Próximo",
            self.fonte_peq,
            self.botao_proximo.x,
            self.botao_proximo.y,
            largura=self.botao_proximo.width,
            altura=self.botao_proximo.height
        )

    # Desenha tela
    def desenhar(self):

        self.desenhar_base()

        if not self.motor or not self.nivel:
            return

        self._desenhar_topo()
        self._desenhar_rodape()

        if not self.nivel_concluido:
            self._desenhar_jogo()
        else:
            self._desenhar_tela_final()