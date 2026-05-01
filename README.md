# Ninja vs Pirate Typing Game

A simple Python/Pygame typing game for kids.

## What it does

- Shows a 3-letter word on screen
- Your child types each letter
- Correct letters move the ninja closer to the treasure
- A pirate opponent advances slowly
- When the ninja reaches the treasure, the game shows a win message

## Setup

1. Install Python 3.12+ and make sure `python --version` works.
2. Install Pygame:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

## Files

- `main.py` - the game code
- `words/words.txt` - a simple word list
- `images/` - place `ninja.png`, `pirate.png`, and `treasure.png` here if you want custom sprites

## How to customize

- Add more words to `words/words.txt`
- Replace sprites in `images/`
- Adjust `NINJA_STEP` and `PIRATE_STEP` in `main.py` for movement speed
- Add sound effects inside the game loop
