from services.paths import resource_path, writable_path
import json
import os

# Carrega arquivo json
def carregar_json(nome_arquivo):

    caminho_usuario = writable_path(f"data/{nome_arquivo}")
    caminho_padrao = resource_path(f"data/{nome_arquivo}")

    if not os.path.exists(caminho_usuario):

        os.makedirs(os.path.dirname(caminho_usuario), exist_ok=True)

        with open(caminho_padrao, "r", encoding="utf-8") as f:
            dados = json.load(f)

        with open(caminho_usuario, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    with open(caminho_usuario, "r", encoding="utf-8") as f:
        return json.load(f)

# Salva arquivo json
def salvar_json(nome_arquivo, dados):

    caminho_usuario = writable_path(f"data/{nome_arquivo}")

    os.makedirs(os.path.dirname(caminho_usuario), exist_ok=True)

    with open(caminho_usuario, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)