import numpy as np
import tkinter as tk
import tkinter.simpledialog as simpledialog
import random

DEF_XMIN = 800 # Default minimum x value for window size
DEF_YMIN = 600 # Default minimum y value for window size

CELL_SIZE = 50 # Default size for each cell of the board display

def main()-> None:
    """
    Main entry point of the program.
    """
    board = random_puzzle()

    # Creates the root window
    root = tk.Tk()
    root.title("Sudoku Solver")

    # Creates canvas object to display sudoku board
    canvas = tk.Canvas(root, width=9*CELL_SIZE, height=9*CELL_SIZE, 
                       borderwidth=0, highlightthickness=0)
    canvas.pack(pady=10)
    display_board(canvas, board)

    # Initializes maps containing the numbers in the initial board
    rows, columns, cells = initialize_maps(board)

    def on_click()-> None:
        """
        Calls the solve_board function when the button is clicked.
        """
        if solve_board(board, rows, columns, cells):
            display_board(canvas, board)
        else:
            exit()

    def input_number(event: tk.Event)-> None:
        """
        Handles player input on the sudoku board.

        Args:
            event (tk.Event): Represents a click event. 
        """
        # Calculates position of the click on the sudoku board.
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        cell = (row // 3) * 3 + (col // 3)
        
        # Checks if space is empty.
        if board[row][col] == 0: 
            # Opens a dialogue box to input an integer from 1-9.
            user_input = tk.simpledialog.askinteger("Input", "Enter a number (1-9):")
            
            # Checks if user input is a valid move.
            if user_input and 1 <= user_input <= 9 and is_safe(rows, columns, cells, user_input, row, col, cell): 
                # Adds input number to the current board.
                board[row][col] = user_input
                rows[row].add(user_input)
                columns[col].add(user_input)
                cells[cell].add(user_input)
                display_board(canvas, board)
            else:
                tk.messagebox.showerror("Error", "Invalid move.")

    # Bind click event to canvas
    canvas.bind("<Button-1>", input_number)

    # Creates clickable button to solve the sudoku puzzle.
    button = tk.Button(root, text="Solve puzzle!", command=on_click, font=("Georgia", 16), width=12, height=1)
    button.pack()

    # Configures root window size
    root.geometry(f"{DEF_XMIN}x{DEF_YMIN}")
    root.minsize(DEF_XMIN, DEF_YMIN)

    root.mainloop()

def random_puzzle()-> np.array:
    """
    Returns a random sudoku puzzle picked from a list of sample puzzles.

    Returns:
        np.array: Array representing a sudoku puzzle.
    """
    sample_puzzles = [
        np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]),
        np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]),
        np.array([
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ]),
        np.array([
            [0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 0, 3, 0, 0, 0, 0, 4, 5],
            [0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 8, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 7, 0, 0]
        ]),
        np.array([
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 6, 0],
            [0, 0, 0, 0, 0, 0, 0, 9, 0],
            [5, 0, 0, 0, 0, 0, 6, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 7, 0, 0, 0, 0, 0, 0]
        ]),
        np.array([
            [0, 0, 0, 2, 0, 0, 0, 6, 3],
            [3, 0, 0, 0, 0, 5, 4, 0, 1],
            [0, 0, 1, 0, 0, 3, 9, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 9, 0],
            [0, 0, 0, 5, 3, 8, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 6, 3, 0, 0, 5, 0, 0],
            [5, 0, 3, 7, 0, 0, 0, 0, 8],
            [4, 7, 0, 0, 0, 1, 0, 0, 0]
        ])
    ]
    return sample_puzzles[random.randint(0, len(sample_puzzles))]

def display_board(canvas: tk.Canvas, board: np.ndarray)-> None:
    """
    Displays the current sudoku board.

    Args:
        canvas (tk.Canvas): Canvas object for the board display.
        board (np.ndarray): 9x9 matrix containing the sudoku board.
    """
    # Clears canvas
    canvas.delete("all")
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
                canvas.create_text(x, y, text=f"{int(num)}", font=("Georgia", 16))

def solve_board(board: np.ndarray, rows: list[set], columns: list[set], 
                cells: list[set]) -> bool:
    """
    Solves the given sudoku board.

    Args:
        board (np.ndarray): 9x9 matrix containing the sudoku board.
        rows (list[set[int]]): List containing maps of the current numbers in each row.
        columns (list[set[int]]): List containing maps of the current numbers in each column.
        cells (list[set[int]]): List containing maps of the current numbers in each cell.

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

def initialize_maps(board: np.ndarray)-> tuple[list[set[int]]]:
    """
    Initializes maps containing the numbers on the board contained in each
    row, column and cell.

    Args:
        board (np.ndarray): 9x9 matrix containing the sudoku board.
    Returns:
        tuple[list[set[int]]]: Tuple containing each map.
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

    # Returns maps
    return rows, columns, cells

def is_safe(rows: list[set], columns: list[set], cells: list[set], num: int, 
            row: int, col: int, cell: int) -> bool:
    """
    Checks whether the given number is a valid option for the solution path.

    Args:
        rows (list[set[int]]): List containing maps of the current numbers in each row.
        columns (list[set[int]]): List containing maps of the current numbers in each column.
        cells (list[set[int]]): List containing maps of the current numbers in each cell. 
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

def next_available(board: np.ndarray) -> tuple[int]:
    """
    Retrieves the index of the next available slot in the sudoku board.

    Args:
        board (np.ndarray): 9x9 matrix containing the sudoku board.
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