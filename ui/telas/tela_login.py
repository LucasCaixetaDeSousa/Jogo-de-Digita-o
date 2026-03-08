from __future__ import annotations
import pygame

from ui.base_scene import BaseScene
from services.util import Util
from game_config import GameConfig

# Obtém código admin
def _obter_codigo_admin() -> str:

    try:
        from services.config_sistema import ConfigSistema
        return str(ConfigSistema().codigo_admin())

    except Exception:

        if hasattr(GameConfig, "CODIGO_ADMIN"):
            return str(getattr(GameConfig, "CODIGO_ADMIN"))

        return "admin"

class TelaLogin(BaseScene):

    # Inicializa tela de login
    def __init__(self, tela, fontes, gerenciador_turmas, state):

        super().__init__(tela, fontes)

        self.gerenciador_turmas = gerenciador_turmas
        self.state = state

        self.estado: str = "nome"

        self.nome: str = ""
        self.codigo_admin: str = ""

        self.botoes_turmas: list[tuple[str, pygame.Rect]] = []
        self.botao_voltar: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self._codigo_admin_correto: str = _obter_codigo_admin()

    # Carrega turmas disponíveis
    def _carregar_turmas(self) -> None:

        self.botoes_turmas.clear()

        try:
            turmas = self.gerenciador_turmas.listar()

        except Exception:
            turmas = []

        if not turmas:
            self.toast("Nenhuma turma cadastrada.")
            return

        largura = 220
        altura = 48
        esp_x = 40
        esp_y = 18

        total = len(turmas)
        linhas = (total + 1) // 2

        inicio_y = GameConfig.ALTURA // 2 - (linhas * (altura + esp_y)) // 2 + 10

        i = 0

        for linha in range(linhas):

            y = inicio_y + linha * (altura + esp_y)

            for col in range(2):

                if i >= total:
                    break

                turma = turmas[i]
                turma_nome = str(getattr(turma, "nome", turma))

                if col == 0:
                    x = GameConfig.LARGURA // 2 - largura - esp_x // 2
                else:
                    x = GameConfig.LARGURA // 2 + esp_x // 2

                rect = pygame.Rect(x, y, largura, altura)

                self.botoes_turmas.append((turma_nome, rect))

                i += 1

    # Controla ação de voltar
    def _voltar(self):

        if self.estado in ("turma", "admin_codigo"):

            self.estado = "nome"
            self.codigo_admin = ""
            self.toast("")

            return None

        return "sair"

    # Atualiza lógica da tela
    def atualizar(self, eventos):

        mouse = pygame.mouse.get_pos()

        for e in eventos:

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_F1:

                    self.estado = "admin_codigo"
                    self.codigo_admin = ""
                    self.toast("")

                    continue

                if e.key == pygame.K_ESCAPE:

                    r = self._voltar()

                    if r:
                        return r

                    continue

                if self.estado == "nome":

                    if e.key == pygame.K_RETURN:

                        erro = Util.nome_valido(self.nome)

                        if erro:
                            self.toast(erro)

                        else:

                            self.estado = "turma"
                            self.toast("")
                            self._carregar_turmas()

                        continue

                    if e.key == pygame.K_BACKSPACE:

                        self.nome = self.nome[:-1]

                        continue

                    if e.unicode and len(self.nome) < 30:

                        self.nome += e.unicode
                        self.toast("")

                elif self.estado == "admin_codigo":

                    if e.key == pygame.K_RETURN:

                        if self.codigo_admin == self._codigo_admin_correto:

                            self.state.login("ADMIN", "0", True)

                            return "niveis"

                        self.codigo_admin = ""
                        self.toast("Código incorreto.")

                        continue

                    if e.key == pygame.K_BACKSPACE:

                        self.codigo_admin = self.codigo_admin[:-1]

                        continue

                    if e.unicode and len(self.codigo_admin) < 12:

                        self.codigo_admin += e.unicode

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                if self.botao_voltar.collidepoint(mouse):

                    r = self._voltar()

                    if r:
                        return r

                    continue

                if self.estado == "turma":

                    for turma_nome, rect in self.botoes_turmas:

                        if rect.collidepoint(mouse):

                            self.state.login(self.nome, turma_nome, False)

                            return "niveis"

        return None

    # Desenha entrada de nome
    def _desenhar_nome(self):

        instrucao = self.fonte_peq.render(
            "Digite seu nome:",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(
            instrucao,
            instrucao.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2 - 90))
        )

        texto = self.nome + ("_" if self.cursor() else "")

        img = self.fonte.render(texto if texto else "_", True, GameConfig.VERDE)

        self.tela.blit(
            img,
            img.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2))
        )

    # Desenha seleção de turmas
    def _desenhar_turmas(self):

        self.botao_voltar = self.desenhar_voltar()

        instrucao = self.fonte_peq.render(
            "Escolha sua turma:",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(
            instrucao,
            instrucao.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2 - 100))
        )

        for turma_nome, rect in self.botoes_turmas:

            GameConfig.desenhar_botao(
                self.tela,
                f"Turma {turma_nome}",
                self.fonte_peq,
                rect.x,
                rect.y,
                largura=rect.width,
                altura=rect.height
            )

    # Desenha login admin
    def _desenhar_admin(self):

        self.botao_voltar = self.desenhar_voltar()

        instrucao = self.fonte_peq.render(
            "Bem Vindo Professor(a)! Digite a senha:",
            True,
            GameConfig.BRANCO
        )

        self.tela.blit(
            instrucao,
            instrucao.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2 - 70))
        )

        texto = "*" * len(self.codigo_admin) + ("_" if self.cursor() else "")

        img = self.fonte.render(texto if texto else "_", True, GameConfig.VERDE)

        self.tela.blit(
            img,
            img.get_rect(center=(GameConfig.LARGURA // 2, GameConfig.ALTURA // 2))
        )

    # Desenha tela de login
    def desenhar(self):

        self.desenhar_base("TREINO DE DIGITAÇÃO")

        if self.estado == "nome":
            self._desenhar_nome()

        elif self.estado == "turma":
            self._desenhar_turmas()

        elif self.estado == "admin_codigo":
            self._desenhar_admin()

        self.desenhar_toast()