import json
import random
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load words from JSON file for given language
def load_words(language: str) -> Dict[str, List[str]]:
    file_path = os.path.join(DATA_DIR, f'words_{language}.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Word file not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}

# Select random word from words_data based on difficulty level
def get_random_word(words_data: Dict[str, List[str]], difficulty: str) -> str:
    difficulty_key = difficulty.lower()
    if difficulty_key not in words_data or not words_data[difficulty_key]:
        return ""

    word = random.choice(words_data[difficulty_key])
    return word.upper()

# Get random word for given language and difficulty
def get_word(language: str, difficulty: str) -> str:
    words_data = load_words(language)
    if not words_data:
        return ""
    return get_random_word(words_data, difficulty)
