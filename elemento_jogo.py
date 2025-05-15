
from abc import ABC, abstractmethod

class ElementoJogo(ABC):
    # classe base abstrata para elementos desenháveis do jogo
    def __init__(self):
        pass

    @abstractmethod
    def desenhar(self, tela, offset_x, offset_y):
        # metodo abstrato para desenhar o elemento na tela
        pass