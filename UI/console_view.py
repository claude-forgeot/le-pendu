import os
import sys
from typing import List, Tuple, Optional
from utils import language_manager

# ASCII art for the hangman (index = number of errors)
HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\  |
      / \  |
           |
    =========
    """
]


# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Display main menu to choose language and difficulty
def display_main_menu() -> Optional[Tuple[str, str]]:
    clear_screen()
    print("H H"*15)
    print(f"   {language_manager.get_text('welcome')}")
    print("H H"*15)

    # 1. Language selection
    language = ""
    while language not in ['fr', 'en']:
        choice = input(f"{language_manager.get_text('language_prompt')}: ").lower()
        if choice == 'quit':
            return None
        if choice in ['fr', 'en']:
            language = choice
            language_manager.set_language(language)
        else:
            print(language_manager.get_text('invalid_choice'))

    # 2. Difficulty selection
    difficulty = ""
    while difficulty not in ['facile', 'moyen', 'difficile']:
        choice = input(f"{language_manager.get_text('difficulty_prompt')}: ").lower()
        if choice == 'quit':
            return None
        if choice in ['facile', 'moyen', 'difficile']:
            difficulty = choice
        else:
            print(language_manager.get_text('invalid_choice'))

    return language, difficulty

# Display current game state (hangman, masked word, played letters)
def display_game_state(masked_word: str, played_letters: List[str], errors: int, max_errors: int):
    pic_index = min(errors, len(HANGMAN_PICS) - 1)

    print(HANGMAN_PICS[pic_index])
    print("\n")
    print(f"{language_manager.get_text('word_label')}: {masked_word}")
    print("\n")
    print(f"{language_manager.get_text('errors_label')}: {errors}/{max_errors}")
    print(f"{language_manager.get_text('played_letters_label')}: {', '.join(sorted(played_letters))}")
    print("\n" + "H H "*15 + "\n")

# Prompt player to enter a letter
def get_letter_input() -> str:
    return input(f"{language_manager.get_text('guess_prompt')}: ").upper()


# Display message to the user
def display_message(message: str, is_error: bool = False):
    prefix = "Error: " if is_error else "Info: "
    print(f"{prefix}{message}\n")

# Display winning message
def display_win_message(secret_word: str):
    print("H H "*15)
    print(language_manager.get_text('win_msg'))
    print(f"{language_manager.get_text('secret_word_was')}: {secret_word}")
    print("H H "*15)


# Display losing message
def display_loss_message(secret_word: str):
    print("H H "*15)
    print(language_manager.get_text('lose_msg'))
    print(f"{language_manager.get_text('secret_word_was')}: {secret_word}")
    print("H H "*15)

# Display goodbye message
def display_goodbye_message():
    print(f"\n{language_manager.get_text('goodbye_msg')}\n")