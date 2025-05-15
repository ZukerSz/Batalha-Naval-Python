
import pygame
import sys

from game import Jogo

if __name__ == "__main__":
    pygame.init() # inicializa o pygame

    jogo = Jogo() # cria uma instancia da classe Jogo e inicia o jogo
    jogo.executar()

    pygame.quit() # finaliza o pygame ao sair do loop principal
    sys.exit()
