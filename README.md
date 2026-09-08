# sip_chess

Hand-gesture controlled chess. Point your index finger, hold it steady over a
piece to select it, hold again over a destination square to move it.

## Setup

Requires Python 3.11 (mediapipe/pygame do not yet support 3.13+).

```bash
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Put your piece images in a `pieces/` folder next to `main.py`, named like
`wp.png`, `bq.png`, etc. (white/black + piece letter).

## Run

```bash
python main.py
```

Press `H` to toggle the hand landmark overlay.

## Project structure

```
main.py              entry point, game loop only
config.py             all tunable constants in one place
core/
  hand_tracker.py      wraps mediapipe, returns clean landmark lists
  gesture.py           dwell-to-click detection (hold-still-to-select logic)
game/
  state.py             GameState class - board, selection, move history (no globals)
ui/
  board_view.py         drawing the board/pieces, pixel <-> square conversion
  home_screen.py         start screen
  popups.py              game-over screen
```

This is the base for further extension: AI opponent, richer gestures
(pinch/drag), pawn promotion, move history panel, etc.
