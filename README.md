# Breakthrough - Board Game with AI

A Python implementation of the **Breakthrough** board game featuring a GUI built with Tkinter and an AI opponent powered by the Minimax algorithm with alpha-beta pruning.

## About the Game

Breakthrough is a two-player abstract strategy board game played on an 8×8 board. Each player starts with 16 pawns occupying the first two rows on their side. Pawns can move one square forward (straight or diagonally), and can capture only diagonally. The first player to reach the opponent's back row — or capture all of their pieces — wins.

- **White (O)** — the human player, moves upward
- **Black (X)** — the AI opponent, moves downward

## Project Structure

| File          | Description                                                                   |
| ------------- | ----------------------------------------------------------------------------- |
| `main.py`     | Entry point — launches the GUI                                                |
| `board.py`    | Board representation using bitboards, display logic, and win-condition checks |
| `computer.py` | AI engine — move generation, evaluation function, and Minimax search          |
| `player.py`   | Console-based player input (used for text-mode play)                          |
| `gui.py`      | Tkinter GUI — board rendering, click handling, and game-over screen           |

## How It Works

### Bitboard Representation

The board state is stored as two 64-bit integers (`white_board` and `black_board`), where each bit corresponds to one square on the 8×8 board. This compact representation allows efficient move generation and evaluation using bitwise operations (`AND`, `OR`, `XOR`, shifts).

### AI — Minimax with Alpha-Beta Pruning

The AI uses the **Minimax** algorithm to search the game tree and find the best move. Key optimizations include:

- **Alpha-beta pruning** — cuts off branches that cannot influence the final decision, drastically reducing the number of nodes evaluated.
- **Iterative deepening** — the AI searches at increasing depths (1, 2, 3, …) within a fixed time limit (~3 seconds), ensuring it always has a valid move ready while exploring as deeply as time allows.
- **Transposition table** — a hash map that caches previously evaluated positions to avoid redundant computation. Automatically cleared when it exceeds 1,000,000 entries to manage memory.
- **Move ordering** — moves are sorted by their heuristic score before search, which improves the effectiveness of alpha-beta cutoffs.

### Evaluation Function

The board evaluation considers multiple factors:

| Factor          | Weight        | Description                                             |
| --------------- | ------------- | ------------------------------------------------------- |
| Material        | ×100          | Difference in piece count                               |
| Row advancement | row³          | Pawns closer to the goal are worth exponentially more   |
| Center control  | ×25 / ×10     | Bonus for occupying or surrounding the 4 center squares |
| Pawn chains     | ×10           | Diagonal support between friendly pawns                 |
| Blocked pawns   | ×30 (penalty) | Pawns stacked vertically with no forward path           |

Terminal states (win/loss) return ±100,000 to ensure the AI always prioritizes winning or avoiding defeat.

## How to Run

**Requirements:** Python 3.10+ (uses `int.bit_count()`)

```bash
python main.py
```

### Controls

1. Click a white piece to select it — valid moves are highlighted in green
2. Click a highlighted square to move
3. The AI responds automatically after each move

## Win Conditions

- A pawn reaches the opponent's back row (row 8 for white, row 1 for black)
- All of the opponent's pieces are captured
