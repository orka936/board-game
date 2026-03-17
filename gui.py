import sys
import tkinter as tk
from computer import computer_move
from board import white_board, black_board, end_game

# --- podešavanja ---
sirina = 600
visina = 600

VELICINA = 8
POLJE = 75

class BreaktroughGUI:

    def __init__(self, root, turn = True):
        self.root = root
        self.root.title("Breakthrough")

        # fiksna veličina (ne može resize)
        self.root.resizable(False, False)

        # dobijanje širine i visine ekrana
        ekran_sirina = self.root.winfo_screenwidth()
        ekran_visina = self.root.winfo_screenheight()

        # računanje pozicije za centriranje
        pozicija_x = (ekran_sirina // 2) - (sirina // 2)
        pozicija_y = (ekran_visina // 2) - (visina // 2)

        # postavljanje geometrije prozora: širina x visina + X + Y
        self.root.geometry(f"{sirina}x{visina}+{pozicija_x}+{pozicija_y}")

        # tabla igre
        self.canvas = tk.Canvas(self.root, width=sirina, height=visina, bg="white")
        self.canvas.pack()

        self.turn = turn  # True za igrača, False za kompjuter

        self.canvas.bind("<Button-1>", self.klik)

        global white_board, black_board
        self.white_board = white_board
        self.black_board = black_board

        self.bit = None
        self.potezi = []
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(8):
            for j in range(8):
                boja = "white" if (i+j) % 2 == 0 else "gray"
                boja = "green" if not self.bit == None and self.bit == (i*8 + j) else boja
                boja = "light green" if not self.potezi == [] and (i*8 + j) in self.potezi else boja 
                x1, y1 = j*POLJE, visina - (i*POLJE)
                x2, y2 = (j+1)*POLJE, visina - ((i+1)*POLJE)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=boja)

                if (self.black_board >> (i*8 + j)) & 1:
                    self.canvas.create_oval(x1+5, y1-5, x2-5, y2+5, fill="black", outline="black")
                elif (self.white_board >> (i*8 + j)) & 1:
                    self.canvas.create_oval(x1+5, y1-5, x2-5, y2+5, fill="white", outline="black")

    
    def computer_move(self):
        if self.end_game():
            print("Game over!")
            return
        
        self.turn = False
        self.white_board, self.black_board, self.bit = computer_move(self.white_board, self.black_board)
        self.draw_board()
        if self.end_game():
            return
        self.draw_board()
        self.root.update_idletasks()
        self.root.update()
        self.turn = True
        return

    def klik(self, event):
        if self.end_game():
            print("Game over!")
            return
        
        if not self.turn:
            return  # nije red igrača
        red = 7 - (event.y // POLJE)
        kolona = event.x // POLJE

        if red < 0 or red > 7 or kolona < 0 or kolona > 7:
            return

        bit = red * 8 + kolona

        if bit in self.potezi:
            nova_pozicija = bit
            self.white_board &= ~(1 << self.bit)
            self.white_board |= (1 << nova_pozicija)
            self.black_board &= ~(1 << nova_pozicija)
            self.potezi = []
            self.bit = nova_pozicija
            self.draw_board()
            if self.end_game():
                return
            
            self.draw_board()
            self.root.update_idletasks()
            self.root.update()

            self.turn = False
            self.computer_move()

            return

        if (self.white_board >> bit) & 1 == 0:
            return
        
        self.potezi = []
        # proveri mogucnosti pomeranja
        if bit + 7 < 64 and not bit % 8 == 0 and (self.white_board >> (bit + 7)) & 1 == 0:
            self.potezi.append(bit + 7)
        if bit + 8 < 64 and (self.black_board >> (bit + 8)) & 1 == 0 and (self.white_board >> (bit + 8)) & 1 == 0:
            self.potezi.append(bit + 8)
        if bit + 9 < 64 and not (bit+1) % 8 == 0 and (self.white_board >> (bit + 9)) & 1 == 0:
            self.potezi.append(bit + 9)
        
        if self.potezi == []:
            return

        self.bit = bit
        self.draw_board()

    def end_game(self):
        if self.white_board & 0xff00000000000000 or self.black_board == 0:
            self.show_game_over("Pobedio si!")
            return True
        elif self.black_board & 0x00000000000000ff or self.white_board == 0:
            self.show_game_over("Izgubio si!")
            return True
        else:
            return False

    def show_game_over(self, poruka):
        # nacrtaj poluprovidan pravougaonik preko cele table
        self.canvas.create_rectangle(
            0, 0, sirina, visina,
            fill="black", stipple="gray50", outline=""
        )

        # tekst na sredini
        self.canvas.create_text(
            sirina // 2, visina // 2,
            text=poruka,
            fill="white",
            font=("Helvetica", 32, "bold")
        )


    def run(self):
        self.root.mainloop()
        