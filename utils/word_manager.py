# Word loading and storage from TXT files with difficulty sections

import random
import os

# Path to data/ folder (from utils/ go up one level with '..' then into 'data')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


# Parse TXT file into dict with difficulty keys and word lists
def load_words_from_txt(file_path):
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


# Load word dictionary for specified language (fr or en)
def load_words(language):
    if language == 'en':
        file_path = os.path.join(DATA_DIR, 'words_en.txt')
    elif language == 'fr':
        file_path = os.path.join(DATA_DIR, 'words_fr.txt')
    else:
        print(f"Error: Unsupported language '{language}'")
        return {}

    return load_words_from_txt(file_path)


# Select random uppercase word from specified difficulty level
def get_random_word(words_data, difficulty):
    difficulty_key = difficulty.lower()
    if difficulty_key not in words_data or not words_data[difficulty_key]:
        return ""

    word = random.choice(words_data[difficulty_key])
    return word.upper()


# Fetch random word for specified language and difficulty
def get_word(language, difficulty):
    words_data = load_words(language)
    if not words_data:
        return ""
    return get_random_word(words_data, difficulty)


# Append word to TXT file under specified difficulty section, returns success bool
def add_word_to_txt(file_path, word, difficulty):
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


# Add validated word to language-specific TXT file, returns success bool
def add_word(language, word, difficulty):
    if not word or not word.strip():
        print("Error: Word cannot be empty")
        return False

    if difficulty.lower() not in ['facile', 'moyen', 'difficile']:
        print(f"Error: Invalid difficulty '{difficulty}'. Must be 'facile', 'moyen', or 'difficile'")
        return False

    word = word.strip()

    if language == 'en':
        file_path = os.path.join(DATA_DIR, 'words_en.txt')
    elif language == 'fr':
        file_path = os.path.join(DATA_DIR, 'words_fr.txt')
    else:
        print(f"Error: Unsupported language '{language}'")
        return False

    success = add_word_to_txt(file_path, word, difficulty)

    if success:
        print(f"Word '{word}' added successfully to {language} words ({difficulty})")

    return success
