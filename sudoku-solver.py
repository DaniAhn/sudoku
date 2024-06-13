import numpy as np
import tkinter as tk

DEF_XMIN = 800 # Default minimum x value for window size
DEF_YMIN = 600 # Default minimum y value for window size

CELL_SIZE = 50 # Default size for each cell of the board display

def main():
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
    
    display_board(canvas, sample_puzzle)
    solve_board(sample_puzzle)

    root.mainloop()

def display_board(canvas, board: list) -> None:
    """
    Displays the current sudoku board.

    Args:
        canvas: Canvas object for the board display.
        board (list): 9x9 matrix containing the sudoku board.
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

def solve_board(board: list) -> None:
    """
    Solves the given sudoku board.

    Args:
        board (list): 9x9 matrix containing the sudoku board.
    """
    rows, columns, cells = initialize_maps(board)

def initialize_maps(board):
    """
    Initializes maps containing the amount of times each number
    on the board appears in each row, column and cell.

    Args:
        board (list): 9x9 matrix containing the sudoku board.
    """
    # Initializes as lists of dicts representing units of each type
    rows = [{} for i in range(9)]
    columns = [{} for i in range(9)]
    cells = [{} for i in range(9)]

    # Sets map values for each number in the initial board
    # Exits program if board is unsolvable
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                num = board[row][col]
                cell_index = (row // 3) * 3 + (col // 3)

                if num in rows[row].keys():
                    print("Error: Unsolvable board")
                    exit()
                else:
                    rows[row][num] = 1

                if num in columns[col].keys():
                    print("Error: Unsolvable board")
                    exit()
                else:
                    columns[col][num] = 1

                if num in cells[cell_index].keys():
                    print("Error: Unsolvable board")
                    exit()
                else: 
                    cells[cell_index][num] = 1                    

    print(f"{rows}\n")
    print(f"{columns}\n")
    print(f"{cells}")

    # Returns maps
    return rows, columns, cells

def is_safe(board, rows, columns, cells):
    is_safe = False

if __name__ == "__main__":
    main()