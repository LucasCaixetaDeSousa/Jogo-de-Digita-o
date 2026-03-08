from __future__ import annotations
import pygame

from game_config import GameConfig
from ui.base_list_scene import BaseListScene
from ui.componentes.ui_list_item import UIListItemRenderer

class TelaEditorAlunos(BaseListScene):

    # Inicializa editor de alunos
    def __init__(self, tela, fontes, gerenciador_alunos, gerenciador_turmas, state):

        super().__init__(tela, fontes)

        self.ga = gerenciador_alunos
        self.gt = gerenciador_turmas
        self.state = state

        self.linha_h = 34
        self.top_y = 140

        self.scroll.item_altura = self.linha_h
        self.scroll.topo = self.top_y
        self.scroll.altura_tela = tela.get_height()

        self.aluno_sel = None
        self.confirmar_excluir = False

        self.botao_excluir = pygame.Rect(0, 0, 0, 0)

    # Reinicia tela
    def iniciar(self):

        self.scroll.reset()
        self.idx_sel = 0
        self.item_sel_id = None

        self.aluno_sel = None
        self.confirmar_excluir = False

        self._rebuild_lista()

    # Lista alunos
    def _listar_alunos(self):

        return self.ga.listar_alunos()

    # Reconstrói lista
    def _rebuild_lista(self):

        alunos = self._listar_alunos()
        self.rebuild_lista(alunos)

    # Exclui aluno
    def _excluir(self):

        if not self.aluno_sel:
            self.toast("Selecione um Aluno")
            return

        if not self.confirmar_excluir:
            self.confirmar_excluir = True
            self.toast("Clique em Confirmar!")
            return

        self.ga.remover(self.aluno_sel["nome"], self.aluno_sel["turma"])

        self.toast("Aluno removido!")

        self.confirmar_excluir = False
        self.aluno_sel = None
        self.item_sel_id = None

        self._rebuild_lista()

    # Atualiza tela
    def atualizar(self, eventos):

        self.aplicar_scroll(eventos, len(self.itens_rects))

        retorno = self.voltar_por_esc(eventos, "admin")
        if retorno:
            return retorno

        retorno = self.voltar_por_botao(eventos, "admin")
        if retorno:
            return retorno

        for e in eventos:

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                if self.botao_excluir.collidepoint(e.pos):
                    self._excluir()
                    return None

                selecionado = self.detectar_selecao(eventos)

                if selecionado is not None:

                    self.aluno_sel = selecionado
                    self.item_sel_id = selecionado
                    self.confirmar_excluir = False

                    return None

        return None

    # Desenha item da lista
    def _desenhar_item(self, aluno, rect, selecionado, hover):

        UIListItemRenderer.draw(
            tela=self.tela,
            rect=rect,
            texto="",
            fonte=self.fonte_peq,
            selecionado=selecionado,
            hover=hover,
        )

        cor = (
            GameConfig.VERDE
            if hover
            else GameConfig.AMARELO
            if selecionado
            else GameConfig.BRANCO
        )

        turma = self.gt.obter(aluno["turma"])
        nome_turma = turma.nome if turma else aluno["turma"]

        nome_img = self.fonte_peq.render(aluno["nome"], True, cor)
        turma_img = self.fonte_peq.render(nome_turma, True, cor)
        nivel_img = self.fonte_peq.render(f'Nível {aluno["nivel"]}', True, cor)

        self.tela.blit(nome_img, (rect.x + 12, rect.y + 6))
        self.tela.blit(turma_img, (rect.x + 320, rect.y + 6))
        self.tela.blit(nivel_img, (rect.x + 500, rect.y + 6))

    # Desenha tela
    def desenhar(self):

        self.desenhar_cabecalho("Editor — Alunos")

        self.botao_excluir = GameConfig.desenhar_botao(
            self.tela,
            "Excluir" if not self.confirmar_excluir else "Confirmar",
            self.fonte_peq,
            GameConfig.LARGURA - 160,
            30,
            130,
            45,
            excluir=True,
        )

        self._rebuild_lista()

        self.desenhar_lista(self._desenhar_item)

        self.desenhar_toast()