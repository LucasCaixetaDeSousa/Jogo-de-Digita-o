from __future__ import annotations

import json
import os
from typing import Dict, Any

from services.paths import resource_path, writable_path

CONFIG_PADRAO = {
    "codigo_admin": "102030"
}

class ConfigSistema:

    # Inicializa configuração do sistema
    def __init__(self, arquivo: str = "config.json"):

        self.arquivo = writable_path("data/config.json")
        self.arquivo_padrao = resource_path("data/config.json")

        self.dados: Dict[str, Any] = {}

        self._garantir_arquivo()
        self._carregar()

    # Garante existência do arquivo de configuração
    def _garantir_arquivo(self):

        if os.path.exists(self.arquivo):
            return

        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)

        if os.path.exists(self.arquivo_padrao):

            with open(self.arquivo_padrao, "r", encoding="utf-8") as f:
                dados = json.load(f)

        else:
            dados = CONFIG_PADRAO.copy()

        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # Carrega configuração do sistema
    def _carregar(self):

        try:

            with open(self.arquivo, "r", encoding="utf-8") as f:
                self.dados = json.load(f)

        except Exception:

            self.dados = CONFIG_PADRAO.copy()
            self._salvar()

    # Salva configuração no arquivo
    def _salvar(self):

        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)

    # Retorna código admin
    def codigo_admin(self) -> str:

        return str(
            self.dados.get(
                "codigo_admin",
                CONFIG_PADRAO["codigo_admin"]
            )
        )

    # Altera código admin
    def alterar_codigo_admin(self, novo_codigo: str):

        self.dados["codigo_admin"] = str(novo_codigo)

        self._salvar()