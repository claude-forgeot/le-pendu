# Le Pendu (Hangman)

A classic Hangman game built with Pygame, featuring multiple game modes, bilingual support, and a highscore system.

**Academic Project** - Bachelor 1st Year - La Plateforme

## Features

- **4 Game Modes**
  - Easy Mode (7 lives, simple words)
  - Normal Mode (7 lives, medium words)
  - Hard Mode (5 lives, difficult words, video sequences)
  - Infinite Mode (endless gameplay with increasing difficulty)

- **Bilingual Support**
  - French and English interface
  - Separate word dictionaries per language
  - Language switch from main menu

- **Highscore System**
  - Top 10 leaderboard per game mode
  - Persistent score storage
  - 5-character player name input

- **Custom Word Addition**
  - Add your own words to the dictionary
  - Choose difficulty category (easy/medium/hard)

## Screenshots

The game includes custom graphics:
- Animated hangman (head, arms, legs)
- Themed backgrounds per game mode
- Victory and defeat sequences

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/le-pendu.git
cd le-pendu
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the game
```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A-Z | Guess a letter |
| ESC | Pause menu |
| SPACE | Continue (after win/lose) |

## Project Structure

```
le-pendu/
    main.py                 # Entry point
    UI/                     # Pygame views and controllers
    models/                 # Game logic (game_engine.py)
    utils/                  # Utilities (words, localization, scores)
    data/                   # Word lists and translations (TXT format)
    assets/                 # Images, audio (OGG/MP3), video (MP4)
    tests/                  # Unit tests
```

## Running Tests

```bash
python tests/run_all_tests.py
```

Or run individual test files:
```bash
python -m pytest tests/test_game_engine.py
```

## Technologies

- **Pygame-CE** - Graphics, audio, and input handling
- **OpenCV** - Video playback for cinematic sequences
- **Python 3** - Procedural programming style (no OOP)

## Data Format

All game data uses plain TXT files (no JSON):

**Word files** (`data/words_fr.txt`, `data/words_en.txt`):
```
[facile]
word1
word2

[moyen]
word3

[difficile]
word4
```

**Translations** (`data/locales.txt`):
```
[fr]
key=Valeur en francais

[en]
key=English value
```

## License

This project is for educational purposes as part of the Bachelor program at La Plateforme.

## Authors

Bachelor 1st Year Students - La Plateforme, Marseille
