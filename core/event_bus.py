from __future__ import annotations

from collections.abc import Callable
from typing import Any

class EventBus:

    # Inicializa sistema de eventos
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[[Any], None]]] = {}

    # Registra ouvinte de evento
    def subscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        self._listeners.setdefault(event_name, []).append(callback)

    # Dispara evento para ouvintes
    def emit(self, event_name: str, data: Any = None) -> None:
        for cb in self._listeners.get(event_name, []):
            cb(data)