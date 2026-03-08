from __future__ import annotations

import os
import sys

# Retorna caminho de recurso do executável
def resource_path(rel_path: str) -> str:

    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(".")

    return os.path.join(base_dir, rel_path)

# Retorna caminho gravável do usuário
def writable_path(rel_path: str) -> str:

    base_dir = os.path.join(os.path.expanduser("~"), "TreinoDigitacao")

    caminho = os.path.join(base_dir, rel_path)

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    return caminho