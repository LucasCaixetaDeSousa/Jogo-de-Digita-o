import threading
import time

class RankingSync:

    # Inicializa sincronização do ranking
    def __init__(self, ranking_local, ranking_online, intervalo=5):

        self.ranking_local = ranking_local
        self.ranking_online = ranking_online
        self.intervalo = intervalo

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

    # Loop de sincronização com servidor
    def _loop(self):

        while True:

            time.sleep(self.intervalo)

            try:

                if not self.ranking_online.servidor_online():
                    continue

                ranking = self.ranking_online.ranking_global()

                if not ranking:
                    continue

                self.ranking_local.substituir_global(ranking)

            except Exception:
                pass