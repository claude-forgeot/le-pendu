# views/console_view.py

"""
This file provides all the functions necessary to display the Hangman game
in a command-line interface (CLI).

It adapts the Trello card: "[VIEW] Vue Console (CLI)" for a procedural style.
"""

import os
import sys
from typing import List, Tuple, Optional
from utils import language_manager

# ASCII art for the hangman, corresponding to the number of errors.
# The index represents the number of errors (0 errors = index 0, 1 error = index 1, etc.).
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


def clear_screen():
    """
    Clears the console screen.
    This corresponds to the Trello card item: "Clear screen entre chaque tour".
    """
    # 'nt' is for Windows, 'posix' is for macOS and Linux.
    os.system('cls' if os.name == 'nt' else 'clear')


def display_main_menu() -> Optional[Tuple[str, str]]:
    """
    Displays the main menu to choose language and difficulty.
    Corresponds to the Trello card: "[FEATURE] Menu Principal".

    Returns:
        Optional[Tuple[str, str]]: A tuple containing the chosen (language, difficulty),
                                   or None if the user chooses to quit.
    """
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

def display_game_state(masked_word: str, played_letters: List[str], errors: int, max_errors: int):
    """
    Displays the current state of the game: the hangman drawing, the masked word,
    and the letters that have already been played.

    This combines several items from the Trello card:
    - "Méthode display_word(masked_word, guessed_letters)"
    - "Méthode display_hangman(errors)"
    - "Affichage des lettres jouées"

    Args:
        masked_word (str): The word with unguessed letters hidden (e.g., "H _ N G M _ N").
        played_letters (List[str]): The list of letters already proposed by the player.
        errors (int): The current number of incorrect guesses.
        max_errors (int): The maximum number of allowed errors.
    """
    # Ensure errors do not exceed the number of available pictures.
    pic_index = min(errors, len(HANGMAN_PICS) - 1)

    print(HANGMAN_PICS[pic_index])
    print("\n")
    print(f"{language_manager.get_text('word_label')}: {masked_word}")
    print("\n")
    print(f"{language_manager.get_text('errors_label')}: {errors}/{max_errors}")
    # Display played letters in a sorted, readable format.
    print(f"{language_manager.get_text('played_letters_label')}: {', '.join(sorted(played_letters))}")
    print("\n" + "H H "*15 + "\n")

def get_letter_input() -> str:
    """
    Prompts the player to enter a letter and returns their input.
    This corresponds to the Trello card item: "Méthode get_input() -> str".

    Returns:
        str: The letter entered by the user, converted to uppercase.
    """
    return input(f"{language_manager.get_text('guess_prompt')}: ").upper()


def display_message(message: str, is_error: bool = False):
    """
    Displays a message to the user, such as a win/loss message or an error.
    This corresponds to the Trello card item: "Méthode show_message(msg, type)".

    Args:
        message (str): The message to be displayed.
        is_error (bool): If True, the message is presented as an error.
    """
    prefix = "Error: " if is_error else "Info: "
    print(f"{prefix}{message}\n")

def display_win_message(secret_word: str):
    """
    Displays the winning message, including the secret word.
    """
    print("H H "*15)
    print(language_manager.get_text('win_msg'))
    print(f"{language_manager.get_text('secret_word_was')}: {secret_word}")
    print("H H "*15)


def display_loss_message(secret_word: str):
    """
    Displays the losing message, revealing the secret word.
    """
    print("H H "*15)
    print(language_manager.get_text('lose_msg'))
    print(f"{language_manager.get_text('secret_word_was')}: {secret_word}")
    print("H H "*15)

def display_goodbye_message():
    """
    Displays a goodbye message when the user quits.
    """
    print(f"\n{language_manager.get_text('goodbye_msg')}\n")