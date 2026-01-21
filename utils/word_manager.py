# utils/word_manager.py

"""
This file is responsible for loading words from data files and providing
a random word based on language and difficulty.

It adapts the Trello card: "📚 [DATA] Gestionnaire de Mots" for a procedural style.
"""

import json
import random
import os
from typing import Dict, List

# The path to the directory where the word files are stored.
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_words(language: str) -> Dict[str, List[str]]:
    """
    Loads a word file based on the selected language.

    Args:
        language (str): The language code (e.g., 'fr', 'en').

    Returns:
        Dict[str, List[str]]: A dictionary containing words categorized by difficulty.
                               Returns an empty dictionary if the file is not found.
    """
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

def get_random_word(words_data: Dict[str, List[str]], difficulty: str) -> str:
    """
    Selects a random word from the provided data based on difficulty.

    Args:
        words_data (Dict[str, List[str]]): The dictionary of words.
        difficulty (str): The chosen difficulty ('facile', 'moyen', 'difficile').

    Returns:
        str: A random word in uppercase. Returns an empty string if the difficulty
             or word list is not available.
    """
    difficulty_key = difficulty.lower()
    if difficulty_key not in words_data or not words_data[difficulty_key]:
        return ""
        
    word = random.choice(words_data[difficulty_key])
    return word.upper()

def get_word(language: str, difficulty: str) -> str:
    """
    A helper function that combines loading words and getting a random one.

    Args:
        language (str): The language code ('fr' or 'en').
        difficulty (str): The difficulty level ('facile', 'moyen', 'difficile').

    Returns:
        str: A random word, or an empty string if unsuccessful.
    """
    words_data = load_words(language)
    if not words_data:
        return ""
    return get_random_word(words_data, difficulty)
