from __future__ import annotations

import os

from services.json_manager import carregar_json, salvar_json

class Ranking:

    # Inicializa sistema de ranking
    def __init__(self, arquivo="data/ranking.json", gerenciador_niveis=None):

        self.nome_arquivo = os.path.basename(arquivo)
        self.gerenciador_niveis = gerenciador_niveis
        self.dados = self._carregar()

    # Carrega dados do ranking
    def _carregar(self):

        try:

            data = carregar_json(self.nome_arquivo)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

        return {}

    # Salva dados do ranking
    def _salvar(self):

        salvar_json(self.nome_arquivo, self.dados)

    # Normaliza formato dos níveis
    def _niveis(self, dados_aluno):

        if not isinstance(dados_aluno, dict):
            return {}

        for k, v in list(dados_aluno.items()):

            if isinstance(v, int):

                dados_aluno[k] = {
                    "pontos": v,
                    "tempo": 9999
                }

            elif isinstance(v, dict):

                dados_aluno[k]["pontos"] = int(v.get("pontos", 0))
                dados_aluno[k]["tempo"] = int(v.get("tempo", 9999))

            else:

                dados_aluno[k] = {
                    "pontos": 0,
                    "tempo": 9999
                }

        return dados_aluno

    # Registra pontuação no ranking
    def adicionar_pontos(self, nome, turma, nivel, pontos, tempo):

        chave = f"{nome}|{turma}"

        if chave not in self.dados or not isinstance(self.dados.get(chave), dict):
            self.dados[chave] = {}

        niveis = self._niveis(self.dados[chave])

        nivel = str(nivel)
        pontos = int(pontos)
        tempo = int(tempo)

        if nivel not in niveis:

            niveis[nivel] = {
                "pontos": pontos,
                "tempo": tempo
            }

        else:

            atual = niveis[nivel]

            pontos_atuais = int(atual.get("pontos", 0))
            tempo_atual = int(atual.get("tempo", 9999))

            if pontos > pontos_atuais:

                niveis[nivel] = {
                    "pontos": pontos,
                    "tempo": tempo
                }

            elif pontos == pontos_atuais and tempo < tempo_atual:

                niveis[nivel]["tempo"] = tempo

        self.dados[chave] = niveis
        self._salvar()

    # Retorna ranking global geral
    def global_geral(self, top=30):

        ranking = []

        for chave, dados_aluno in self.dados.items():

            if "|" not in chave:
                continue

            nome, turma = chave.split("|", 1)

            niveis = self._niveis(dados_aluno)

            total_pontos = 0
            total_tempo = 0

            for v in niveis.values():
                total_pontos += int(v.get("pontos", 0))
                total_tempo += int(v.get("tempo", 9999))

            if total_pontos <= 0:
                continue

            ranking.append((nome, turma, total_tempo, total_pontos))

        ranking.sort(key=lambda x: (-x[3], x[2]))

        return ranking[:top]

    # Retorna ranking global por nível
    def global_nivel(self, nivel, top=30):

        ranking = []
        nivel = str(nivel)

        for chave, dados_aluno in self.dados.items():

            if "|" not in chave:
                continue

            nome, turma = chave.split("|", 1)

            niveis = self._niveis(dados_aluno)

            if nivel in niveis:

                pontos = int(niveis[nivel].get("pontos", 0))
                tempo = int(niveis[nivel].get("tempo", 9999))

                if pontos <= 0:
                    continue

                ranking.append((nome, turma, tempo, pontos))

        ranking.sort(key=lambda x: (-x[3], x[2]))

        return ranking[:top]

    # Retorna ranking geral da turma
    def turma_geral(self, turma):

        turma = str(turma)
        ranking = []

        for chave, dados_aluno in self.dados.items():

            if "|" not in chave:
                continue

            nome, t = chave.split("|", 1)

            if str(t) != turma:
                continue

            niveis = self._niveis(dados_aluno)

            total_pontos = 0
            total_tempo = 0

            for v in niveis.values():
                total_pontos += int(v.get("pontos", 0))
                total_tempo += int(v.get("tempo", 9999))

            if total_pontos <= 0:
                continue

            ranking.append((nome, t, total_tempo, total_pontos))

        ranking.sort(key=lambda x: (-x[3], x[2]))

        return ranking

    # Retorna ranking da turma por nível
    def turma_nivel(self, turma, nivel):

        turma = str(turma)
        nivel = str(nivel)

        ranking = []

        for chave, dados_aluno in self.dados.items():

            if "|" not in chave:
                continue

            nome, t = chave.split("|", 1)

            if str(t) != turma:
                continue

            niveis = self._niveis(dados_aluno)

            if nivel in niveis:

                pontos = int(niveis[nivel].get("pontos", 0))
                tempo = int(niveis[nivel].get("tempo", 9999))

                if pontos <= 0:
                    continue

                ranking.append((nome, t, tempo, pontos))

        ranking.sort(key=lambda x: (-x[3], x[2]))

        return ranking

    # Remove aluno do ranking
    def remover_aluno(self, nome, turma):

        chave = f"{nome}|{turma}"

        if chave in self.dados:

            del self.dados[chave]

            self._salvar()