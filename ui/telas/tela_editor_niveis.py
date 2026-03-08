from __future__ import annotations

import pygame
from game_config import GameConfig
from modules.gerenciador_niveis import GerenciadorNiveis

from ui.base_list_scene import BaseListScene
from ui.componentes.ui_list_item import UIListItemRenderer


class TelaEditorNiveis(BaseListScene):

    def __init__(self, tela, fontes, gerenciador: GerenciadorNiveis, state):
        super().__init__(tela, fontes)

        self.gerenciador = gerenciador
        self.state = state

        self.linha_h = 34
        self.top_y = 140

        self.scroll.item_altura = self.linha_h
        self.scroll.topo = self.top_y
        self.scroll.altura_tela = tela.get_height()

        self.nivel_sel_id = None

        self.modo_novo = False
        self.texto = ""
        self.repeticoes = "5"
        self.campo_ativo = "texto"

        self.confirmar_excluir = False

        self.botao_novo = pygame.Rect(0,0,0,0)
        self.botao_editar = pygame.Rect(0,0,0,0)
        self.botao_excluir = pygame.Rect(0,0,0,0)
        self.botao_salvar = pygame.Rect(0,0,0,0)

        self.campo_texto = pygame.Rect(40,160,GameConfig.LARGURA-220,80)
        self.campo_rep = pygame.Rect(40,260,180,45)

        self._cursor_on = True
        self._cursor_last = pygame.time.get_ticks()
        self._cursor_interval = 450

        self._bk_held = False
        self._bk_next_ms = 0
        self._bk_first_delay = 240
        self._bk_repeat = 45

    # ==================================================
    # INICIAR
    # ==================================================

    def iniciar(self):

        self.estado = "lista"
        self.scroll.reset()

        self.idx_sel = 0
        self.item_sel_id = None
        self.nivel_sel_id = None

        self.confirmar_excluir = False
        self._bk_held = False

        self._rebuild_lista()

    # ==================================================
    # LISTA
    # ==================================================

    def _avancados(self):
        return self.gerenciador.niveis.get("avancado", [])

    def _rebuild_lista(self):

        niveis = self._avancados()

        ids = [str(n.id) for n in niveis]

        self.rebuild_lista(ids)

    # ==================================================
    # FECHAR EDIÇÃO
    # ==================================================

    def _fechar_edicao(self):

        self.estado = "lista"
        self.confirmar_excluir = False
        self._bk_held = False

        self._rebuild_lista()

    # ==================================================
    # ABRIR
    # ==================================================

    def _abrir_novo(self):

        self.estado = "editar"

        self.modo_novo = True
        self.nivel_sel_id = None

        self.texto = ""
        self.repeticoes = "5"

        self.campo_ativo = "texto"

    def _abrir_editar(self, nivel_id):

        n = self.gerenciador.obter_nivel_por_id(nivel_id)

        if not n:
            self.toast("Nível não encontrado.")
            return

        self.estado = "editar"

        self.modo_novo = False
        self.nivel_sel_id = str(n.id)

        self.texto = str(n.palavras)
        self.repeticoes = str(n.repeticoes)

        self.campo_ativo = "texto"

    # ==================================================
    # SALVAR
    # ==================================================

    def _salvar(self):

        texto = self.texto.strip()

        if len(texto) < 5:
            self.toast("Texto muito curto.")
            return

        try:
            rep = int(self.repeticoes)
        except ValueError:
            self.toast("Repetições inválidas.")
            return

        if rep <= 0:
            self.toast("Repetições inválidas.")
            return

        if self.modo_novo:

            novo_id = self.gerenciador.proximo_id_avancado()

            self.gerenciador.adicionar_nivel(
                "avancado",
                novo_id,
                novo_id,
                texto,
                rep
            )

            self.toast(f"Criado: {novo_id}")

        else:

            self.gerenciador.editar_nivel(
                self.nivel_sel_id,
                palavras=texto,
                repeticoes=rep
            )

            self.toast(f"Salvo: {self.nivel_sel_id}")

        self.estado = "lista"
        self._rebuild_lista()

    # ==================================================
    # EXCLUIR
    # ==================================================

    def _excluir(self):

        if not self.nivel_sel_id:
            self.toast("Selecione um nível.")
            return

        if not self.confirmar_excluir:

            self.confirmar_excluir = True
            self.toast("Clique em Confirmar.")
            return

        ok = self.gerenciador.remover_nivel(self.nivel_sel_id)

        self.toast(
            f"Excluído: {self.nivel_sel_id}" if ok else "Falha ao excluir."
        )

        self.confirmar_excluir = False
        self.nivel_sel_id = None

        self.estado = "lista"

        self._rebuild_lista()

    # ==================================================
    # INPUT
    # ==================================================

    def _apagar_1(self):

        if self.campo_ativo == "texto":

            if self.texto:
                self.texto = self.texto[:-1]

        else:

            if self.repeticoes:
                self.repeticoes = self.repeticoes[:-1]

    def _handle_input(self, e):

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_TAB:

                self.campo_ativo = (
                    "repeticoes"
                    if self.campo_ativo == "texto"
                    else "texto"
                )

                return

            if e.key == pygame.K_RETURN:

                self._salvar()
                return

            if e.key == pygame.K_BACKSPACE:

                self._bk_held = True
                agora = pygame.time.get_ticks()

                self._apagar_1()

                self._bk_next_ms = agora + self._bk_first_delay

                return

            if not e.unicode:
                return

            if self.campo_ativo == "texto":

                if len(self.texto) < 220:
                    self.texto += e.unicode

            else:

                if e.unicode.isdigit() and len(self.repeticoes) < 3:
                    self.repeticoes += e.unicode

        elif e.type == pygame.KEYUP:

            if e.key == pygame.K_BACKSPACE:
                self._bk_held = False

    # ==================================================
    # CURSOR
    # ==================================================

    def _tick_cursor(self):

        agora = pygame.time.get_ticks()

        if agora - self._cursor_last > self._cursor_interval:

            self._cursor_on = not self._cursor_on
            self._cursor_last = agora

    def _tick_backspace(self):

        if not self._bk_held:
            return

        agora = pygame.time.get_ticks()

        if agora >= self._bk_next_ms:

            self._apagar_1()
            self._bk_next_ms = agora + self._bk_repeat

    # ==================================================
    # UPDATE
    # ==================================================

    def atualizar(self, eventos):

        if self.estado == "lista":
            self.aplicar_scroll(eventos, len(self.itens_rects))

        if self.estado == "editar":
            self._tick_cursor()
            self._tick_backspace()

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

                        if self.nivel_sel_id:
                            self._abrir_editar(self.nivel_sel_id)
                        else:
                            self.toast("Selecione um nível.")

                        return None

                    if self.botao_excluir.collidepoint(e.pos):
                        self._excluir()
                        return None

                    selecionado = self.detectar_selecao(eventos)

                    if selecionado:

                        self.nivel_sel_id = selecionado
                        self.confirmar_excluir = False

                        return None

                else:

                    if self.campo_texto.collidepoint(e.pos):
                        self.campo_ativo = "texto"
                        return None

                    if self.campo_rep.collidepoint(e.pos):
                        self.campo_ativo = "repeticoes"
                        return None

                    if self.botao_salvar.collidepoint(e.pos):
                        self._salvar()
                        return None

        return None

    # ==================================================
    # DRAW ITEM
    # ==================================================

    def _desenhar_item(self, nid, rect, selecionado, hover):

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

        n = self.gerenciador.obter_nivel_por_id(nid)

        prev = str(n.palavras) if n else ""

        if len(prev) > 46:
            prev = prev[:46] + "..."

        txt = self.fonte_peq.render(
            f"{nid} — {prev}",
            True,
            cor
        )

        self.tela.blit(txt, (rect.x + 12, rect.y + 6))

    # ==================================================
    # DRAW LISTA
    # ==================================================

    def _desenhar_lista(self):

        self.desenhar_cabecalho("Editor — Níveis Avançados")

        self.botao_novo = GameConfig.desenhar_botao(
            self.tela,"Novo",self.fonte_peq,
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

    # ==================================================
    # DRAW EDITAR
    # ==================================================

    def _desenhar_edicao(self):

        self.desenhar_voltar()

        self.botao_salvar = GameConfig.desenhar_botao(
            self.tela,
            "Salvar",
            self.fonte_peq,
            GameConfig.LARGURA-160,
            30,
            130,
            45
        )

        titulo = (
            "Novo Nível Avançado"
            if self.modo_novo
            else f"Editar {self.nivel_sel_id}"
        )

        GameConfig.desenhar_titulo(
            self.tela,
            titulo,
            self.fonte,
            GameConfig.LARGURA
        )

        cor_txt = (
            GameConfig.AMARELO
            if self.campo_ativo == "texto"
            else GameConfig.BRANCO
        )

        cor_rep = (
            GameConfig.AMARELO
            if self.campo_ativo == "repeticoes"
            else GameConfig.BRANCO
        )

        pygame.draw.rect(self.tela,GameConfig.CINZA,self.campo_texto)
        pygame.draw.rect(self.tela,cor_txt,self.campo_texto,2,border_radius=8)

        pygame.draw.rect(self.tela,GameConfig.CINZA,self.campo_rep)
        pygame.draw.rect(self.tela,cor_rep,self.campo_rep,2,border_radius=8)

        texto_render=self.texto
        rep_render=self.repeticoes

        if self._cursor_on:

            if self.campo_ativo=="texto":
                texto_render+="_"
            else:
                rep_render+="_"

        linha1=texto_render[:90]
        linha2=texto_render[90:180]

        img1=self.fonte_peq.render(linha1,True,GameConfig.BRANCO)
        self.tela.blit(img1,(self.campo_texto.x+12,self.campo_texto.y+10))

        if linha2:

            img2=self.fonte_peq.render(linha2,True,GameConfig.BRANCO)
            self.tela.blit(img2,(self.campo_texto.x+12,self.campo_texto.y+40))

        rep_img=self.fonte_peq.render(
            rep_render if rep_render else "_",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(rep_img,rep_img.get_rect(center=self.campo_rep.center))

        dica=self.fonte_peq.render(
            "ENTER = salvar | TAB = alternar | ESC = voltar",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(
            dica,
            dica.get_rect(
                center=(GameConfig.LARGURA//2,GameConfig.ALTURA-60)
            )
        )

        self.desenhar_toast()

    # ==================================================
    # DRAW
    # ==================================================

    def desenhar(self):

        GameConfig.desenhar_fundo(self.tela)

        if self.estado=="lista":
            self._desenhar_lista()
            return

        self._desenhar_edicao()