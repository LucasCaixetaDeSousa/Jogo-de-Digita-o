from __future__ import annotations
from typing import Dict, List, Any

from services.progresso import Progresso
from services.ranking import Ranking
from modules.gerenciador_turmas import GerenciadorTurmas

class GerenciadorAlunos:

    # Inicializa gerenciador de alunos
    def __init__(
        self,
        progresso: Progresso,
        ranking: Ranking,
        gerenciador_turmas: GerenciadorTurmas,
    ) -> None:
        self.progresso = progresso
        self.ranking = ranking
        self.gerenciador_turmas = gerenciador_turmas

    # Lista todos os alunos
    def listar_alunos(self) -> List[Dict[str, Any]]:
        alunos: List[Dict[str, Any]] = []

        for chave, dados in self.progresso.dados.items():

            if "|" not in chave:
                continue

            nome, turma = chave.split("|", 1)

            if isinstance(dados, dict):
                nivel = int(dados.get("nivel", 0))
            else:
                nivel = int(dados) if str(dados).isdigit() else 0

            alunos.append(
                {
                    "nome": nome,
                    "turma": turma,
                    "nivel": nivel,
                }
            )

        alunos.sort(key=lambda x: (x["turma"], x["nome"]))
        return alunos

    # Cria novo aluno
    def criar(self, nome: str, turma: str) -> bool:

        chave = f"{nome}|{turma}"

        if chave in self.progresso.dados:
            return False

        self.progresso.set_nivel(nome, turma, 0)
        return True

    # Edita nível do aluno
    def editar_nivel(self, nome: str, turma: str, novo_nivel: int) -> None:
        self.progresso.set_nivel(nome, turma, int(novo_nivel))

    # Remove aluno
    def remover(self, nome: str, turma: str) -> None:
        self.progresso.remover(nome, turma)
        self.ranking.remover_aluno(nome, turma)

    # Remove todos os alunos de uma turma
    def remover_por_turma(self, turma: str) -> int:

        turma = str(turma)

        removiveis: List[tuple[str, str]] = []

        for chave in list(self.progresso.dados.keys()):

            if "|" not in chave:
                continue

            nome, t = chave.split("|", 1)

            if str(t) == turma:
                removiveis.append((nome, t))

        for nome, t in removiveis:
            self.remover(nome, t)

        return len(removiveis)