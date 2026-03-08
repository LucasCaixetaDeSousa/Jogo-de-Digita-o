from __future__ import annotations
from typing import Dict

class Aluno:

    # Inicializa aluno
    def __init__(self, nome: str, turma: str) -> None:
        self.nome: str = nome
        self.turma: str = turma
        self.pontos_por_nivel: Dict[str, int] = {}

    # Retorna chave única do aluno
    def chave(self) -> str:
        return f"{self.nome}|{self.turma}"

    # Registra pontuação em um nível
    def registrar_pontuacao(self, nivel_id: str, pontos: int) -> None:
        self.pontos_por_nivel[nivel_id] = max(int(pontos), 0)

    # Retorna pontuação de um nível
    def pontuacao_nivel(self, nivel_id: str) -> int:
        return self.pontos_por_nivel.get(nivel_id, 0)

    # Retorna pontuação total
    def pontuacao_total(self) -> int:
        return sum(self.pontos_por_nivel.values())