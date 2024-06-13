import numpy as np
import tkinter as tk

DEF_XMIN = 800 # Default minimum x value for window size
DEF_YMIN = 600 # Default minimum y value for window size

CELL_SIZE = 50 # Default size for each cell of the board display

def main() -> None:
    """
    Main entry point of the program.
    """
    # Sample sudoku board
    sample_puzzle = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    # Creates the root window
    root = tk.Tk()
    root.title("Sudoku Solver")

    # Creates canvas object to display sudoku board
    canvas = tk.Canvas(root, width=9*CELL_SIZE, height=9*CELL_SIZE, 
                       borderwidth=0, highlightthickness=0)
    canvas.pack()

    # Configures root window size
    root.geometry(f"{DEF_XMIN}x{DEF_YMIN}")
    root.minsize(DEF_XMIN, DEF_YMIN)
    
    # Initializes maps containing the numbers in the initial board
    rows, columns, cells = initialize_maps(sample_puzzle)

    solve_board(sample_puzzle, rows, columns, cells)
    display_board(canvas, sample_puzzle)

    root.mainloop()

def display_board(canvas, board: list[list[int]]) -> None:
    """
    Displays the current sudoku board.

    Args:
        canvas: Canvas object for the board display.
        board (list[list[int]]): 9x9 matrix containing the sudoku board.
    """
    # Draws the lines of the sudoku grid
    for i in range(len(board) + 1):
        width = 1 if i % 3 != 0 else 2
        canvas.create_line(0, i * CELL_SIZE, 9 * CELL_SIZE, i * CELL_SIZE,
                           fill="black", width=width)
        canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, 9 * CELL_SIZE, 
                           fill="black", width=width)
        
    # Fills in each number of the board
    for row in range(len(board)):
        for col in range(len(board[row])):
            num = board[row][col]
            if num != 0:
                x = col * CELL_SIZE + CELL_SIZE / 2
                y = row * CELL_SIZE + CELL_SIZE / 2
                canvas.create_text(x, y, text=f"{num}", font=("Arial", 16))

def solve_board(board: list[list[int]], rows: list[set], columns: list[set], 
                cells: list[set]) -> bool:
    """
    Solves the given sudoku board.

    Args:
        board (list[list[int]]): 9x9 matrix containing the sudoku board.
        rows (list[set]): List containing maps of the current numbers in each row.
        columns (list[set]): List containing maps of the current numbers in each column.
        cells (list[set]): List containing maps of the current numbers in each cell.

    Returns:
        bool: Indicates whether the current solution path is correct.
    """
    # Retrieves the index of the next available slot in the board
    index = next_available(board)
    if index == (): # Returns True if no empty slot remains
        return True
    
    row, col = index
    cell = (row // 3) * 3 + (col // 3)
    
    # Attempts to fill in values from 1 to 9
    for num in range(1, 10):
        # Checks if solution given the current number is valid
        if is_safe(rows, columns, cells, num, row, col, cell):
            # Adds new number to current working solution
            board[row][col] = num
            rows[row].add(num)
            columns[col].add(num)
            cells[cell].add(num)
            # Recursively checks if urrent solution holds
            if solve_board(board, rows, columns, cells):
                return True
            # Backtracks if unsuccessful
            board[row][col] = 0
            rows[row].remove(num)
            columns[col].remove(num)
            cells[cell].remove(num)
    
    return False

def initialize_maps(board: list[list[int]]) -> tuple[list[set], list[set], list[set]]:
    """
    Initializes maps containing the numbers on the board contained in each
    row, column and cell.

    Args:
        board (list[list[int]]): 9x9 matrix containing the sudoku board.
    Returns:
        tuple[list[set], list[set], list[set]]: Tuple containing each map.
    """
    # Initializes as lists of sets representing units of each type
    rows = [set() for i in range(9)]
    columns = [set() for i in range(9)]
    cells = [set() for i in range(9)]

    # Sets map values for each number in the initial board
    # Exits program if board is unsolvable
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                num = board[row][col]
                cell = (row // 3) * 3 + (col // 3)

                if num in rows[row]:
                    print("Error: Unsolvable board")
                    exit()
                else:
                    rows[row].add(num)

                if num in columns[col]:
                    print("Error: Unsolvable board")
                    exit()
                else:
                    columns[col].add(num)

                if num in cells[cell]:
                    print("Error: Unsolvable board")
                    exit()
                else: 
                    cells[cell].add(num)                  

    print(f"{rows}\n")
    print(f"{columns}\n")
    print(f"{cells}")

    # Returns maps
    return rows, columns, cells

def is_safe(rows: list[set], columns: list[set], cells: list[set], num: int, 
            row: int, col: int, cell: int) -> bool:
    """
    Checks whether the given number is a valid option for the solution path.

    Args:
        rows (list[set]): List containing maps of the current numbers in each row.
        columns (list[set]): List containing maps of the current numbers in each column.
        cells (list[set]): List containing maps of the current numbers in each cell. 
        num (int): The current number being evaluated.
        row (int): Index of the current row.
        col (int): Index of the current column.
        cell (int): Index of the current cell.
    Returns:
        bool: True if the given number is a valid option. False otherwise.
    """
    # Checks if given number appears in the corresponding row, column and cell.
    if (num not in rows[row] 
        and num not in columns[col] 
        and num not in cells[cell]):
        return True
    
    return False

def next_available(board: list[list[int]]) -> tuple[int]:
    """
    Retrieves the index of the next available slot in the sudoku board.

    Args:
        board (list[list[int]]): 9x9 matrix containing the sudoku board.
    Returns:
        tuple[int]: Tuple containing the coordinates for the index of the next available slot.
    """
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return ()

if __name__ == "__main__":
    main()