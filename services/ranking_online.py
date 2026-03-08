from __future__ import annotations

import json
import urllib.request
import urllib.parse
import threading

class RankingOnline:

    # Inicializa cliente do ranking online
    def __init__(self, url_base: str = "https://digitacao-ranking.onrender.com"):

        self.url = url_base.rstrip("/")

    # Envia requisição POST
    def _post(self, url, data):

        try:

            data_bytes = json.dumps(data).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=5) as resp:

                texto = resp.read().decode("utf-8")

                if not texto:
                    return None

                return json.loads(texto)

        except Exception as e:

            print("RankingOnline POST erro:", e)
            return None

    # Envia requisição GET
    def _get(self, url):

        try:

            with urllib.request.urlopen(url, timeout=5) as resp:

                texto = resp.read().decode("utf-8")

                if not texto:
                    return None

                return json.loads(texto)

        except Exception as e:

            print("RankingOnline GET erro:", e)
            return None

    # Envia score para servidor
    def enviar_score(self, nome, turma, nivel, pontos, tempo=9999):

        def _thread():

            url = f"{self.url}/score"

            data = {
                "nome": nome,
                "turma": turma,
                "nivel": str(nivel),
                "pontos": int(pontos),
                "tempo": int(tempo)
            }

            self._post(url, data)

        threading.Thread(target=_thread, daemon=True).start()

    # Retorna ranking global
    def ranking_global(self, top=20):

        url = f"{self.url}/ranking?top={top}"

        data = self._get(url)

        return data or []

    # Retorna ranking global por nível
    def ranking_global_nivel(self, nivel, top=20):

        params = urllib.parse.urlencode({
            "nivel": str(nivel),
            "top": top
        })

        url = f"{self.url}/ranking?{params}"

        data = self._get(url)

        return data or []

    # Retorna ranking por turma
    def ranking_turma(self, turma, top=20):

        params = urllib.parse.urlencode({
            "turma": turma,
            "top": top
        })

        url = f"{self.url}/ranking?{params}"

        data = self._get(url)

        return data or []

    # Retorna ranking por turma e nível
    def ranking_turma_nivel(self, turma, nivel, top=20):

        params = urllib.parse.urlencode({
            "turma": turma,
            "nivel": str(nivel),
            "top": top
        })

        url = f"{self.url}/ranking?{params}"

        data = self._get(url)

        return data or []

    # Testa conexão com servidor
    def servidor_online(self):

        try:

            url = f"{self.url}/ranking?nivel=1"

            with urllib.request.urlopen(url, timeout=3):

                return True

        except Exception:

            return False