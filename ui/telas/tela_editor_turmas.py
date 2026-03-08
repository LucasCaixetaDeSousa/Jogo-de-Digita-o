from __future__ import annotations
import pygame

from game_config import GameConfig
from ui.base_list_scene import BaseListScene
from ui.componentes.ui_list_item import UIListItemRenderer

class TelaEditorTurmas(BaseListScene):

    # Inicializa editor de turmas
    def __init__(self, tela, fontes, gerenciador_turmas, gerenciador_alunos, state):

        super().__init__(tela, fontes)

        self.gt = gerenciador_turmas
        self.ga = gerenciador_alunos
        self.state = state

        self.linha_h = 34
        self.top_y = 140

        self.scroll.item_altura = self.linha_h
        self.scroll.topo = self.top_y
        self.scroll.altura_tela = tela.get_height()

        self.turma_sel_id = None
        self.confirmar_excluir = False

        self.modo_novo = False
        self.nome_turma = ""

        self.botao_novo = pygame.Rect(0,0,0,0)
        self.botao_editar = pygame.Rect(0,0,0,0)
        self.botao_excluir = pygame.Rect(0,0,0,0)
        self.botao_salvar = pygame.Rect(0,0,0,0)

        self.campo_nome = pygame.Rect(40,180,GameConfig.LARGURA-220,55)

        self._cursor_on = True
        self._cursor_last = pygame.time.get_ticks()
        self._cursor_interval = 450

    # Reinicia tela
    def iniciar(self):

        self.estado = "lista"
        self.scroll.reset()

        self.idx_sel = 0
        self.item_sel_id = None
        self.turma_sel_id = None

        self.confirmar_excluir = False

        self._rebuild_lista()

    # Lista turmas
    def _listar_turmas(self):

        return self.gt.listar()

    # Reconstrói lista
    def _rebuild_lista(self):

        turmas = self._listar_turmas()
        ids = [str(t.id) for t in turmas]

        self.rebuild_lista(ids)

    # Fecha edição
    def _fechar_edicao(self):

        self.estado = "lista"
        self.confirmar_excluir = False

        self._rebuild_lista()

    # Abre criação de turma
    def _abrir_novo(self):

        self.estado = "editar"

        self.modo_novo = True
        self.turma_sel_id = None

        self.nome_turma = ""

    # Abre edição de turma
    def _abrir_editar(self, turma_id):

        turma = self.gt.obter(turma_id)

        if not turma:
            self.toast("Turma não encontrada.")
            return

        self.estado = "editar"

        self.modo_novo = False
        self.turma_sel_id = turma_id

        self.nome_turma = turma.nome

    # Salva turma
    def _salvar(self):

        nome = self.nome_turma.strip()

        if len(nome) < 2:
            self.toast("Nome inválido.")
            return

        if self.modo_novo:

            novo_id = self.gt.proximo_id()
            self.gt.adicionar(novo_id, nome)

            self.toast(f"Criada: {nome}")

        else:

            self.gt.editar(self.turma_sel_id, nome)

            self.toast(f"Editada: {nome}")

        self.estado = "lista"
        self._rebuild_lista()

    # Exclui turma
    def _excluir(self):

        if not self.turma_sel_id:
            self.toast("Selecione uma turma.")
            return

        if not self.confirmar_excluir:

            self.confirmar_excluir = True
            self.toast("Clique em Confirmar.")

            return

        self.gt.remover(self.turma_sel_id)

        self.toast("Turma removida.")

        self.confirmar_excluir = False
        self.turma_sel_id = None

        self.estado = "lista"

        self._rebuild_lista()

    # Processa input de texto
    def _handle_input(self, e):

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_RETURN:
                self._salvar()
                return

            if e.key == pygame.K_BACKSPACE:
                self.nome_turma = self.nome_turma[:-1]
                return

            if not e.unicode:
                return

            if len(self.nome_turma) < 40:
                self.nome_turma += e.unicode

    # Atualiza cursor
    def _tick_cursor(self):

        agora = pygame.time.get_ticks()

        if agora - self._cursor_last > self._cursor_interval:

            self._cursor_on = not self._cursor_on
            self._cursor_last = agora

    # Atualiza tela
    def atualizar(self, eventos):

        if self.estado == "lista":
            self.aplicar_scroll(eventos, len(self.itens_rects))

        if self.estado == "editar":
            self._tick_cursor()

        for e in eventos:

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:

                if self.estado == "editar":
                    self._fechar_edicao()
                    return None

                return "admin"

            if self.estado == "editar":
                self._handle_input(e)

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                if self.botao_voltar.collidepoint(e.pos):

                    if self.estado == "editar":
                        self._fechar_edicao()
                        return None

                    return "admin"

                if self.estado == "lista":

                    if self.botao_novo.collidepoint(e.pos):
                        self._abrir_novo()
                        return None

                    if self.botao_editar.collidepoint(e.pos):

                        if self.turma_sel_id:
                            self._abrir_editar(self.turma_sel_id)
                        else:
                            self.toast("Selecione uma turma.")

                        return None

                    if self.botao_excluir.collidepoint(e.pos):
                        self._excluir()
                        return None

                    selecionado = self.detectar_selecao(eventos)

                    if selecionado:

                        self.turma_sel_id = selecionado
                        self.confirmar_excluir = False

                        return None

                else:

                    if self.campo_nome.collidepoint(e.pos):
                        return None

                    if self.botao_salvar.collidepoint(e.pos):
                        self._salvar()
                        return None

        return None

    # Desenha item da lista
    def _desenhar_item(self, tid, rect, selecionado, hover):

        UIListItemRenderer.draw(
            self.tela,
            rect,
            "",
            self.fonte_peq,
            selecionado,
            hover
        )

        cor = (
            GameConfig.VERDE
            if hover
            else GameConfig.AMARELO
            if selecionado
            else GameConfig.BRANCO
        )

        turma = self.gt.obter(tid)
        nome = turma.nome if turma else ""

        txt = self.fonte_peq.render(nome, True, cor)

        self.tela.blit(txt, (rect.x + 12, rect.y + 6))

    # Desenha lista
    def _desenhar_lista(self):

        self.desenhar_cabecalho("Editor — Turmas")

        self.botao_novo = GameConfig.desenhar_botao(
            self.tela,"Nova",self.fonte_peq,
            GameConfig.LARGURA-160,30,130,45
        )

        self.botao_editar = GameConfig.desenhar_botao(
            self.tela,"Editar",self.fonte_peq,
            GameConfig.LARGURA-160,85,130,45
        )

        self.botao_excluir = GameConfig.desenhar_botao(
            self.tela,
            "Excluir" if not self.confirmar_excluir else "Confirmar",
            self.fonte_peq,
            GameConfig.LARGURA-160,
            140,
            130,
            45,
            excluir=True
        )

        self._rebuild_lista()

        self.desenhar_lista(self._desenhar_item)

        self.desenhar_toast()

    # Desenha edição
    def _desenhar_edicao(self):

        self.desenhar_voltar()

        self.botao_salvar = GameConfig.desenhar_botao(
            self.tela,"Salvar",self.fonte_peq,
            GameConfig.LARGURA-160,30,130,45
        )

        titulo = (
            "Nova Turma"
            if self.modo_novo
            else f"Editar Turma {self.turma_sel_id}"
        )

        GameConfig.desenhar_titulo(
            self.tela,
            titulo,
            self.fonte,
            GameConfig.LARGURA
        )

        pygame.draw.rect(self.tela,GameConfig.CINZA,self.campo_nome)
        pygame.draw.rect(self.tela,GameConfig.AMARELO,self.campo_nome,2,border_radius=8)

        texto = self.nome_turma

        if self._cursor_on:
            texto += "_"

        img = self.fonte_peq.render(texto,True,GameConfig.BRANCO)

        self.tela.blit(img,(self.campo_nome.x+12,self.campo_nome.y+14))

        self.desenhar_toast()

    # Desenha tela
    def desenhar(self):

        GameConfig.desenhar_fundo(self.tela)

        if self.estado == "lista":
            self._desenhar_lista()
            return

        self._desenhar_edicao()