from __future__ import annotations

import os
import pygame

from game_config import *

from core.scene_manager import SceneManager
from core.game_state import GameState
from core.event_bus import EventBus

from services.resource_cache import ResourceCache
from services.progresso import Progresso
from services.ranking import Ranking
from services.paths import resource_path
from services.sync_service import SyncService

from modules.gerenciador_niveis import GerenciadorNiveis
from modules.gerenciador_turmas import GerenciadorTurmas
from modules.gerenciador_alunos import GerenciadorAlunos

from ui.telas.tela_login import TelaLogin
from ui.telas.tela_niveis import TelaNiveis
from ui.telas.tela_jogo import TelaJogo
from ui.telas.tela_ranking import TelaRanking
from ui.telas.tela_admin import TelaAdmin
from ui.telas.tela_editor_alunos import TelaEditorAlunos
from ui.telas.tela_editor_turmas import TelaEditorTurmas
from ui.telas.tela_editor_niveis import TelaEditorNiveis

class _RankingOnlineFallback:

    def enviar_score(self, nome, turma, nivel, pontos, tempo=9999):
        return None

    def ranking_global(self, top=20):
        return []

    def ranking_global_nivel(self, nivel, top=20):
        return []

    def ranking_turma(self, turma, top=20):
        return []

    def ranking_turma_nivel(self, turma, nivel, top=20):
        return []

    def servidor_online(self):
        return False


class Game:

    # Inicializa todo o sistema do jogo
    def __init__(self):

        pygame.init()

        try:
            pygame.mixer.init()
            self.mixer_disponivel = True
        except Exception:
            self.mixer_disponivel = False

        try:
            icone = pygame.image.load(resource_path("assets/imagens/icone.png"))
            pygame.display.set_icon(icone)
        except Exception:
            pass

        try:
            self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        except Exception:
            pygame.display.init()
            self.tela = pygame.display.set_mode((LARGURA, ALTURA))

        pygame.display.set_caption("Treino de Digitação")

        self.clock = pygame.time.Clock()

        self.fonte = ResourceCache.fonte("consolas", 32)
        self.fonte_peq = ResourceCache.fonte("consolas", 22)

        if self.mixer_disponivel:
            try:
                self.som_acerto = ResourceCache.som("sons/acerto.wav")
            except Exception:
                self.som_acerto = None

            try:
                self.som_erro = ResourceCache.som("sons/erro.wav")
            except Exception:
                self.som_erro = None
        else:
            self.som_acerto = None
            self.som_erro = None

        fontes = (self.fonte, self.fonte_peq)
        sons = (self.som_acerto, self.som_erro)

        self.state = GameState()
        self.events = EventBus()

        self.progresso = Progresso(ARQUIVO_PROGRESSO)

        self.gerenciador_niveis = GerenciadorNiveis(ARQUIVO_NIVEIS)

        self.ranking = Ranking(
            ARQUIVO_RANKING,
            gerenciador_niveis=self.gerenciador_niveis
        )

        self.gerenciador_turmas = GerenciadorTurmas()

        self.gerenciador_alunos = GerenciadorAlunos(
            self.progresso,
            self.ranking,
            self.gerenciador_turmas
        )

        self.ranking_online = self._criar_ranking_online()

        self.sync = SyncService()

        self.events.subscribe("nivel_completo", self._nivel_completo)

        self.scene = SceneManager()

        self.tela_login = TelaLogin(
            self.tela,
            fontes,
            self.gerenciador_turmas,
            self.state
        )

        self.tela_niveis = TelaNiveis(
            self.tela,
            fontes,
            self.gerenciador_niveis,
            self.progresso,
            self.state
        )

        self.tela_jogo = TelaJogo(
            self.tela,
            fontes,
            sons,
            self.gerenciador_niveis,
            self.state,
            self.events
        )

        self.tela_ranking = TelaRanking(
            self.tela,
            fontes,
            self.ranking,
            self.state,
            self.gerenciador_niveis
        )

        self.tela_admin = TelaAdmin(
            self.tela,
            fontes,
            self.state
        )

        self.tela_editor_alunos = TelaEditorAlunos(
            self.tela,
            fontes,
            self.gerenciador_alunos,
            self.gerenciador_turmas,
            self.state
        )

        self.tela_editor_turmas = TelaEditorTurmas(
            self.tela,
            fontes,
            self.gerenciador_turmas,
            self.gerenciador_alunos,
            self.state
        )

        self.tela_editor_niveis = TelaEditorNiveis(
            self.tela,
            fontes,
            self.gerenciador_niveis,
            self.state
        )

        self.scene.registrar("login", self.tela_login)
        self.scene.registrar("niveis", self.tela_niveis)
        self.scene.registrar("jogo", self.tela_jogo)
        self.scene.registrar("ranking", self.tela_ranking)
        self.scene.registrar("admin", self.tela_admin)
        self.scene.registrar("editor_alunos", self.tela_editor_alunos)
        self.scene.registrar("editor_turmas", self.tela_editor_turmas)
        self.scene.registrar("editor_niveis", self.tela_editor_niveis)

        self.scene.mudar("login")

    # Cria instância do ranking online
    def _criar_ranking_online(self):

        try:
            from services.ranking_online import RankingOnline

            url_base = os.getenv("RANKING_URL", "").strip()

            if url_base:
                return RankingOnline(url_base)

            return RankingOnline()

        except Exception:
            return _RankingOnlineFallback()

    # Processa evento de nível completo
    def _nivel_completo(self, data):

        if not data:
            return

        nome = data.get("nome")
        turma = data.get("turma")
        nivel = data.get("nivel")
        pontos = int(data.get("pontos", 0))
        tempo = int(data.get("tempo", 9999))

        if not nome or not turma or nivel is None:
            return

        self.ranking.adicionar_pontos(
            nome,
            turma,
            nivel,
            pontos,
            tempo
        )

        idx = self.gerenciador_niveis.indice_global(nivel)

        if idx is not None:
            self.progresso.registrar(nome, turma, idx + 1)

        self.sync.adicionar(
            nome,
            turma,
            nivel,
            pontos,
            tempo
        )

    # Inicia telas quando necessário
    def _iniciar_tela_se_necessario(self, nome_tela):

        if nome_tela == "niveis":
            self.tela_niveis.iniciar()

        elif nome_tela == "jogo":
            self.tela_jogo.iniciar()

        elif nome_tela == "ranking":
            self.tela_ranking.iniciar()

        elif nome_tela == "admin":
            self.tela_admin.iniciar()

        elif nome_tela == "editor_alunos":
            self.tela_editor_alunos.iniciar()

        elif nome_tela == "editor_turmas":
            self.tela_editor_turmas.iniciar()

        elif nome_tela == "editor_niveis":
            self.tela_editor_niveis.iniciar()

    # Encerra pygame com segurança
    def _encerrar(self):

        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception:
            pass

        try:
            pygame.quit()
        except Exception:
            pass

    # Loop principal do jogo
    def executar(self):

        rodando = True

        try:
            while rodando:

                self.clock.tick(60)

                eventos = pygame.event.get()

                for e in eventos:
                    if e.type == pygame.QUIT:
                        rodando = False

                retorno = self.scene.atualizar(eventos)

                if retorno == "sair":
                    rodando = False

                elif isinstance(retorno, str) and retorno:
                    self._iniciar_tela_se_necessario(retorno)
                    self.scene.mudar(retorno)

                self.scene.desenhar()
                pygame.display.update()

        finally:
            self._encerrar()