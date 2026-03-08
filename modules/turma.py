from __future__ import annotations
from typing import Dict, Any

class Turma:

    # Inicializa turma
    def __init__(
        self,
        id: str,
        nome: str,
        ano_letivo: str = "",
        ativa: bool = True,
    ) -> None:

        self.id: str = str(id)
        self.nome: str = nome
        self.ano_letivo: str = ano_letivo
        self.ativa: bool = bool(ativa)

    # Converte turma para dict
    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "nome": self.nome,
            "ano_letivo": self.ano_letivo,
            "ativa": self.ativa,
        }

    # Cria turma a partir de dict
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Turma":

        return Turma(
            id=str(data.get("id", "")),
            nome=str(data.get("nome", "")),
            ano_letivo=str(data.get("ano_letivo", "")),
            ativa=bool(data.get("ativa", True)),
        )