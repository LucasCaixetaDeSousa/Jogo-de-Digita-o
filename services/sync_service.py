from __future__ import annotations

import json
import os
import threading
import time

from services.paths import writable_path
from services.ranking_online import RankingOnline

class SyncService:

    # Inicializa serviço de sincronização
    def __init__(self, arquivo="data/sync_queue.json", intervalo=10):

        self.arquivo = writable_path(arquivo)
        self.intervalo = intervalo
        self.queue = self._carregar()

        try:
            self.ranking_online = RankingOnline()
        except Exception:
            self.ranking_online = None

        self.lock = threading.Lock()

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

    # Carrega fila de sincronização
    def _carregar(self):

        if not os.path.exists(self.arquivo):
            return []

        try:

            with open(self.arquivo, "r", encoding="utf8") as f:
                return json.load(f)

        except Exception:
            return []

    # Salva fila de sincronização
    def _salvar(self):

        try:

            with open(self.arquivo, "w", encoding="utf8") as f:
                json.dump(self.queue, f, indent=2)

        except Exception:
            pass

    # Adiciona item na fila de sincronização
    def adicionar(self, nome, turma, nivel, pontos, tempo):

        item = {
            "nome": nome,
            "turma": turma,
            "nivel": nivel,
            "pontos": pontos,
            "tempo": tempo
        }

        with self.lock:

            self.queue.append(item)

            self._salvar()

    # Executa loop de sincronização
    def _loop(self):

        while True:

            time.sleep(self.intervalo)

            if not self.queue:
                continue

            if not self.ranking_online:
                continue

            try:

                if not self.ranking_online.servidor_online():
                    continue

            except Exception:
                continue

            with self.lock:

                nova = []

                for item in self.queue:

                    try:

                        resp = self.ranking_online.enviar_score(
                            item["nome"],
                            item["turma"],
                            item["nivel"],
                            item["pontos"],
                            item["tempo"]
                        )

                        if resp is None:
                            nova.append(item)

                    except Exception:
                        nova.append(item)

                self.queue = nova

                self._salvar()