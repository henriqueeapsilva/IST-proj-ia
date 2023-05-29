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

BOARD_SIZE = 10
ROW_HINTS = []
COL_HINTS = []
PIECES = ('t', 'T', 'b', 'B', 'r', 'R', 'l', 'L', 'u')

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

    def __init__(self, row, col):
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), None, dtype=object)
        self.row = row
        self.col = col
        self.hint_row = row[:]
        self.hint_col = col[:]
        self.free_row = [BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.free_col = [BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.boats = [4, 3, 2, 1]
        self.unknown_coord = []
        self.coord_boats = []

    def set_value(self, row: int, col: int, val):
        """Insere peça no board e atualiza os espaços livres e o número de peças
        que cabem em cada linha e coluna."""
        if 0 <= row <= 9 and 0 <= col <= 9:
            if self.get_value(row, col) is None:

                self.free_row[row] -= 1
                self.free_col[col] -= 1
                
                if val.lower() != 'w':
                    self.row[row] -= 1
                    self.col[col] -= 1
                    self.coord_boats.append((row, col))
                    self.coord_boats.sort(key=lambda c: (c[0], c[1]))

                    if val.lower() == 'c':
                        self.circle_case(row, col)
                        self.boats[0] -= 1
                        self.coord_boats.remove((row, col))

                    elif val.lower() == 't':
                        self.top_case(row, col)

                    elif val.lower() == 'r':
                        self.right_case(row, col)

                    elif val.lower() == 'b':
                        self.bottom_case(row, col)

                    elif val.lower() == 'l':
                        self.left_case(row, col)

                    elif val.lower() == 'm':
                        self.middle_case(row, col)

                    else:
                        self.middle_case(row, col)
                        self.unknown_coord.append((row, col))
                        self.unknown_coord.sort(key=lambda c: (c[0], c[1]))
                
                self.board[row][col] = val
            
            elif val != 'w' and (self.get_value(row, col) == 'u' or val.isupper()):
                self.board[row][col] = val

        return self

    def count_boats(self):
        ### TODO: ESTA MAL, ISTO FODE TUDO,
        ### TODO: ARRANJAR FORMA MELHOR QUE NAO ELIMINE AS COORD???
        i = 0
        while len(self.coord_boats) > i:
            length = 0
            row = self.coord_boats[i][0]
            col = self.coord_boats[i][1]
            
            h = self.adjacent_horizontal_values(row, col)
            v = self.adjacent_vertical_values(row, col)
            
            if self.get_value(row, col).lower() == 't' or self.get_value(row, col).lower() == 'l':
            
                if v[1] is not None and v[1] != 'w' and v[1] != 'W':
                    while (row + length, col) in self.coord_boats:
                        self.coord_boats.remove((row + length, col))
                        length += 1
            
                    if self.get_value(row + length - 1, col).lower() != 'b':
                        continue

                elif h[1] is not None and h[1] != 'w' and h[1] != 'W':
                    while (row, col + length) in self.coord_boats:
                        self.coord_boats.remove((row, col + length))
                        length += 1
                    
                    if self.get_value(row, col + length - 1).lower() != 'r':
                        continue
            
                length -= 1
                self.boats[length] -= 1
            
            else:
                i += 1

    def circle_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r, c-1, 'w')

    def top_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r, c-1, 'w')
        self.set_value(r+2, c-1, 'w')
        self.set_value(r+2, c+1, 'w')
        self.set_value(r+1, c, 'u')

    def right_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r+1, c-2, 'w')
        self.set_value(r-1, c-2, 'w')
        self.set_value(r, c-1, 'u')
    
    def bottom_case(self, r: int, c: int):

        self.set_value(r-2, c-1, 'w')
        self.set_value(r-2, c+1, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r, c-1, 'w')
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'u')
    
    def left_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c-1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r+1, c+2, 'w')
        self.set_value(r-1, c+2, 'w')
        self.set_value(r, c+1, 'u')

    def middle_case(self, r: int, c: int):
        """"Funciona para ambas as peças m e u."""
        self.set_value(r - 1, c - 1, 'w')
        self.set_value(r - 1, c + 1, 'w')
        self.set_value(r + 1, c + 1, 'w')
        self.set_value(r + 1, c - 1, 'w')

    def process_unknown(self):
        ### Obriga ser peca: h[0],h[1] != 'w' and h[0],h[1] != None
        for coord in self.unknown_coord:
            row = coord[0]
            col = coord[1]
            v = self.adjacent_vertical_values(row, col)
            h = self.adjacent_horizontal_values(row, col)

            v = tuple(element.lower() if element is not None else None for element in v)
            h = tuple(element.lower() if element is not None else None for element in h)


            #circle piece
            if ((h[0] == 'w' and h[1] == 'w' and v[0] == 'w' and v[1] == 'w')
                or (row == 0
                    and ((col == 0 and v[1] == 'w' and h[1] == 'w')
                    or (col == 9 and v[1] == 'w' and h[0] == 'w')
                    or (h[0] == 'w' and h[1] == 'w' and v[1] == 'w')))

                or (row == 9
                    and ((col == 9 and v[0] == 'w' and h[0] == 'w')
                    or (col == 0 and v[0] == 'w' and h[1] == 'w')
                    or (h[0] == 'w' and h[1] == 'w' and v[0] == 'w')))

                or (col == 0 and (v[0] == 'w' and v[1] == 'w' and h[1] == 'w'))

                or (col == 9 and (v[0] == 'w' and v[1] == 'w' and h[0] == 'w'))):
                self.set_value(row, col, 'c')
                self.coord_boats.remove((row, col))
                self.boats[0] -= 1
                self.unknown_coord.remove((row, col))

            # top piece
            elif ((v[0] == 'w' or row == 0)
                and (((h[0] == 'w' and h[1] == 'w')
                or (col == 0 and h[1] == 'w')
                or (col == 9 and h[0] == 'w'))
                    and v[1] !=  'w' and v[1] is not None
                    or (v[1] == 'm' or v[1] == 'M'))):
                self.set_value(row, col, 't')
                self.unknown_coord.remove((row, col))

            # bottom piece
            elif ((v[1] == 'w' or row == 9)
                and (((h[0] == 'w' and h[1] == 'w')
                or (col == 0 and h[1] == 'w')
                or (col == 9 and h[0] == 'w'))
                   and v[0] !=  'w' and v[0] is not None
                   or (v[0] == 'm' or v[0] == 'M'))):
                self.set_value(row, col, 'b')
                self.unknown_coord.remove((row, col))

            # horizontal boat middle piece
            elif ((v[0] == 'w' or row == 0)
                and (h[0] != 'w'
                and h[1] != 'w'
                and h[0] is not None
                and h[1] is not None)):
                self.set_value(row, col, 'm')
                self.unknown_coord.remove((row, col))

            # vertical boat middle piece
            elif ((h[0] == 'w' or col == 0)
                and (v[0] != 'w'
                and v[1] != 'w'
                and v[0] is not None
                and v[1] is not None)):
                self.set_value(row, col, 'm')
                self.unknown_coord.remove((row, col))

            # right piece
            elif ((h[1] == 'w' or col == 9)
                and (((v[0] == 'w' and v[1] == 'w')
                or (row == 0 and v[1] == 'w')
                or (row == 9 and v[0] == 'w'))
                    and h[0] != 'w' and h[0] is not None)
                    or (h[0] == 'm' or h[0] == 'M')):
                self.set_value(row, col, 'r')
                self.unknown_coord.remove((row, col))

            # left piece
            elif ((h[0] == 'w' or col == 0)
                and (((v[0] == 'w',v[1] == 'w')
                or (row == 0 and v[1] == 'w')
                or (row == 9 and v[0] == 'w'))
                    and h[1] != 'w' and h[1] is not None)
                    or (h[0] == 'm' or h[0] == 'M')):
                self.set_value(row, col, 'l')
                self.unknown_coord.remove((row, col))

            else:
                continue

    def process_middle(self):
        for coord in self.coord_boats:
            row = coord[0]
            col = coord[1]
            if self.get_value(row, col).lower() == 'm':
                v = self.adjacent_vertical_values(row, col)
                h = self.adjacent_horizontal_values(row, col)

                v = tuple(element.lower() if element is not None else None for element in v)
                h = tuple(element.lower() if element is not None else None for element in h)

                if v[0] == 'w' or v[1] == 'w' or row == 0 or row == 9:
                    self.set_value(row, col - 1, 'u')
                    self.set_value(row, col + 1, 'u')
                    self.set_value(row - 1, col, 'w')
                    self.set_value(row + 1, col, 'w')

                if h[0] == 'w' or h[1] == 'w' or col == 0 or col == 9:
                    self.set_value(row - 1, col, 'u')
                    self.set_value(row + 1, col, 'u')
                    self.set_value(row, col - 1, 'w')
                    self.set_value(row, col + 1, 'w')

    def calculate_actions(self):
        ### TODO: ESTA MAL LENGTH - 1 NOS MEIOS DEVERIA SER A FORMA CORRETA
        ### TODO: PROVAVELMENTE count_boats ESTA A FODER ISTO
        length = 3
        while length >= 0:
            if self.boats[length] > 0:
                break
            length -= 1

        actions = []
        print(self.boats)
        if length > 1:
            for row in range(BOARD_SIZE):
                if self.hint_row[row] > length:
                    for col in range(BOARD_SIZE - length):
                        x = self.get_value(row, col)
                        # analisa a primeira coordenada
                        if ((x != 'u' and x != 'l' and x != 'L' and x is not None)
                        or (self.adjacent_values_left(row, col) in PIECES)):
                            continue

                        break_outer = False

                        # analisa as coordenadas interiores
                        for j in range(length):
                            x = self.get_value(row, col + j + 1)
                            print(x)
                            if ((x != 'u' and x != 'm' and x != 'M' and x is not None)
                            or (self.adjacent_vertical_values(row, col + j + 1) in PIECES)):
                                break_outer = True
                                break

                        if break_outer:
                            continue
                        # analisa a ultima coordenada
                        x = self.get_value(row, col + length)
                        if ((x != 'u' and x != 'r' and x != 'R' and x is not None)
                        or (self.adjacent_values_right(row, col + length) in PIECES)):
                            continue

                        actions.append(((row, col),(row, col + length)))

            for col in range(BOARD_SIZE):
                if self.hint_col[col] > length:
                    for row in range(BOARD_SIZE - length):
                        x = self.get_value(row, col)
                        if ((x != 'u' and x != 't' and x != 'T' and x is not None)
                        or (self.adjacent_values_top(row, col) in PIECES)):
                            continue

                        break_outer = False

                        print(length)
                        for j in range(length):
                            x = self.get_value(row+j+1, col)
                            if ((x != 'u' and x != 'm' and x != 'M' and x is not None)
                            or (self.adjacent_horizontal_values(row+j+1, col) in PIECES)):
                                break_outer = True
                                break

                        if break_outer:
                            continue

                        x = self.get_value(row + length, col)
                        if ((x != 'u' and x != 'b' and x != 'B' and x is not None)
                        or (self.adjacent_values_bottom(row + length, col) in PIECES)):
                            continue

                        actions.append(((row, col), (row + length, col)))

        elif length == 1:
            for row in range(BOARD_SIZE):
                if self.hint_row[row] > 0:
                    for col in range(BOARD_SIZE - length):
                        x = self.get_value(row, col)
                        y = self.get_value(row, col + 1)
                        if ((x != 'u' and x != 'l' and x != 'L' and x is not None) and (y != 'u' and y != 'r' and y != 'R' and y is not None)):
                            continue

                        actions.append(((row, col),(row, col + length)))

            for col in range(BOARD_SIZE):
                if self.hint_col[col] > 0:
                    for row in range(BOARD_SIZE - length):
                        x = self.get_value(row, col)
                        y = self.get_value(row + 1, col)
                        if ((x != 'u' and x != 't' and x != 'T' and x is not None) and (y != 'u' and y != 'b' and y != 'B' and y is not None)):
                            continue

                        actions.append(((row, col), (row + length, col)))

        print(self.boats)
        print(self)
        return actions

    def calculate_state(self, hints):
        """Calcula o estado inicial do board."""
        for hint in hints:
            r = int(hint[0])
            c = int(hint[1])
            v = hint[2]
            self.set_value(r, c, v)

        while True:
            state = self.free_row[:] + self.unknown_coord[:]
            self.fill_water()
            self.fill_boats()
            self.process_unknown()
            self.process_middle()
            if state == self.free_row + self.unknown_coord:
                break

        self.count_boats()

        return self

    def print_board(self):
        """Faz print do board no terminal."""
        print("(ROW) Peças:", self.row, " Livres:", self.free_row, '\n')
        print("(COL) Peças:", self.col, " Livres:", self.free_col, '\n')
        print("(COR)", len(self.coord_boats), self.coord_boats, '\n')
        print("(UKN)", len(self.unknown_coord), self.unknown_coord, '\n')
        print("(BTS)", self.boats, '\n')

        for i in range(10):
            for j in range(10):
                if self.get_value(i, j) is None:
                    sys.stdout.write('?')
                else:
                    if self.get_value(i,j) == 'w':
                        sys.stdout.write('.')
                    else:
                        sys.stdout.write(self.board[i][j])
            sys.stdout.write('\n')

    def __repr__(self):
        grid = ""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = self.get_value(row, col)
                if x == 'w':
                    x = '.'
                elif x is None:
                    x = '?'
                grid += x
            grid += '\n'
        return grid

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row <= 9 and 0 <= col <= 9:
            return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return self.get_value(row - 1, col), self.get_value(row + 1, col)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return self.get_value(row, col - 1), self.get_value(row, col + 1)

    def adjacent_values_left(self, row: int, col: int) -> (str, str, str, str, str):
        """Devolve os valores à volta da coordenada"""
        return (
            self.get_value(row-1, col),
            self.get_value(row-1, col-1),
            self.get_value(row, col-1),
            self.get_value(row+1, col-1),
            self.get_value(row+1, col)
        )

    def adjacent_values_right(self, row: int, col: int) -> (str, str, str, str, str):
        """Devolve os valores à volta da coordenada"""
        return (
            self.get_value(row-1, col),
            self.get_value(row-1, col+1),
            self.get_value(row, col+1),
            self.get_value(row-1, col+1),
            self.get_value(row-1, col)
        )

    def adjacent_values_top(self, row: int, col: int) -> (str, str, str, str, str):
        """Devolve os valores à volta da coordenada"""
        return (
            self.get_value(row, col-1),
            self.get_value(row-1, col-1),
            self.get_value(row-1, col),
            self.get_value(row-1, col+1),
            self.get_value(row, col+1)
        )

    def adjacent_values_bottom(self, row: int, col: int) -> (str, str, str, str, str):
        """Devolve os valores à volta da coordenada"""
        return (
            self.get_value(row, col+1),
            self.get_value(row+1, col+1),
            self.get_value(row+1, col),
            self.get_value(row+1, col-1),
            self.get_value(row, col-1)
        )

    def fill_boats(self):
        """No caso em que os espaços livres numa linha (coluna) é igual ao
        número de peças de barcos que faltam nessa linha (coluna), essa linha
        (coluna) é preenchida com peças de barcos."""
        for i in range(BOARD_SIZE):
            if self.row[i] != 0 and self.free_row[i] == self.row[i]:
                for col in range(BOARD_SIZE):
                    if self.get_value(i, col) is None:
                        self.set_value(i, col, 'u')
                        self.set_value(i - 1, col - 1, 'w')
                        self.set_value(i - 1, col + 1, 'w')
                        self.set_value(i + 1, col + 1, 'w')
                        self.set_value(i + 1, col - 1, 'w')

            if self.col[i] != 0 and self.free_col[i] == self.col[i]:
                for row in range(BOARD_SIZE):
                    if self.get_value(row, i) is None:
                        self.set_value(row, i, 'u')
                        self.set_value(row - 1, i - 1, 'w')
                        self.set_value(row - 1, i + 1, 'w')
                        self.set_value(row + 1, i + 1, 'w')
                        self.set_value(row + 1, i - 1, 'w')

    def fill_water(self):
        for row, val in enumerate(self.row):
            if val == 0:
                for col in range(BOARD_SIZE):
                    self.set_value(row, col, 'w')

        for col, val in enumerate(self.col):
            if val == 0:
                for row in range(BOARD_SIZE):
                    self.set_value(row, col, 'w')

    def execute_action(self, action: list):
        horizontal = action[1][0] - action[0][0]
        vertical = action[1][1] - action[0][1]

        new_row = self.row[:]
        new_col = self.col[:]
        new_board = Board(new_row, new_col)
        new_board.board = self.board[:][:]
        new_board.free_row = self.free_row[:]
        new_board.free_col = self.free_col[:]
        new_board.boats = self.boats[:]
        new_board.unknown_coord = self.unknown_coord[:]
        new_board.coord_boats = self.coord_boats[:]
        new_board.hint_row = self.hint_row[:]
        new_board.hint_col = self.hint_col[:]

        if horizontal == vertical:
            new_board.set_value(action[0][0], action[0][1], 'c')

        elif horizontal == 0:
            if vertical == 1:
                new_board.set_value(action[0][0], action[0][1], 'l')
                new_board.set_value(action[1][0], action[1][1], 'r')
            elif vertical == 2:
                new_board.set_value(action[0][0], action[0][1], 'l')
                new_board.set_value(action[0][0], action[0][1] + 1, 'm')
                new_board.set_value(action[1][0], action[1][1], 'r')
            elif vertical == 3:
                new_board.set_value(action[0][0], action[0][1], 'l')
                new_board.set_value(action[0][0], action[0][1] + 1, 'm')
                new_board.set_value(action[0][0], action[0][1] + 2, 'm')
                new_board.set_value(action[1][0], action[1][1], 'r')

        elif vertical == 0:
            if horizontal == 1:
                new_board.set_value(action[0][0], action[0][1], 't')
                new_board.set_value(action[1][0], action[1][1], 'b')
            elif horizontal == 2:
                new_board.set_value(action[0][0], action[0][1], 't')
                new_board.set_value(action[0][0] + 1, action[0][1], 'm')
                new_board.set_value(action[1][0], action[1][1], 'b')
            elif horizontal == 3:
                new_board.set_value(action[0][0], action[0][1], 't')
                new_board.set_value(action[0][0] + 1, action[0][1], 'm')
                new_board.set_value(action[0][0] + 2, action[0][1], 'm')
                new_board.set_value(action[1][0], action[1][1], 'b')

        while True:
            state = new_board.free_row[:] + new_board.unknown_coord[:]
            new_board.fill_water()
            new_board.fill_boats()
            new_board.process_unknown()
            new_board.process_middle()
            if state == new_board.free_row + new_board.unknown_coord:
                break

#        print(action)
#        print(new_board)
        new_board.count_boats()

        return new_board




    """ -------------------- Validade (pode ser útil) ---------------------------- """
    def is_valid(self):
        row_pieces = 0
        col_pieces = 0
        for r in self.row:
            row_pieces += r
        for c in self.col:
            col_pieces += c
        return row_pieces == col_pieces

    """--------------------------------------------------------------------------------"""

    """ -------------------------- GOAL TEST functions ------------------------------------------ """

    def get_remaining_pieces(self):
        """ Obtém o número de peças que ainda faltam colocar
        Esta implementação implica no final após ser encontrado o goal_test
        caso seja necessário se coloque o resto das águas necessárias
        """
        pieces = 0
        for r in self.row:
            pieces += r
        return pieces

    def all_boats_places(self):
        """ verifica se todos os barcos já foram colocados
        Esta implementação implica que sempre que coloquemos um barco se verifique se completa um barco
        e que se vá retirando o número de barcos a ser colocados no array de barcos.
        """
        for b in self.boats:
            if b != 0:
                return False
        return True

    """ -------------------------------------------------------------------------------------------- """


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
        for _ in range(num):
            hints.append(tuple(sys.stdin.readline().split()[1:]))
        return Board(row, col).calculate_state(hints)


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if not state.board.is_valid():
            return []
        return state.board.calculate_actions()

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        return BimaruState(state.board.execute_action(action))

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.is_valid() and state.board.get_remaining_pieces() == 0 and state.board.all_boats_places()

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
    goal_node = depth_first_tree_search(bimaru)
    print(goal_node.state.board)
