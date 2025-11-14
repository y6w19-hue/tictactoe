
"""
tic_tac_toe.py
Simple Tic-Tac-Toe game with Tkinter GUI.
Two-player or play vs simple CPU (random / blocking heuristic).
"""

import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe (Keele assignment)")
        self.current_player = "X"
        self.board = [None] * 9  # 3x3 flattened
        self.buttons = []
        self.vs_cpu = tk.BooleanVar(value=False)

        top = tk.Frame(root)
        top.pack(pady=6)
        tk.Checkbutton(top, text="Play vs CPU", variable=self.vs_cpu).pack(side="left", padx=8)
        tk.Button(top, text="New Game", command=self.reset_board).pack(side="left", padx=8)

        frame = tk.Frame(root)
        frame.pack()
        for i in range(9):
            b = tk.Button(frame, text="", font=("Helvetica", 28), width=4, height=2,
                          command=lambda i=i: self.on_click(i))
            b.grid(row=i//3, column=i%3)
            self.buttons.append(b)

        self.status = tk.Label(root, text="X starts", font=("Helvetica", 12))
        self.status.pack(pady=6)

    def on_click(self, index):
        if self.board[index] is not None:
            return
        self.make_move(index, self.current_player)
        winner = self.check_winner()
        if winner:
            self.end_game(winner)
            return

        if self.vs_cpu.get() and self.current_player == "O":
            # CPU already played; shouldn't happen in this flow
            return

        # swap player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status.config(text=f"{self.current_player}'s turn")

        if self.vs_cpu.get() and self.current_player == "O":
            self.root.after(300, self.cpu_move)  # small delay for UX

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state="disabled")
    
    def cpu_move(self):
        # Simple CPU: try win, block, else random
        move = self.find_winning_move("O")
        if move is None:
            move = self.find_winning_move("X")  # block player's win
        if move is None:
            empties = [i for i, v in enumerate(self.board) if v is None]
            if not empties:
                return
            move = random.choice(empties)
        self.make_move(move, "O")
        winner = self.check_winner()
        if winner:
            self.end_game(winner)
            return
        self.current_player = "X"
        self.status.config(text="X's turn")

    def find_winning_move(self, player):
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in lines:
            vals = [self.board[a], self.board[b], self.board[c]]
            if vals.count(player) == 2 and vals.count(None) == 1:
                # return empty index
                for i in (a,b,c):
                    if self.board[i] is None:
                        return i
        return None

    def check_winner(self):
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]  # 'X' or 'O'
        if all(v is not None for v in self.board):
            return "Draw"
        return None

    def end_game(self, winner):
        msg = "It's a draw!" if winner == "Draw" else f"{winner} wins!"
        messagebox.showinfo("Game Over", msg)
        # disable buttons
        for b in self.buttons:
            b.config(state="disabled")
        self.status.config(text=msg)

    def reset_board(self):
        self.board = [None]*9
        for b in self.buttons:
            b.config(text="", state="normal")
        self.current_player = "X"
        self.status.config(text="X starts")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
