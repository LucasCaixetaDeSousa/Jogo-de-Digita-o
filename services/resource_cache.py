import pygame
import os

class ResourceCache:

    _fontes = {}
    _sons = {}

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")

    # Retorna fonte em cache
    @staticmethod
    def fonte(nome: str, tamanho: int):

        key = (nome, tamanho)

        if key not in ResourceCache._fontes:
            ResourceCache._fontes[key] = pygame.font.SysFont(nome, tamanho)

        return ResourceCache._fontes[key]

    # Retorna som em cache
    @staticmethod
    def som(path: str):

        caminho = os.path.join(ResourceCache.ASSETS_DIR, path)

        if caminho not in ResourceCache._sons:

            ResourceCache._sons[caminho] = pygame.mixer.Sound(caminho)

        return ResourceCache._sons[caminho]