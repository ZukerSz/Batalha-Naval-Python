
import pygame
import random

from constantes import (LINHAS_TABULEIRO, COLUNAS_TABULEIRO, TAMANHO_CELULA,
                        AZULCLARO, VERMELHO, VERDE, PRETO, CINZAESCURO)

from tipos_de_navio import BaseNavio, ElementoJogo # importa classes de navio e a base abstrata

class Tabuleiro(ElementoJogo): # herda de ElementoJogo
    # representa o tabuleiro de jogo
    def __init__(self, linhas: int = LINHAS_TABULEIRO, colunas: int = COLUNAS_TABULEIRO):
        super().__init__() # chama o construtor da classe base
        self._linhas = linhas
        self._colunas = colunas
        self._grid = [[0 for _ in range(self._colunas)] for _ in range(self._linhas)] # grid armazena: (0: água \1: parte de navio nao atingido, \2: acerto, \3: água com tiro)
        self._navios: list[BaseNavio] = [] # Lista de instâncias de navio no tabuleiro

    # getters
    @property
    def linhas(self) -> int: return self._linhas
    @property
    def colunas(self) -> int: return self._colunas
    @property
    def grid(self) -> list[list[int]]: return self._grid
    @property
    def navios(self) -> list[BaseNavio]: return self._navios

    def pode_colocar_navio(self, linha_inicio: int, coluna_inicio: int, navio: BaseNavio) -> bool:
        # verifica se um navio pode ser colocado na posicao e direção especificadas
        for i in range(navio.tamanho): # executa pelas células que o navio ocuparia
            r = linha_inicio + i if navio.direcao == "vertical" else linha_inicio
            c = coluna_inicio + i if navio.direcao == "horizontal" else coluna_inicio

            if not (0 <= r < self._linhas and 0 <= c < self._colunas): # Verifica limites e se a célula já está ocupada por outro navio
                 return False
            if self._grid[r][c] != 0:
                 return False 

        return True # Se chegou aqui, todas as posições são válidas

    def colocar_navio(self, linha_inicio: int, coluna_inicio: int, navio: BaseNavio) -> bool:
        # tenta colocar um navio no tabuleiro. Retorna True se bem-sucedido, False caso nao der certo
        if self.pode_colocar_navio(linha_inicio, coluna_inicio, navio):
            posicoes = []
            for i in range(navio.tamanho):
                r = linha_inicio + i if navio.direcao == "vertical" else linha_inicio
                c = coluna_inicio + i if navio.direcao == "horizontal" else coluna_inicio
                self._grid[r][c] = 1 # marca a celula como ocupada por navio
                posicoes.append((r, c))

            navio.posicoes = posicoes # salva as posicoes no objeto navio
            self._navios.append(navio) # add navio na lista
            return True

        return False

    # implementacao do metodo abstrato desenhar de ElementoJogo
    def desenhar(self, tela: pygame.Surface, offset_x: int, offset_y: int, mostrar_navios: bool = False):
        # desenha o tabuleiro e seus conteúdos (água, tiros, navios se visíveis)
        # desenha o fundo da agua e os marcadores de tiro primeiro
        for linha in range(self._linhas):
            for coluna in range(self._colunas):
                x = offset_x + coluna * TAMANHO_CELULA
                y = offset_y + linha * TAMANHO_CELULA
                rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)

                valor_celula = self._grid[linha][coluna]
                cor = AZULCLARO 

                if valor_celula == 2: # acertou
                    cor = VERDE
                elif valor_celula == 3: # errou na agua
                    cor = VERMELHO

                pygame.draw.rect(tela, cor, rect)
                pygame.draw.rect(tela, PRETO, rect, 1) # borda do quadradinn

            for navio in self._navios:
                if mostrar_navios or navio.esta_afundado():
                    navio.desenhar(tela, offset_x, offset_y, True, self._grid)

    def atacar(self, linha: int, coluna: int) -> bool | None:
        # processa um ataque em uma célula do tabuleiro.
        # retorna True para acerto, False para água, None para posição já atacada
        if not (0 <= linha < self._linhas and 0 <= coluna < self._colunas):
            return None

        valor_celula = self._grid[linha][coluna]

        if valor_celula in [2, 3]:
            return None

        if valor_celula == 1:
            self._grid[linha][coluna] = 2 
            
            for navio in self._navios:
                if (linha, coluna) in navio.posicoes:
                    navio.atingir(linha, coluna) 
                    break
            return True

        elif valor_celula == 0:
            self._grid[linha][coluna] = 3 
            return False 

        return None

    def todos_navios_afundados(self) -> bool:
        # verifica se todos os navios no tabuleiro foram afundados
        if not self._navios:
            return False

        for navio in self._navios:
            if not navio.esta_afundado():
                return False

        return True