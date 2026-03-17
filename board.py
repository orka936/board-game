white_board = 0x000000000000ffff
black_board = 0xffff000000000000

KOLONA_MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
ROW_MAP = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7}

WHITE_WIN = 0xff00000000000000
BLACK_WIN = 0x00000000000000ff

def print_board(white_board, black_board, bit=None):
    print("      " + '     '.join(KOLONA_MAP.keys()))  
    print('   ' + '-' * (8 * 5 + 9))
    for i in range(7, -1, -1):
        row = []
        for j in range(8):
            if (black_board >> (i*8 + j)) & 1:
                if bit is not None and bit == (i*8 + j):
                    row.append('- X -')
                else:
                    row.append('  X  ')
            elif (white_board >> (i*8 + j)) & 1:
                if bit is not None and bit == (i*8 + j):
                    row.append('- O -')
                else:
                    row.append('  O  ')
            else:
                row.append('     ')
        print(str(i+1) + '  |' + '|'.join(row) + '|')
        print('   ' + '-' * (8 * 5 + 9))

def end_game(white_board, black_board):
    if white_board & WHITE_WIN:
        return True
    elif black_board & BLACK_WIN:
        return True
    elif white_board == 0 or black_board == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    print_board(white_board, black_board)