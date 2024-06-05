import numpy as np
import tkinter as tk

DEF_XMIN = 800
DEF_YMIN = 600

CELL_SIZE = 50

def main():
    board = np.zeros((9, 9))

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

    root = tk.Tk()

    root.title("Sudoku Solver")

    canvas = tk.Canvas(root, width=9*CELL_SIZE, height=9*CELL_SIZE, 
                       borderwidth=0, highlightthickness=0)
    canvas.pack()

    root.geometry(f"{DEF_XMIN}x{DEF_YMIN}")
    root.minsize(DEF_XMIN, DEF_YMIN)
    
    display_board(canvas, sample_puzzle)

    root.mainloop()

def display_board(canvas, board: list):
    for i in range(len(board) + 1):
        width = 1 if i % 3 != 0 else 2

        canvas.create_line(0, i * CELL_SIZE, 9 * CELL_SIZE, i * CELL_SIZE,
                           fill="black", width=width)
        canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, 9 * CELL_SIZE, 
                           fill="black", width=width)
        
    for row in range(len(board)):
        for col in range(len(board[row])):
            num = board[row][col]
            if num != 0:
                x = col * CELL_SIZE + CELL_SIZE / 2
                y = row * CELL_SIZE + CELL_SIZE / 2
                canvas.create_text(x, y, text=f"{num}")

if __name__ == "__main__":
    main()