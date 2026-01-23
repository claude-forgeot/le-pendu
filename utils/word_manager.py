# utils/word_manager.py

"""
Word Manager for the Hangman game.
Manages word storage in different formats: TXT for English, JSON for French.
"""

import json
import random
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_words_from_txt(file_path: str) -> Dict[str, List[str]]:
    """
    Load words from a TXT file with section format.
    Format:
        [difficulty_level]
        word1
        word2
        ...
    """
    words_data = {}
    current_difficulty = None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith('[') and line.endswith(']'):
                    current_difficulty = line[1:-1]
                    words_data[current_difficulty] = []
                elif current_difficulty:
                    words_data[current_difficulty].append(line)

        return words_data
    except FileNotFoundError:
        print(f"Error: Word file not found at {file_path}")
        return {}
    except Exception as e:
        print(f"Error loading TXT file {file_path}: {e}")
        return {}


def load_words_from_json(file_path: str) -> Dict[str, List[str]]:
    """Load words from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Word file not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}


def load_words(language: str) -> Dict[str, List[str]]:
    """
    Load words for the given language.
    English words are loaded from TXT, French words from JSON.
    """
    if language == 'en':
        file_path = os.path.join(DATA_DIR, 'words_en.txt')
        return load_words_from_txt(file_path)
    elif language == 'fr':
        file_path = os.path.join(DATA_DIR, 'words_fr.json')
        return load_words_from_json(file_path)
    else:
        print(f"Error: Unsupported language '{language}'")
        return {}


def get_random_word(words_data: Dict[str, List[str]], difficulty: str) -> str:
    """Select random word from words_data based on difficulty level."""
    difficulty_key = difficulty.lower()
    if difficulty_key not in words_data or not words_data[difficulty_key]:
        return ""

    word = random.choice(words_data[difficulty_key])
    return word.upper()


def get_word(language: str, difficulty: str) -> str:
    """Get random word for given language and difficulty."""
    words_data = load_words(language)
    if not words_data:
        return ""
    return get_random_word(words_data, difficulty)


def add_word_to_txt(file_path: str, word: str, difficulty: str) -> bool:
    """
    Add a word to a TXT file under the specified difficulty section.
    Returns True if successful, False otherwise.
    """
    try:
        words_data = load_words_from_txt(file_path)

        difficulty_key = difficulty.lower()
        if difficulty_key not in words_data:
            words_data[difficulty_key] = []

        word_lower = word.lower()

        # Check if word already exists
        word_exists = False
        for w in words_data[difficulty_key]:
            if w.lower() == word_lower:
                word_exists = True
                break

        if word_exists:
            print(f"Word '{word}' already exists in {difficulty} difficulty")
            return False

        words_data[difficulty_key].append(word_lower)

        with open(file_path, 'w', encoding='utf-8') as f:
            for diff_level in ['facile', 'moyen', 'difficile']:
                if diff_level in words_data and words_data[diff_level]:
                    f.write(f"[{diff_level}]\n")
                    for w in words_data[diff_level]:
                        f.write(f"{w}\n")
                    f.write("\n")

        return True
    except Exception as e:
        print(f"Error adding word to TXT file: {e}")
        return False


def add_word_to_json(file_path: str, word: str, difficulty: str) -> bool:
    """
    Add a word to a JSON file under the specified difficulty section.
    Returns True if successful, False otherwise.
    """
    try:
        words_data = load_words_from_json(file_path)

        difficulty_key = difficulty.lower()
        if difficulty_key not in words_data:
            words_data[difficulty_key] = []

        word_lower = word.lower()

        # Check if word already exists
        word_exists = False
        for w in words_data[difficulty_key]:
            if w.lower() == word_lower:
                word_exists = True
                break

        if word_exists:
            print(f"Word '{word}' already exists in {difficulty} difficulty")
            return False

        words_data[difficulty_key].append(word_lower)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(words_data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Error adding word to JSON file: {e}")
        return False


def add_word(language: str, word: str, difficulty: str) -> bool:
    """
    Add a word to the appropriate file based on language.
    English words go to TXT, French words go to JSON.
    Returns True if successful, False otherwise.
    """
    if not word or not word.strip():
        print("Error: Word cannot be empty")
        return False

    if difficulty.lower() not in ['facile', 'moyen', 'difficile']:
        print(f"Error: Invalid difficulty '{difficulty}'. Must be 'facile', 'moyen', or 'difficile'")
        return False

    word = word.strip()

    if language == 'en':
        file_path = os.path.join(DATA_DIR, 'words_en.txt')
        success = add_word_to_txt(file_path, word, difficulty)
    elif language == 'fr':
        file_path = os.path.join(DATA_DIR, 'words_fr.json')
        success = add_word_to_json(file_path, word, difficulty)
    else:
        print(f"Error: Unsupported language '{language}'")
        return False

    if success:
        print(f"Word '{word}' added successfully to {language} words ({difficulty})")

    return success
