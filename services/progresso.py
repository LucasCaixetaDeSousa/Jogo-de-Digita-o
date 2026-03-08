from __future__ import annotations

import json
import os

from services.paths import resource_path, writable_path

class Progresso:

    # Inicializa sistema de progresso
    def __init__(self, arquivo="data/progresso.json"):

        nome_arquivo = os.path.basename(arquivo)

        self.arquivo = writable_path(f"data/{nome_arquivo}")
        self.arquivo_padrao = resource_path(f"data/{nome_arquivo}")

        self._garantir_arquivo()
        self.dados = self._carregar()

    # Garante existência do arquivo de progresso
    def _garantir_arquivo(self):

        if os.path.exists(self.arquivo):
            return

        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)

        if os.path.exists(self.arquivo_padrao):

            try:
                with open(self.arquivo_padrao, "r", encoding="utf8") as f:
                    dados = json.load(f)
            except Exception:
                dados = {}

        else:
            dados = {}

        if not isinstance(dados, dict):
            dados = {}

        with open(self.arquivo, "w", encoding="utf8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # Carrega dados de progresso
    def _carregar(self):

        try:

            with open(self.arquivo, "r", encoding="utf8") as f:
                data = json.load(f)

            return data if isinstance(data, dict) else {}

        except Exception:
            return {}

    # Salva dados de progresso
    def _salvar(self):

        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)

        with open(self.arquivo, "w", encoding="utf8") as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)

    # Retorna nível atual do aluno
    def obter_nivel(self, nome, turma):

        chave = f"{nome}|{turma}"

        valor = self.dados.get(chave, 0)

        if isinstance(valor, dict):

            try:
                return int(valor.get("nivel", 0))
            except Exception:
                return 0

        try:
            return int(valor)
        except Exception:
            return 0

    # Define nível do aluno
    def set_nivel(self, nome, turma, nivel):

        chave = f"{nome}|{turma}"

        self.dados[chave] = int(nivel)

        self._salvar()

    # Remove progresso do aluno
    def remover(self, nome, turma):

        chave = f"{nome}|{turma}"

        if chave in self.dados:

            del self.dados[chave]

            self._salvar()

    # Registra avanço de nível
    def registrar(self, nome, turma, nivel):

        chave = f"{nome}|{turma}"

        atual = self.obter_nivel(nome, turma)

        if int(nivel) > atual:

            self.dados[chave] = int(nivel)

            self._salvar()