
import pygame
import string
from abc import ABC, abstractmethod

from constantes import TAMANHO_CELULA, CINZAESCURO, VERDE, PRETO, LARANJA

# importa a classe base abstrata
from elemento_jogo import ElementoJogo


# classe base para navios que herda de ElementoJogo
class BaseNavio(ElementoJogo):
    # classe base para todos os tipos de navios
    def __init__(self, nome: str, tamanho: int, direcao: str = "horizontal"):
        super().__init__()
        self._nome = nome
        self._tamanho = tamanho
        self._direcao = direcao
        self._posicoes: list[tuple[int, int]] = []
        self._partes_atingidas: set[tuple[int, int]] = set()

    def __str__(self):
        status = "Afundado" if self.esta_afundado() else f"{len(self._partes_atingidas)}/{self._tamanho} atingido(s)"
        return f"{self._nome}({self._tamanho}, {self._direcao}) - {status}"

    @property
    def nome(self) -> str: return self._nome
    @property
    def tamanho(self) -> int: return self._tamanho
    @property
    def direcao(self) -> str: return self._direcao

    @direcao.setter
    def direcao(self, nova_direcao: str):
        if nova_direcao in ["horizontal", "vertical"]:
            self._direcao = nova_direcao
        else:
            print(f"AVISO: direção inválida para {self.nome}: {nova_direcao}")

    @property
    def posicoes(self) -> list[tuple[int, int]]: return self._posicoes

    @posicoes.setter
    def posicoes(self, novas_posicoes: list[tuple[int, int]]):
         # Basicamente apenas permite que o tabuleiro defina as posições
         self._posicoes = novas_posicoes

    @property
    def partes_atingidas(self) -> set[tuple[int, int]]: return self._partes_atingidas

    def atingir(self, linha: int, coluna: int) -> bool:
        # registra um acerto em uma posição específica do navio."""
        if (linha, coluna) in self._posicoes:
            self._partes_atingidas.add((linha, coluna))
            # verificar se afundou após o acerto e retornar essa info tbm
            return True
        return False 

    def esta_afundado(self) -> bool:
        # verifica se todas as partes do navio foram atingidas
        # se o navio nao foi posicionado, nao foi afundado
        if not self._posicoes:
             return False
        return len(self._partes_atingidas) == self._tamanho

    # polimorfismo: metodo para desenhar uma parte
    @abstractmethod
    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        # metodo abstrato para desenhar uma célula específica pertencente a este navio
        pass

    def desenhar(self, tela: pygame.Surface, offset_x: int, offset_y: int, mostrar: bool = False, grid_tabuleiro=None):
        # desenha o navio chamando desenhar_parte para cada célula
        # requer o grid do tabuleiro para saber o status das suas células
        if mostrar and self._posicoes and grid_tabuleiro:
            for r, c in self._posicoes:
                if 0 <= r < len(grid_tabuleiro) and 0 <= c < len(grid_tabuleiro[0]):
                    status_celula = grid_tabuleiro[r][c]
                    self.desenhar_parte(tela, offset_x, offset_y, r, c, status_celula)

class Destroyer(BaseNavio):
    def __init__(self, direcao: str = "horizontal"):
        super().__init__("Destroyer", 1, direcao)

    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        x = offset_x + coluna * TAMANHO_CELULA
        y = offset_y + linha * TAMANHO_CELULA
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        cor = CINZAESCURO 

        if self.esta_afundado(): # verifica se o navio afundou por completo
            cor = LARANJA
        elif status_celula == 2: # ve se nao afundou, mas esta PARTE foi atingida
             cor = VERDE

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)

class Lancha(BaseNavio):
    def __init__(self, direcao: str = "horizontal"):
        super().__init__("Lancha", 2, direcao)

    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        x = offset_x + coluna * TAMANHO_CELULA
        y = offset_y + linha * TAMANHO_CELULA
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        cor = CINZAESCURO

        if self.esta_afundado():
             cor = LARANJA
        elif status_celula == 2:
             cor = VERDE

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)

class Submarino(BaseNavio):
    def __init__(self, direcao: str = "horizontal"):
        super().__init__("Submarino", 3, direcao)

    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        x = offset_x + coluna * TAMANHO_CELULA
        y = offset_y + linha * TAMANHO_CELULA
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        cor = CINZAESCURO

        if self.esta_afundado():
             cor = LARANJA
        elif status_celula == 2:
             cor = VERDE

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)

class Cruzador(BaseNavio):
    def __init__(self, direcao: str = "horizontal"):
        super().__init__("Cruzador", 4, direcao)

    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        x = offset_x + coluna * TAMANHO_CELULA
        y = offset_y + linha * TAMANHO_CELULA
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        cor = CINZAESCURO

        if self.esta_afundado():
             cor = LARANJA
        elif status_celula == 2:
             cor = VERDE

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)

class Encouracado(BaseNavio):
    def __init__(self, direcao: str = "horizontal"):
        super().__init__("Encouracado", 5, direcao)

    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        x = offset_x + coluna * TAMANHO_CELULA
        y = offset_y + linha * TAMANHO_CELULA
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        cor = CINZAESCURO

        if self.esta_afundado():
             cor = LARANJA
        elif status_celula == 2:
             cor = VERDE

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)

class PortaAvioes(BaseNavio):
    def __init__(self, direcao: str = "horizontal"):
        super().__init__("Porta-aviões", 6, direcao)

    def desenhar_parte(self, tela: pygame.Surface, offset_x: int, offset_y: int, linha: int, coluna: int, status_celula: int):
        x = offset_x + coluna * TAMANHO_CELULA
        y = offset_y + linha * TAMANHO_CELULA
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        cor = CINZAESCURO

        if self.esta_afundado():
             cor = LARANJA
        elif status_celula == 2:
             cor = VERDE

        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, PRETO, rect, 1)

INFO_NAVIOS = {
    1: {"nome": "Destroyer", "classe": Destroyer},
    2: {"nome": "Lancha", "classe": Lancha},
    3: {"nome": "Submarino", "classe": Submarino},
    4: {"nome": "Cruzador", "classe": Cruzador},
    5: {"nome": "Encouracado", "classe": Encouracado},
    6: {"nome": "Porta-aviões", "classe": PortaAvioes}
}

MAX_NAVIOS_JOGADOR = len(INFO_NAVIOS)