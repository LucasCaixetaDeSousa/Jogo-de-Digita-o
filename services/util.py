class Util:

    # Valida nome do jogador
    @staticmethod
    def nome_valido(nome):

        nome = nome.strip()

        if not nome:
            return "Digite um nome"

        if len(nome) < 2:
            return "Nome muito curto"

        return None