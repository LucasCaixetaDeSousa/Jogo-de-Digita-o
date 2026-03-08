from __future__ import annotations
import os
from typing import Dict, List

from modules.nivel import Nivel
from services.json_manager import carregar_json, salvar_json

DIFICULDADES_PADRAO = ("basico", "intermediario", "avancado")

class GerenciadorNiveis:

    # Inicializa gerenciador de níveis
    def __init__(self, arquivo_json: str = "data/niveis.json") -> None:

        self.arquivo: str = arquivo_json
        self.nome_arquivo: str = os.path.basename(arquivo_json)

        self.niveis: Dict[str, List[Nivel]] = {d: [] for d in DIFICULDADES_PADRAO}
        self._index_map: Dict[str, int] = {}

        self._carregar()
        self._rebuild_index()

    # Carrega níveis do arquivo
    def _carregar(self) -> None:

        try:
            data = carregar_json(self.nome_arquivo)
        except Exception:
            data = {}

        if not isinstance(data, dict):
            data = {}

        for dificuldade in DIFICULDADES_PADRAO:

            lista = data.get(dificuldade, [])

            if not isinstance(lista, list):
                lista = []

            niveis_convertidos = []

            for item in lista:

                try:
                    niveis_convertidos.append(
                        Nivel.from_dict(item, dificuldade=dificuldade)
                    )
                except Exception:
                    continue

            self.niveis[dificuldade] = niveis_convertidos

    # Salva níveis no arquivo
    def _salvar(self) -> None:

        data = {
            dificuldade: [n.to_dict() for n in lista]
            for dificuldade, lista in self.niveis.items()
        }

        salvar_json(self.nome_arquivo, data)

    # Reconstrói índice global de níveis
    def _rebuild_index(self) -> None:

        self._index_map.clear()

        for i, nivel in enumerate(self.todos_niveis()):
            self._index_map[str(nivel.id)] = i

    # Retorna índice global de um nível
    def indice_global(self, nivel_id):
        return self._index_map.get(str(nivel_id))

    # Retorna nível por índice
    def obter_nivel_por_indice(self, indice):

        lista = self.todos_niveis()

        if 0 <= indice < len(lista):
            return lista[indice]

        return None

    # Retorna nível por id
    def obter_nivel_por_id(self, nivel_id):

        nivel_id_str = str(nivel_id)

        for nivel in self.todos_niveis():

            if str(nivel.id) == nivel_id_str:
                return nivel

        return None

    # Retorna lista completa de níveis
    def todos_niveis(self):

        return (
            self.niveis["basico"]
            + self.niveis["intermediario"]
            + self.niveis["avancado"]
        )

    # Adiciona novo nível
    def adicionar_nivel(self, dificuldade, id, nome, palavras, repeticoes):

        if dificuldade not in self.niveis:
            return False

        nivel = Nivel(
            id=str(id),
            nome=str(nome),
            palavras=str(palavras),
            repeticoes=int(repeticoes),
            dificuldade=dificuldade,
        )

        self.niveis[dificuldade].append(nivel)

        self._salvar()
        self._rebuild_index()

        return True

    # Edita nível existente
    def editar_nivel(self, nivel_id, *, palavras=None, repeticoes=None):

        n = self.obter_nivel_por_id(nivel_id)

        if not n:
            return False

        if palavras is not None:
            n.palavras = str(palavras)

        if repeticoes is not None:
            n.repeticoes = int(repeticoes)

        self._salvar()
        self._rebuild_index()

        return True

    # Reorganiza ids de níveis avançados
    def _reorganizar_avancados(self):

        lista = self.niveis["avancado"]

        for i, n in enumerate(lista):

            novo = f"3-{i+1}"

            n.id = novo
            n.nome = novo

    # Remove nível avançado
    def remover_nivel(self, nivel_id):

        lista = self.niveis["avancado"]

        for i, n in enumerate(lista):

            if str(n.id) == str(nivel_id):

                del lista[i]

                self._reorganizar_avancados()

                self._salvar()
                self._rebuild_index()

                return True

        return False

    # Retorna próximo id avançado
    def proximo_id_avancado(self):

        lista = self.niveis["avancado"]

        return f"3-{len(lista)+1}"