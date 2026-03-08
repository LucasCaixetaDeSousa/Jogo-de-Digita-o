from __future__ import annotations

import os
from typing import Dict, List, Optional

from modules.turma import Turma
from services.json_manager import carregar_json, salvar_json


class GerenciadorTurmas:

    TURMA_ADMIN_ID = "0"

    # Inicializa gerenciador de turmas
    def __init__(self, arquivo: str = "data/turmas.json") -> None:

        self.arquivo: str = arquivo
        self.nome_arquivo: str = os.path.basename(arquivo)

        self.turmas: Dict[str, Turma] = {}

        self._carregar()
        self._garantir_turma_admin()

    # Carrega turmas do arquivo
    def _carregar(self) -> None:

        try:
            data = carregar_json(self.nome_arquivo)
        except Exception:
            data = []

        if not isinstance(data, list):
            data = []

        self.turmas.clear()

        for item in data:

            try:
                turma = Turma.from_dict(item)
                self.turmas[str(turma.id)] = turma
            except Exception:
                continue

    # Salva turmas no arquivo
    def _salvar(self) -> None:

        salvar_json(
            self.nome_arquivo,
            [t.to_dict() for t in self.turmas.values()]
        )

    # Garante existência da turma ADMIN
    def _garantir_turma_admin(self) -> None:

        if self.TURMA_ADMIN_ID not in self.turmas:

            self.turmas[self.TURMA_ADMIN_ID] = Turma(
                self.TURMA_ADMIN_ID,
                "ADMIN"
            )

            self._salvar()

    # Lista turmas disponíveis
    def listar(self) -> List[Turma]:

        return [
            turma
            for turma in self.turmas.values()
            if str(turma.id) != self.TURMA_ADMIN_ID
        ]

    # Obtém turma pelo id
    def obter(self, id: str) -> Optional[Turma]:

        return self.turmas.get(str(id))

    # Retorna próximo id disponível
    def proximo_id(self) -> str:

        ids = [
            int(t.id)
            for t in self.turmas.values()
            if str(t.id).isdigit() and str(t.id) != self.TURMA_ADMIN_ID
        ]

        if not ids:
            return "1"

        return str(max(ids) + 1)

    # Renumera ids das turmas
    def _renumerar_turmas(self) -> None:

        turmas = [
            t for t in self.turmas.values()
            if str(t.id) != self.TURMA_ADMIN_ID
        ]

        turmas.sort(
            key=lambda t: int(t.id) if str(t.id).isdigit() else 9999
        )

        admin = self.turmas.get(self.TURMA_ADMIN_ID)

        novo_dict: Dict[str, Turma] = {}

        contador = 1

        for turma in turmas:

            novo_id = str(contador)

            turma.id = novo_id
            novo_dict[novo_id] = turma

            contador += 1

        if admin is not None:

            admin.id = self.TURMA_ADMIN_ID
            novo_dict[self.TURMA_ADMIN_ID] = admin

        self.turmas = novo_dict

    # Cria nova turma
    def criar(self, id: str, nome: str) -> bool:

        id = str(id)

        if id == self.TURMA_ADMIN_ID:
            return False

        if id in self.turmas:
            return False

        self.turmas[id] = Turma(id, nome)

        self._salvar()

        return True

    # Alias para criar turma
    def adicionar(self, id: str, nome: str) -> bool:
        return self.criar(id, nome)

    # Edita nome da turma
    def editar(self, id: str, novo_nome: str) -> bool:

        id = str(id)

        if id == self.TURMA_ADMIN_ID:
            return False

        turma = self.obter(id)

        if not turma:
            return False

        turma.nome = novo_nome

        self._salvar()

        return True

    # Remove turma
    def remover(self, id: str, gerenciador_alunos=None) -> bool:

        id = str(id)

        if id == self.TURMA_ADMIN_ID:
            return False

        if id not in self.turmas:
            return False

        if gerenciador_alunos:

            try:
                gerenciador_alunos.remover_por_turma(id)
            except Exception:
                pass

        del self.turmas[id]

        self._renumerar_turmas()
        self._salvar()

        return True