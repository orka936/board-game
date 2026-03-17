from board import end_game
import time

RIGHT_BOARD = 0x8080808080808080
LEFT_BOARD = 0x0101010101010101

BLACK_WIN = 0x00000000000000ff
WHITE_WIN = 0xff00000000000000

COLUMNS = 8
ROWS = 8
ROW_MASK = 0xff

MAX_TIME = 3 - 0.2 # za svaki slucaj

# hash mapa za ponovljene pozicije
transposition_table = dict()

def new_bit_position(black_board, new_black_board):
    diff = black_board ^ new_black_board # XOR
    if diff == 0:
        return None
    return (diff & -diff).bit_length() - 1 # diff & -diff izoluje najmanje znacajan bit sa 1

def generate_moves(white_board, black_board, side): # side: True-player, False-computer
    moves = []

    if side: #player
        for i in range((ROWS-1) * COLUMNS):
            if (white_board >> i) & 1:
                if (LEFT_BOARD >> i) & 1 == 0 and (white_board >> (i + 7)) & 1 == 0:
                    new_white_board = (white_board & ~(1 << i)) | (1 << (i + 7))
                    new_black_board = black_board & ~(1 << (i + 7))
                    score = board_evaluation(new_white_board, new_black_board)
                    moves.append((score, new_white_board, new_black_board))
                if (black_board >> (i+8)) & 1 == 0 and (white_board >> (i+8)) & 1 == 0:
                    new_white_board = (white_board & ~(1 << i)) | (1 << (i + 8))
                    new_black_board = black_board
                    score = board_evaluation(new_white_board, new_black_board)
                    moves.append((score, new_white_board, new_black_board))
                if (RIGHT_BOARD >> i) & 1 == 0 and (white_board >> (i + 9)) & 1 == 0:
                    new_white_board = (white_board & ~(1 << i)) | (1 << (i + 9))
                    new_black_board = black_board & ~(1 << (i + 9))
                    score = board_evaluation(new_white_board, new_black_board)
                    moves.append((score, new_white_board, new_black_board))
    else: #computer
        for i in range(ROWS, ROWS * COLUMNS):
            if (black_board >> i) & 1:
                if (LEFT_BOARD >> i) & 1 == 0 and (black_board >> (i - 9)) & 1 == 0:
                    new_black_board = (black_board & ~(1 << i)) | (1 << (i - 9))
                    new_white_board = white_board & ~(1 << (i - 9))
                    score = board_evaluation(new_white_board, new_black_board)
                    moves.append((score, new_white_board, new_black_board))
                if (black_board >> (i-8)) & 1 == 0 and (white_board >> (i-8)) & 1 == 0:
                    new_black_board = (black_board & ~(1 << i)) | (1 << (i - 8))
                    new_white_board = white_board
                    score = board_evaluation(new_white_board, new_black_board)
                    moves.append((score, new_white_board, new_black_board))
                if (RIGHT_BOARD >> i) & 1 == 0 and (black_board >> (i - 7)) & 1 == 0:
                    new_black_board = (black_board & ~(1 << i)) | (1 << (i - 7))
                    new_white_board = white_board & ~(1 << (i - 7))
                    score = board_evaluation(new_white_board, new_black_board)
                    moves.append((score, new_white_board, new_black_board))
    # sortiranje
    if side:  # player (maximizer)
        moves.sort(key=lambda x: x[0], reverse=True)
    else:     # computer (minimizer)
        moves.sort(key=lambda x: x[0])

    return [(w, b) for _, w, b in moves]

def board_evaluation(white_board, black_board):
    score = 0
    
    if black_board & BLACK_WIN or white_board == 0:
        return -100000
    if white_board & WHITE_WIN or black_board == 0:
        return 100000
    
    score += (white_board.bit_count() - black_board.bit_count()) * 100

    for row in range(ROWS):
        row_mask = ROW_MASK << (row * 8)
        white_in_row = (white_board & row_mask).bit_count()
        black_in_row = (black_board & row_mask).bit_count()

        score += white_in_row * ((row) ** 3)
        score -= black_in_row * ((7 - row) ** 3)
    
    # kontrola centra table
    CENTER_MASK = (1 << 27) | (1 << 28) | (1 << 35) | (1 << 36)
    ARROUND_CENTER_MASK = (1 << 18) | (1 << 19) | (1 << 20) | (1 << 21) | (1 << 26) | (1 << 29) | (1 << 34) | (1 << 37) | (1 << 42) | (1 << 43) | (1 << 44) | (1 << 45)

    score += ((white_board & CENTER_MASK).bit_count() - (black_board & CENTER_MASK).bit_count()) * 25
    score += ((white_board & ARROUND_CENTER_MASK).bit_count() - (black_board & ARROUND_CENTER_MASK).bit_count()) * 10

    # blokiranost pijuna i pawn chain
    white_left = (white_board & ~BLACK_WIN) & ~(LEFT_BOARD)
    white_right = (white_board & ~BLACK_WIN) & ~(RIGHT_BOARD)

    score += (white_board & ((white_left << 7) | (white_right << 9))).bit_count() * 10
    score -= (white_board & (white_board << 8)).bit_count() * 30

    black_left = (black_board & ~WHITE_WIN) & ~(RIGHT_BOARD)
    black_right = (black_board & ~WHITE_WIN) & ~(LEFT_BOARD)

    score -= (black_board & ((black_left >> 7) | (black_right >> 9))).bit_count() * 10
    score += (black_board & (black_board >> 8)).bit_count() * 30

    return score

def minimax(white_board, black_board, depth, alpha, beta, maximizing_player, start_time, max_time):
    key = (white_board, black_board, maximizing_player)

    if key in transposition_table:
        entry = transposition_table[key]
        if entry["depth"] >= depth:  # imamo dovoljno duboku analizu
            return entry["score"], entry["best_white"], entry["best_black"]

    if time.time() - start_time >= max_time:
        return board_evaluation(white_board, black_board), white_board, black_board

    if depth == 0 or end_game(white_board, black_board):
        score = board_evaluation(white_board, black_board)
        transposition_table[key] = {"depth": depth, "score": score, "best_white": white_board, "best_black": black_board}
        
        return score, white_board, black_board
    
    if maximizing_player: #player
        max_eval = float('-inf')
        best_white, best_black = white_board, black_board
        for new_white, new_black in generate_moves(white_board, black_board, True):
            eval, _, _ = minimax(new_white, new_black, depth - 1, alpha, beta, False, start_time, max_time)
            if eval > max_eval:
                max_eval = eval
                best_white, best_black = new_white, new_black
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[key] = {"depth": depth, "score": max_eval, "best_white": best_white, "best_black": best_black}
        return max_eval, best_white, best_black
    else: # kompjuter
        min_eval = float('inf')
        best_white, best_black = white_board, black_board
        for new_white, new_black in generate_moves(white_board, black_board, False):
            eval, _, _ = minimax(new_white, new_black, depth - 1, alpha, beta, True, start_time, max_time)
            if eval < min_eval:
                min_eval = eval
                best_white, best_black = new_white, new_black
            beta = min(beta, eval)
            if beta <= alpha:
                break

        transposition_table[key] = {"depth": depth, "score": min_eval, "best_white": best_white, "best_black": best_black}
        return min_eval, best_white, best_black
    

#wrapper / iterative deepening
def computer_move(white_board, black_board, alpha=float('-inf'), beta=float('inf'), maximizing_player=False):
    start = time.time()
    best_white, best_black = white_board, black_board
    depth_reached = 1

    while True:
        _, new_white, new_black = minimax(white_board, black_board, depth_reached, alpha, beta, maximizing_player, start, MAX_TIME)

        if time.time() - start >= MAX_TIME:
            break

        best_white, best_black = new_white, new_black

        depth_reached += 1
    
    #print("Max time " + (str)((time.time() - start) * 100 // 10 / 10) + " reached at depth " + str(depth_reached) + " transpositions: " + str(len(transposition_table)))
    if (len(transposition_table) > 1_000_000):
        transposition_table.clear()
    return best_white, best_black, new_bit_position(black_board, best_black)