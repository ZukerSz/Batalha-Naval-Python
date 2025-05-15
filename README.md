# Batalha Naval vs IA usando Pygame

Este é um jogo de Batalha Naval clássico implementado usando a biblioteca Pygame em Python. O jogo permite que um jogador posicione seus navios em um tabuleiro e, em seguida, tente afundar os navios da Inteligência Artificial (IA) no tabuleiro adversário.

## Como Jogar

1.  **Requisitos:** Certifique-se de ter o Python instalado em seu sistema. Você também precisará instalar a biblioteca Pygame. Se ainda não a tiver, você pode instalá-la usando o pip:
    ```bash
    pip install pygame
    ```

2.  **Execução:** Para iniciar o jogo, navegue até o diretório onde você salvou o arquivo `main.py` (ou o nome que você deu ao seu arquivo de código) e execute o seguinte comando no seu terminal:
    ```bash
    python main.py
    ```

3.  **Fase de Posicionamento:**
    * No início do jogo, você verá o seu tabuleiro (à esquerda) e o tabuleiro da IA (à direita, inicialmente vazio).
    * Na parte inferior da tela, haverá instruções sobre como posicionar seus navios.
    * **Escolha o tamanho do navio:** Pressione as teclas numéricas de `1` a `6` para selecionar o tamanho do navio que você deseja posicionar (Destroyer, Lancha, Submarino, Cruzador, Encouraçado, Porta-aviões). O nome e o tamanho do navio selecionado serão exibidos na interface.
    * **Girar o navio:** Pressione a tecla `R` para alternar entre a orientação horizontal e vertical do navio. A orientação atual será mostrada na interface.
    * **Posicionar o navio:** Clique em uma célula vazia do seu tabuleiro (o da esquerda) para colocar o navio. Se a posição for válida (não sobrepõe outros navios e está dentro dos limites do tabuleiro), o navio será colocado.
    * Você precisa posicionar um de cada tipo de navio (Lancha, Fragata, Submarino, Cruzador, Encouraçado, Porta-aviões). A interface mostrará qual navio você está atualmente posicionando e quais ainda faltam.
    * Depois de posicionar todos os seus navios, a fase de jogo começará automaticamente.

4.  **Fase de Jogo:**
    * A interface indicará de quem é a vez.
    * **Se for seu turno:** Clique em uma célula do tabuleiro da IA (o da direita) para lançar um ataque.
        * Se você acertar um navio da IA, a célula ficará verde.
        * Se você acertar a água, a célula ficará vermelha.
        * Se acertar o navio por completo, a célula  correspondente ficará laranja, mostrando que o navio foi afundado.
    * **Se for o turno da IA:** A IA fará um ataque aleatório no seu tabuleiro.
        * Se a IA acertar um de seus navios, a célula correspondente no seu tabuleiro ficará verde.
        * Se a IA acertar a água, a célula correspondente no seu tabuleiro ficará vermelha.
        * Se acertar o navio por completo, a célula  correspondente ficará laranja, mostrando que o navio foi afundado.
    * O objetivo é afundar todos os navios da IA antes que a IA afunde todos os seus.

5.  **Fim de Jogo:**
    * O jogo termina quando todos os navios de um dos jogadores forem afundados.
    * Uma mensagem na parte inferior da tela declarará o vencedor ("Vencedor: Jogador" ou "Vencedor: IA").
    * Para jogar novamente, você precisará executar o script novamente.

## Autor

[Iuker Souza] [ZukerSz](https://github.com/ZukerSz)
