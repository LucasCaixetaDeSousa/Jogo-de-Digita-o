from __future__ import annotations

class SceneManager:

    # Inicializa gerenciador de cenas
    def __init__(self) -> None:
        self._cenas: dict[str, object] = {}
        self._atual: object | None = None
        self._nome_atual: str | None = None

    # Registra nova cena
    def registrar(self, nome: str, cena: object) -> None:
        self._cenas[nome] = cena

    # Muda cena ativa
    def mudar(self, nome: str) -> None:

        if nome not in self._cenas:
            raise KeyError(f"Cena não registrada: {nome}")

        self._atual = self._cenas[nome]
        self._nome_atual = nome

        if hasattr(self._atual, "on_enter"):
            self._atual.on_enter()

    # Atualiza cena atual
    def atualizar(self, eventos):

        if not self._atual:
            return

        if hasattr(self._atual, "atualizar"):

            retorno = self._atual.atualizar(eventos)

            if isinstance(retorno, str):
                if retorno in self._cenas:
                    self.mudar(retorno)

            return retorno

    # Desenha cena atual
    def desenhar(self):

        if self._atual and hasattr(self._atual, "desenhar"):
            self._atual.desenhar()

    # Retorna nome da cena atual
    def nome_atual(self) -> str | None:
        return self._nome_atual