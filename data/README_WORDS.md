# Word Storage System

This document explains how words are stored and managed in the Hangman game.

## Storage Formats

The game uses two different storage formats depending on the language:

### English Words (TXT Format)

File: `words_en.txt`

Format:
```
[facile]
cat
sun
cup

[moyen]
guitar
window
computer

[difficile]
xylophone
rhododendron
```

**Characteristics:**
- Plain text file
- Sections defined by brackets: `[difficulty]`
- One word per line
- Three difficulty levels: facile, moyen, difficile

### French Words (JSON Format)

File: `words_fr.json`

Format:
```json
{
  "facile": ["chat", "pain", "porte"],
  "moyen": ["guitare", "fenetre", "ballon"],
  "difficile": ["xylophone", "rhododendron"]
}
```

**Characteristics:**
- JSON structure
- Dictionary with difficulty levels as keys
- Arrays of words as values
- Three difficulty levels: facile, moyen, difficile

## Adding Words

### Using Python Code

```python
from utils import word_manager

# Add an English word (stored in TXT)
word_manager.add_word('en', 'python', 'moyen')

# Add a French word (stored in JSON)
word_manager.add_word('fr', 'ordinateur', 'facile')
```

### Using Interactive Script

Run the interactive script:
```bash
python3 add_word_interactive.py
```

This script will guide you through adding words step by step.

### Manual Editing

You can also edit the files directly:

**English (TXT):**
1. Open `data/words_en.txt`
2. Navigate to the desired difficulty section
3. Add your word on a new line

**French (JSON):**
1. Open `data/words_fr.json`
2. Find the difficulty level
3. Add your word to the array (don't forget the comma)

## Difficulty Levels

- **facile** (easy): Short, common words (3-5 letters)
- **moyen** (medium): Medium-length words (6-10 letters)
- **difficile** (hard): Long or complex words (10+ letters)

## API Reference

### `load_words(language: str) -> Dict[str, List[str]]`
Load all words for a given language.

**Parameters:**
- `language`: 'en' for English, 'fr' for French

**Returns:**
- Dictionary with difficulty levels as keys and word lists as values

### `get_word(language: str, difficulty: str) -> str`
Get a random word for a specific language and difficulty.

**Parameters:**
- `language`: 'en' for English, 'fr' for French
- `difficulty`: 'facile', 'moyen', or 'difficile'

**Returns:**
- Random word in UPPERCASE, or empty string if not found

### `add_word(language: str, word: str, difficulty: str) -> bool`
Add a word to the appropriate storage file.

**Parameters:**
- `language`: 'en' for English, 'fr' for French
- `word`: The word to add (will be converted to lowercase)
- `difficulty`: 'facile', 'moyen', or 'difficile'

**Returns:**
- `True` if successful, `False` otherwise

**Notes:**
- Duplicates are automatically detected and rejected
- Words are stored in lowercase
- Input validation is performed on all parameters
