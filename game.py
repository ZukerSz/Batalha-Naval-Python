
import pygame
import sys
import random

from constantes import (LINHAS_TABULEIRO, COLUNAS_TABULEIRO, LARGURA_TELA_PX, ALTURA_TELA_PX, MARGEM_ESQ_PX,
                       MARGEM_TOP_PX, LARGURA_TABULEIRO_PX, ALTURA_TABULEIRO_PX,
                       ESPACO_ENTRE_TABULEIROS, ALTURA_INTERFACE_JOGO,
                       PRETO, CINZACLARO, VERDEVENCEDOR, VERMELHO, TAMANHO_CELULA)

# importa classes e informacoes de outros arquivos
from tabuleiro import Tabuleiro
from tipos_de_navio import INFO_NAVIOS, MAX_NAVIOS_JOGADOR, BaseNavio

class Jogo:
    """Controla o fluxo do jogo Batalha Naval."""
    def __init__(self):
        pygame.display.set_mode((LARGURA_TELA_PX, ALTURA_TELA_PX))
        pygame.display.set_caption("Batalha Naval")
        self._tela = pygame.display.get_surface()

        # aqui sao as fontes usadas para fazer este jogo
        self._fonte = pygame.font.SysFont(None, 25)
        self._fonte_coords = pygame.font.SysFont(None, 18) # fonte menor para coordenadas

        self._tabuleiro_jogador = Tabuleiro()
        self._tabuleiro_ia = Tabuleiro()

        # offsets de desenho para os tabuleiros, necessario para desenhar e pegar os cliques do mouse
        self._offset_jogador_x = MARGEM_ESQ_PX
        self._offset_jogador_y = MARGEM_TOP_PX
        self._offset_ia_x = MARGEM_ESQ_PX + LARGURA_TABULEIRO_PX + ESPACO_ENTRE_TABULEIROS
        self._offset_ia_y = MARGEM_TOP_PX

        # tamanho inicial do navio a ser posicionado, que comeca pegando o menor tamanho
        self._tamanho_navio_atual = min(INFO_NAVIOS.keys()) if INFO_NAVIOS else None

        self._direcao_navio_atual = "horizontal"
        self._tipos_navios_colocados_jogador = set()

        self._jogo_iniciado = False
        self._vencedor = None
        self._turno_jogador = True

        self._mensagem_notf = "Selecione no teclado numérico entre (1-6) para selecionar um navio, Mude a direção (R), Posicione (Clique no seu tabuleiro)."
        self._clock = pygame.time.Clock()

    def _pegar_celula(self, pos_mouse: tuple[int, int], offset_x: int, offset_y: int) -> tuple[int, int]:
        # converte a posição do mouse na tela para a linha e coluna do tabuleiro.
        # considera o offset do tabuleiro na tela.
        x_mouse, y_mouse = pos_mouse
        x_relativo = x_mouse - offset_x
        y_relativo = y_mouse - offset_y

        if 0 <= x_relativo < LARGURA_TABULEIRO_PX and 0 <= y_relativo < ALTURA_TABULEIRO_PX:
            coluna = x_relativo // TAMANHO_CELULA
            linha = y_relativo // TAMANHO_CELULA
            return linha, coluna
        return -1, -1

    def _gerar_navios_ia(self):
        # posiciona aleatoriamente os navios da IA
        tipos_navios_ia = list(INFO_NAVIOS.keys())
        navios_colocados_ia = 0
        for tamanho in tipos_navios_ia:
            ClasseNavio = INFO_NAVIOS[tamanho]["classe"]
            tentativas = 0
            max_tentativas = 150
            while tentativas < max_tentativas:
                direcao = random.choice(["horizontal", "vertical"])
                navio_ia = ClasseNavio(direcao)
                linha = random.randint(0, LINHAS_TABULEIRO - 1)
                coluna = random.randint(0, COLUNAS_TABULEIRO - 1)
                if self._tabuleiro_ia.colocar_navio(linha, coluna, navio_ia):
                    navios_colocados_ia += 1
                    break
                tentativas += 1
            if tentativas == max_tentativas:
                print(f"AVISO: IA não conseguiu posicionar o navio de tamanho {tamanho} após {max_tentativas} tentativas.")
        print(f"IA posicionou {navios_colocados_ia} navios.")

    def _ataque_ia(self):
        # realiza um ataque da IA
        self._mensagem_notf = "A IA está pensando onde atacar..."
        self._desenhar_tudo()
        pygame.display.flip()

        pygame.time.wait(100)

        celulas_disponiveis = [(r, c) for r in range(self._tabuleiro_jogador.linhas)
                                     for c in range(self._tabuleiro_jogador.colunas)
                                     if self._tabuleiro_jogador.grid[r][c] in [0, 1]]

        if not celulas_disponiveis:
            if self._vencedor is None:
                self._mensagem_notf = "IA sem jogadas disponíveis!"
                self._turno_jogador = True
            return

        linha, coluna = random.choice(celulas_disponiveis)
        resultado = self._tabuleiro_jogador.atacar(linha, coluna)

        if resultado is True:
            self._mensagem_notf = f"IA ACERTOU um navio! ({linha},{coluna})!"
            if self._tabuleiro_jogador.todos_navios_afundados():
                self._vencedor = "IA"
                self._mensagem_notf = "Todos os seus navios foram afundados! IA venceu o jogo."
                return

        elif resultado is None:
            self._mensagem_notf = "IA ja tentou atacar posição já atingida."
            pass

        if self._vencedor is None:
            self._turno_jogador = True

    def _desenhar_tudo(self):
        # desenha todos os elementos do jogo na tela, incluindo tabuleiros e interface
        self._tela.fill(CINZACLARO)

        # desenha os tabuleiros usando os offsets
        self._tabuleiro_jogador.desenhar(self._tela, self._offset_jogador_x, self._offset_jogador_y, mostrar_navios=True)
        mostrar_navios_ia = True if self._vencedor else False
        self._tabuleiro_ia.desenhar(self._tela, self._offset_ia_x, self._offset_ia_y, mostrar_navios=mostrar_navios_ia)

        # desenho da interface
        y_interface = self._offset_jogador_y + ALTURA_TABULEIRO_PX + 5
        pygame.draw.line(self._tela, PRETO, (0, self._offset_jogador_y + ALTURA_TABULEIRO_PX), (LARGURA_TELA_PX, self._offset_jogador_y + ALTURA_TABULEIRO_PX), 2)

        if not self._jogo_iniciado:
            nome_navio = INFO_NAVIOS.get(self._tamanho_navio_atual, {"nome": "N/A"})["nome"]
            sel_txt = self._fonte.render(f"Navio Selecionado: {nome_navio}({self._tamanho_navio_atual})", True, PRETO)
            rot_txt = self._fonte.render(f"Girar direção (R): {self._direcao_navio_atual}", True, PRETO)
            colocados = sorted(list(self._tipos_navios_colocados_jogador))
            nomes_colocados = [INFO_NAVIOS[t]["nome"] for t in colocados if t in INFO_NAVIOS]
            col_txt = self._fonte.render(f"Navios colocados ({len(colocados)}/{MAX_NAVIOS_JOGADOR}): {', '.join(nomes_colocados)}", True, PRETO)

            self._tela.blit(sel_txt, (10, y_interface)); y_interface += 20
            self._tela.blit(rot_txt, (10, y_interface)); y_interface += 20
            self._tela.blit(col_txt, (10, y_interface)); y_interface += 20

        elif self._jogo_iniciado and not self._vencedor:
            turno_txt = self._fonte.render(f"Vez de jogar: {'Sua vez' if self._turno_jogador else 'Vez da IA'}", True, PRETO)
            self._tela.blit(turno_txt, (10, y_interface)); y_interface += 25
            if self._turno_jogador:
                inst_txt = self._fonte.render("Clique no tabuleiro da DIREITA para atacar!", True, PRETO)
                self._tela.blit(inst_txt, (10, y_interface)); y_interface += 20

        if self._mensagem_notf:
            notf_txt = self._fonte.render(f"Notificação: {self._mensagem_notf}", True, PRETO)
            self._tela.blit(notf_txt, (10, y_interface)); y_interface += 20

        if self._vencedor:
            cor = VERDEVENCEDOR if self._vencedor == "Jogador" else VERMELHO
            fonte_vitoria = pygame.font.SysFont(None, 36)
            vic_txt = fonte_vitoria.render(f"Fim de jogo! O VENCEDOR foi: {self._vencedor.upper()}", True, cor)
            l_txt, a_txt = vic_txt.get_size()
            px = (LARGURA_TELA_PX - l_txt) // 2
            py = self._offset_jogador_y + ALTURA_TABULEIRO_PX + (ALTURA_INTERFACE_JOGO - a_txt) // 2
            self._tela.blit(vic_txt, (px, py ))

        pygame.display.flip()
        self._clock.tick(60)

    def executar(self): # metodo executar
        # inicia e executa o loop principal do jogo
        rodando = True
        while rodando:
            eventos = pygame.event.get()
            pos_mouse = pygame.mouse.get_pos()

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False

                # eventos de posicionamento, antes do jogo iniciar
                if not self._jogo_iniciado:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            self._direcao_navio_atual = "vertical" if self._direcao_navio_atual == "horizontal" else "horizontal"
                            self._mensagem_notf = f"Direção: {self._direcao_navio_atual}"
                        elif evento.unicode.isdigit():
                            tamanho_desejado = int(evento.unicode)
                            if tamanho_desejado in INFO_NAVIOS:
                                if tamanho_desejado in self._tipos_navios_colocados_jogador:
                                    self._mensagem_notf = f"{INFO_NAVIOS[tamanho_desejado]['nome']} já posicionado!"
                                else:
                                    self._tamanho_navio_atual = tamanho_desejado
                                    self._mensagem_notf = f"Selecionado: {INFO_NAVIOS[tamanho_desejado]['nome']}. Clique no seu tabuleiro para posicionar."
                            else:
                                self._mensagem_notf = f"Tamanho de navio inválido: {tamanho_desejado}. Use 1-{MAX_NAVIOS_JOGADOR}."

                    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        # tenta pegar a celula clicada no tabuleiro do jogador, usando seus offsets
                        linha, coluna = self._pegar_celula(pos_mouse, self._offset_jogador_x, self._offset_jogador_y)

                        if linha != -1: # se clicou dentro do tabuleiro do jogador
                            if self._tamanho_navio_atual is None: # garante que um tamanho foi selecionado
                                self._mensagem_notf = "Selecione um navio primeiro (1-6)."
                            elif self._tamanho_navio_atual in self._tipos_navios_colocados_jogador:
                                self._mensagem_notf = f"{INFO_NAVIOS[self._tamanho_navio_atual]['nome']} já foi posicionado. Escolha outro navio (1-{MAX_NAVIOS_JOGADOR})."
                            else:
                                ClasseNavio = INFO_NAVIOS[self._tamanho_navio_atual]["classe"] # obtem a classe do navio pelo tamanho selecionado
                                navio = ClasseNavio(self._direcao_navio_atual) # Ccia uma instancia da classe de navio

                                if self._tabuleiro_jogador.colocar_navio(linha, coluna, navio):
                                    self._tipos_navios_colocados_jogador.add(navio.tamanho)
                                    restantes = MAX_NAVIOS_JOGADOR - len(self._tipos_navios_colocados_jogador)
                                    self._mensagem_notf = f"{navio.nome} posicionado! Restam {restantes} navio(s) para posicionar."

                                    # verifica se todos os navios foram posicionados para iniciar o jogo
                                    if restantes == 0:
                                        self._gerar_navios_ia() # comeca a posicionar/gerar os navios da IA
                                        self._jogo_iniciado = True
                                        self._mensagem_notf = "Todos os navios posicionados! Jogo iniciado. Sua vez."
                                    else:
                                         proximo_tamanho = min([t for t in INFO_NAVIOS.keys() if t not in self._tipos_navios_colocados_jogador], default=None)
                                         self._tamanho_navio_atual = proximo_tamanho
                                         if proximo_tamanho:
                                             self._mensagem_notf += f" Selecione o próximo: {INFO_NAVIOS[proximo_tamanho]['nome']}({proximo_tamanho})."

                                else:
                                    self._mensagem_notf = "Você não consegue colocar o navio selecionado nesta posição."
                        else:
                            self._mensagem_notf = "Clique DENTRO do seu tabuleiro para posicionar navios."

                # eventos de jogo, apos o jogo iniciar
                elif self._jogo_iniciado and self._vencedor is None:
                    if self._turno_jogador: # só processa cliques se for o turno do jogador
                        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                            # tenta pegar a celula clicada no tabuleiro da IA, usando seus offsets
                            linha, coluna = self._pegar_celula(pos_mouse, self._offset_ia_x, self._offset_ia_y)

                            if linha != -1:
                                resultado = self._tabuleiro_ia.atacar(linha, coluna)
                                passar_turno = False # controla passagem de turno

                                if resultado is True:
                                    if self._tabuleiro_ia.todos_navios_afundados():
                                        self._vencedor = "Jogador"
                                        self._mensagem_notf = "Todos os navios da IA afundados! Você VENCEU!"
                                        pass
                                    else:
                                        passar_turno = True # passa o turno para a IA
                                elif resultado is False:
                                    passar_turno = True # se errou, passa o turno para a IA
                                elif resultado is None:
                                    self._mensagem_notf = "Você já atacou esta posição. Tente outra no tabuleiro da IA."
                                if passar_turno and self._vencedor is None:
                                    self._turno_jogador = False
                            else:
                                self._mensagem_notf = "Clique no tabuleiro da DIREITA para atacar."

            # logica de vez da IA
            if self._jogo_iniciado and not self._turno_jogador and self._vencedor is None:
                self._ataque_ia()

            self._desenhar_tudo()

            pygame.display.flip()
            self._clock.tick(60)