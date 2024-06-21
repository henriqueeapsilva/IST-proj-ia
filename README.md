# Artificial Intelligence 2022/23
## Project: Bimaru
### May 2, 2023

#### 1. Introduction
The project for the Artificial Intelligence (AI) course aims to develop a Python program that solves the Bimaru problem using AI techniques. The Bimaru problem, also known as Battleship Puzzle, Yubotu, or Solitaire Battleship, is a puzzle inspired by the well-known two-player Battleship game. The game was created in Argentina by Jaime Poniachik and first appeared in 1982 in the Argentine magazine Humor & Juegos. It became internationally known when it was first included in the World Puzzle Championship in 1992.

#### 2. Problem Description
According to the description in CSPlib, the Bimaru game takes place on a square grid, representing an area of the ocean. Published games usually use a 10 × 10 grid, so we will assume this dimension for the project. The ocean area contains a hidden fleet that the player must find. This fleet consists of a battleship (four squares long), two cruisers (each three squares long), three destroyers (each two squares long), and four submarines (one square each).

Ships can be oriented horizontally or vertically, and two ships do not occupy adjacent grid squares, even diagonally. The player also receives row and column counts, indicating the number of occupied squares in each row and column, and several hints. Each hint specifies the state of an individual square on the grid: water (the square is empty), circle (the square is occupied by a submarine), middle (this is a square in the middle of a battleship or cruiser), top, bottom, left, or right (this square is the end of a ship that occupies at least two squares).

Figure 1 shows an example of the initial grid layout. Figure 2 shows a solution for that same grid. We can assume that a Bimaru instance has a unique solution.

1. [CSPlib Reference](https://www.csplib.org/Problems/prob014/references/)

![Figure 1: Example of a Bimaru instance](figure1.png)

![Figure 2: Example of a solution for a Bimaru instance](figure2.png)

The images in the statement were obtained from the Sea Battle application developed by AculApps for IOS and Android.

#### 3. Objective
The objective of this project is to develop a Python 3.8 program that, given a Bimaru instance, returns a solution, i.e., a fully filled grid. The program should be developed in a file named `bimaru.py`, which reads a Bimaru instance from standard input in the format described in section 4.1. The program should solve the problem using a chosen technique and print the solution to standard output in the format described in section 4.2.

Usage:
```sh
python3 bimaru.py < <instance_file>
```

#### 4. Input and Output Format
The following format is based on the document File Format Description for Unsolvable Boards for CSPLib written by Moshe Rubin (Mountain Vista Software) in December 2005.

##### 4.1 Input Format
Bimaru problem instances consist of three parts:
1. The first line starts with the word `ROW` and contains information about the number of occupied positions in each row of the grid.
2. The second line starts with the word `COLUMN` and contains information about the number of occupied positions in each column of the grid.
3. The third line contains an integer corresponding to the number of hints.
4. The following lines start with the word `HINT` and contain the hints corresponding to the pre-filled positions.

Formally, each of the four parts described above is formatted as follows:
1. `ROW <count-0> ... <count-9>`
2. `COLUMN <count-0> ... <count-9>`
3. `<hint total>`
4. `HINT <row> <column> <hint value>`

Possible values for `<row>` and `<column>` are integers between 0 and 9. The top left corner of the grid corresponds to the coordinates (0,0). Possible values for `<hint value>` are: W (water), C (circle), T (top), M (middle), B (bottom), L (left), and R (right).

Example:
The input file describing the instance in Figure 1 is as follows:
```
ROW 2 3 2 2 3 0 1 3 2 2
COLUMN 6 0 1 0 2 1 3 1 2 4
6
HINT 0 0 T
HINT 1 6 M
HINT 3 2 C
HINT 6 0 W
HINT 8 8 B
HINT 9 5 C
```

##### 4.2 Output Format
The program's output should describe a solution to the Bimaru problem described in the input file, i.e., a fully filled grid that complies with the previously stated rules. The output should follow the format below:
- 10 lines, where each line indicates the content of the respective row of the grid.
- Pre-filled positions (corresponding to hints) are indicated by their respective uppercase letter.
- Other positions are indicated by their respective lowercase letters, except for water positions, which are represented by a dot for readability.
- All lines, including the last one, end with a newline character, i.e., \n

Example:
The output describing the solution in Figure 2 is:
```
T.....t...
b.....M..t
......b..m
..C......m
c......c.b
..........
W...t.....
t...b...t.
m.......B.
b....C....
```

```sh
T.....t...\n
b.....M..t\n
......b..m\n
..C......m\n
c......c.b\n
..........\n
W...t.....\n
t...b...t.\n
m.......B.\n
b....C....\n
```

#### 5. Implementation
This section describes the code that may be used in the project and the code that should be implemented.

##### 5.1 Code to Use
For this project, use the files provided on the course website containing the Python implementation of search algorithms. The most important aspect is to understand what these functionalities do and how to use them. These files should not be modified. If any definitions in these files need to be changed, these changes should be made in the project implementation file.

Other dependencies are not allowed, except for the Python package `numpy`, which may be useful for representing the solution and performing array operations.

###### 5.1.1 Search Algorithms
The `search.py` file contains the necessary structures to run different search algorithms, including:
- `Problem` class: Abstract representation of the search problem;
- `breadth_first_tree_search` function: Breadth-first search;
- `depth_first_tree_search` function: Depth-first search;
- `greedy_search` function: Greedy search;
- `astar_search` function: A* search.

###### 5.1.2 `BimaruState` Class
This class represents the states used in the search algorithms. The `board` member stores the grid configuration corresponding to the state. The class code is shown below. Modifications to this class are allowed, such as changes to the `__lt__(self, other)` method to support more complex tie-breaking functions. However, these changes should be properly justified with comments in the code.
```python
class BimaruState:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1
    def __lt__(self, other):
        """ This method is used in case of a tie in managing the open list in informed searches. """
        return self.id < other.id
```

##### 5.2 Code to Implement

###### 5.2.1 `Board` Class
The `Board` class is the internal representation of a Bimaru grid. The implementation of this class and its methods is free. For example, it may include methods to determine adjacent values `adjacent_vertical_values` and `adjacent_horizontal_values` that receive two arguments, the grid coordinates (row, column), and return a tuple with two strings corresponding to the adjacent values vertically (above, below) and horizontally (left, right), respectively. If there are no adjacent values, i.e., at the grid edges, or if they have not yet been filled, they return None. Other methods, such as a `get_value` method to return the value filled in a specific position, or a `print` method to print the grid in the format described in section 4.2, may also be implemented. These methods can be used to test the remaining implementation of the class.
```python
class Board:
    """ Internal representation of a Bimaru grid. """
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Returns the values immediately above and below, respectively. """
        # TODO
        pass
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Returns the values immediately to the left and right, respectively. """
        # TODO
        pass
    # TODO: other class methods
```

###### 5.2.2 `parse_instance` Function
The `parse_instance` function reads a Bimaru problem instance in the input format presented (section 4.1) and returns an object of type

 `Board` corresponding to the initial state of the grid. The code for this function is shown below.
```python
def parse_instance():
    import sys
    input = sys.stdin.read().strip().split("\n")
    row = list(map(int, input[0][4:].strip().split()))
    column = list(map(int, input[1][7:].strip().split()))
    num_hints = int(input[2])
    hints = [tuple(h.split()[1:]) for h in input[3:]]
    return row, column, num_hints, hints
```

###### 5.2.3 `Bimaru` Class
The `Bimaru` class inherits from the `Problem` class and should implement the methods `actions`, `result`, `goal_test`, and `h` (informed search heuristic). This class represents a Bimaru instance to be solved by a search algorithm. The `__init__` method receives an object of type `Board` corresponding to the initial state of the grid.

The class code is shown below.
```python
class Bimaru(Problem):
    def __init__(self, board: Board):
        """ This class builds an instance of the Bimaru problem to be solved by search algorithms. """
        # TODO
        pass
    def actions(self, state: BimaruState) -> list:
        """ Returns the possible actions that can be performed from the current state. """
        # TODO
        pass
    def result(self, state: BimaruState, action) -> BimaruState:
        """ Returns the resulting state from performing the given action. """
        # TODO
        pass
    def goal_test(self, state: BimaruState) -> bool:
        """ Returns True if the state is a goal state. """
        # TODO
        pass
    def h(self, node) -> int:
        """ Informed search heuristic """
        # TODO
        pass
```

##### 5.2.4 Main Function
The main function reads the Bimaru instance, creates a problem, selects a search algorithm, and prints the solution. The solution may include the following steps:
1. Parse the input instance:
```python
rows, cols, num_hints, hints = parse_instance()
```
2. Create the initial board and Bimaru instance:
```python
board = Board(rows, cols, num_hints, hints)
problem = Bimaru(board)
```
3. Run the search algorithm:
```python
from search import astar_search
solution = astar_search(problem)
```
4. Print the solution:
```python
solution.state.board.print()
```

#### 6. Optional Enhancements
This section includes optional enhancements that may be made:
- Implement a graphical user interface (GUI) to show the grid and solution;
- Implement more efficient data structures;
- Implement additional heuristics for the search algorithm;
- Implement more complex tie-breaking functions in the `__lt__` method of the `BimaruState` class.
