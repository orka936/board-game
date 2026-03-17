from board import ROW_MAP, KOLONA_MAP

def get_position_input():
    while True:
        try:
            pos = input("Unesite polje figure koju želite da pomerite (npr. A1): ").strip().upper()
            if len(pos) != 2:
                raise ValueError("Unos mora biti u formatu A1, B2, ... H8 (2 karaktera)")
            if pos[0] not in KOLONA_MAP.keys() or not pos[1].isdigit() or int(pos[1]) < 1 or int(pos[1]) > 8:
                raise ValueError("Neispravan unos. Molimo unesite polje u formatu A1, B2, ... H8 (prvo slovo a zatim i broj)")
            row = ROW_MAP[int(pos[1])]
            col = KOLONA_MAP[pos[0]]
            bit = row * 8 + col

            #print("bit " + str(bit) + " kolona " + str(col) + " red " + str(row))
            return bit
        except ValueError as e:
            print(e)

def player_move(white_board, black_board):
    opcije = {1: None, 2: None, 3: None}
    print("Tvoj potez:")
    while True:
        try:
            bit = get_position_input()
            if (white_board >> bit) & 1:
                if bit + 7 < 64 and not bit % 8 == 0 and (white_board >> (bit + 7)) & 1 == 0:
                    print("1 - Pomeranje figure levo")
                    opcije[1] = bit + 7
                if bit + 8 < 64 and (black_board >> (bit + 8)) & 1 == 0 and (white_board >> (bit + 8)) & 1 == 0:
                    print("2 - Pomeranje figure pravo")
                    opcije[2] = bit + 8
                if bit + 9 < 64 and not (bit+1) % 8 == 0 and (white_board >> (bit + 9)) & 1 == 0:
                    print("3 - Pomeranje figure desno")
                    opcije[3] = bit + 9
                
                if not any(opcije.values()):
                    print("Nema mogućih poteza za ovu figuru. Pokušaj ponovo.")
                    continue
                while True:
                    try:
                        izbor = int(input("Unesite broj opcije za pomeranje figure (1, 2, 3): "))
                        if opcije.get(izbor) is not None:
                            nova_pozicija = opcije[izbor]
                            white_board &= ~(1 << bit)
                            white_board |= (1 << nova_pozicija)
                            black_board &= ~(1 << nova_pozicija)
                            return white_board, black_board, nova_pozicija
                        else:
                            print("Nevažeća opcija. Pokušaj ponovo.")
                    except ValueError:
                        print("Molimo unesite broj opcije.")
                
            else:
                print("Na tom polju nema tvoje figure. Pokušaj ponovo.")
        except Exception as e:
            print(f"Greška: {e}")