# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 127:
# 103606 Henrique Silva
# 103624 Afonso Azaruja

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, grid, row, col):
        self.board = grid
        self.row = row
        self.col = col

    def insert(self, row: int, col: int, val):
        """Insere peça no board e atualiza os espaços livres e o número de peças
        que cabem em cada linha e coluna."""
        if 0 <= row <= 9 and 0 <= col <= 9:
            if self.get_value(row, col) == None:
                self.free_row[row] -= 1
                self.free_col[col] -= 1
                if val != "W" and val != ".":
                    self.row[row] -= 1
                    self.col[col] -= 1
                self.board[row][col] = val
                return self

    def calculate_state(self, hints):
        """Calcula o estado inicial do board"""
        self.free_row = [10 for _ in range(10)]
        self.free_col = [10 for _ in range(10)]

        for j in hints:
            r = int(j[0])
            c = int(j[1])
            self.insert(r, c, j[2])

            if j[2] == "C":
                if self.get_value(r-1, c-1) == None:
                    self.insert(r-1, c-1, ".")
                if self.get_value(r-1, c) == None:
                    self.insert(r-1, c, ".")
                if self.get_value(r-1, c+1) == None:
                    self.insert(r-1, c+1, ".")
                if self.get_value(r, c+1) == None:
                    self.insert(r, c+1, ".")
                if self.get_value(r+1, c+1) == None:
                    self.insert(r+1, c+1, ".")
                if self.get_value(r+1, c) == None:
                    self.insert(r+1, c, ".")
                if self.get_value(r+1, c-1) == None:
                    self.insert(r+1, c-1, ".")
                if self.get_value(r, c-1) == None:
                    self.insert(r, c-1, ".")

            if j[2] == "T":
                pass
            if j[2] == "R":
                pass
            if j[2] == "B":
                pass
            if j[2] == "L":
                pass
            if j[2] == "M":
                pass

        ### caso free_row(col) == row(col) então pode ser preenchida
        i = 0
        for j in self.row:
            if j == 0:
                self.fill_row(i)
            i += 1

        i = 0
        for j in self.col:
            if j == 0:
                self.fill_col(i)
            i += 1

        return self

    def print_board(self):
        """Faz print do board no terminal."""
        print(self.row)
        print(self.col)
        for i in range(10):
            for j in range(10):
                if(self.get_value(i, j) == None):
                    sys.stdout.write("?")
                else:
                    sys.stdout.write(self.board[i][j])
            sys.stdout.write("\n")
        print(self.free_row)
        print(self.free_col)


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row <= 9 and 0 <= col <= 9:
            return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col-1), self.get_value(row, col+1))
    
    def adjacent_diagonal_values(self, row: int, col: int) -> (str, str, str, str):
        """Devolve os valores que se encontram nas diagonais, começando pelo,
        canto superior esquerdo, seguindo os ponteiros do relógio."""
        return (
            self.get_value(row-1, col-1), 
            self.get_value(row-1, col+1),
            self.get_value(row+1, col+1),
            self.get_value(row+1, col-1))
    
    def adjacent_values(self, row: int, col: int) -> (str, str, str, str, str, str, str, str):
        """Devolve os valores à volta da coordenada"""
        return (
            self.get_value(row-1, col-1),
            self.get_value(row-1, col), 
            self.get_value(row-1, col+1),
            self.get_value(row, col+1),
            self.get_value(row+1, col+1),
            self.get_value(row+1, col),
            self.get_value(row+1, col-1),
            self.get_value(row, col-1) 
        )

    def fill_row(self, row: int):
        """Preenche as linhas que já estão completas com água"""
        for i in range(10):
            if self.get_value(row, i) == None:
                self.insert(row, i, ".")
        return self

    def fill_col(self, col: int):
        """Preenche as colunas que já estão completas com água"""
        for i in range(10):
            if self.get_value(i, col) == None:
                self.insert(i, col, ".")
        return self

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
                
        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        row = list(map(int, sys.stdin.readline().split()[1:]))
        col = list(map(int, sys.stdin.readline().split()[1:]))
        num = int(sys.stdin.readline())
        hints = []
        grid = np.full((10,10), None, dtype=object)
        for _ in range(num):
            hints.append(tuple(sys.stdin.readline().split()[1:]))
        return Board(grid, row, col).calculate_state(hints)

    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    Board.print_board(board)
