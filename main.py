import sys
from board import  print_board, end_game, white_board, black_board
from player import player_move
from computer import computer_move, board_evaluation # u slucaju da treba da se ispisje score
from gui import BreaktroughGUI
import tkinter as tk

VELICINA = 8
POLJE = 60

def main_gui():
    root = tk.Tk()
    gui = BreaktroughGUI(root)
    gui.run()
        

if __name__ == "__main__":
    main_gui()