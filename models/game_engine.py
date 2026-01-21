# models/game_engine.py

"""
This file contains the core logic for the Hangman game, implemented in a procedural style.
Instead of a GameEngine class, we use a dictionary to represent the game state
and functions to operate on that state.

This approach adapts the Trello card: "[MODEL] Développement du GameEngine"
for a non-OOP (Object-Oriented Programming) context, as requested.
"""

def create_game(secret_word: str, max_errors: int = 6) -> dict:
    """
    Creates a new game state dictionary.
    This function corresponds to the __init__ method in the Trello card.

    Args:
        secret_word (str): The word to guess.
        max_errors (int): The maximum number of allowed mistakes.

    Returns:
        dict: A dictionary representing the state of a new game.
    """
    game_state = {
        "secret_word": secret_word.upper(),
        "max_errors": max_errors,
        "letters_played": set(),  # Using a set for efficient lookup
        "errors": 0,
        "status": "in_progress"  # Can be 'in_progress', 'won', or 'lost'
    }
    return game_state


def get_masked_word(game_state: dict) -> str:
    """
    Generates the masked word string with spaces for readability (e.g., "H _ N G M _ N").
    This corresponds to the Trello card item: "Méthode get_mot_masque() -> str"

    Args:
        game_state (dict): The current game state dictionary.

    Returns:
        str: The secret word with unguessed letters replaced by underscores.
    """
    masked_word_list = []
    secret_word = game_state["secret_word"]
    letters_played = game_state["letters_played"]
    
    for letter in secret_word:
        if letter in letters_played:
            masked_word_list.append(letter)
        else:
            masked_word_list.append("_")
            
    return " ".join(masked_word_list)

def play_letter(game_state: dict, letter: str) -> bool:
    """
    Processes a player's move. It validates the letter, updates the game state,
    and checks for win/loss conditions.
    This corresponds to "Méthode jouer_lettre(lettre)" from the Trello card.

    Args:
        game_state (dict): The current game state.
        letter (str): The letter played by the user.

    Returns:
        bool: True if the letter was valid and processed, False otherwise.
    """
    letter = letter.upper()

    # Validation: Must be a single alphabetic character and not already played.
    if len(letter) != 1 or not letter.isalpha() or letter in game_state["letters_played"]:
        return False

    game_state["letters_played"].add(letter)

    # If the letter is not in the secret word, increment errors.
    if letter not in game_state["secret_word"]:
        game_state["errors"] += 1

    # Update game status
    if is_won(game_state):
        game_state["status"] = "won"
    elif is_lost(game_state):
        game_state["status"] = "lost"

    return True

def is_won(game_state: dict) -> bool:
    """
    Checks if the game has been won.
    This corresponds to "Méthode est_gagne()" from the Trello card.

    Args:
        game_state (dict): The current game state.

    Returns:
        bool: True if all letters of the secret word have been guessed, False otherwise.
    """
    secret_word_letters = set(game_state["secret_word"])
    return secret_word_letters.issubset(game_state["letters_played"])

def is_lost(game_state: dict) -> bool:
    """
    Checks if the game has been lost.
    This corresponds to "Méthode est_perdu()" from the Trello card.

    Args:
        game_state (dict): The current game state.

    Returns:
        bool: True if the number of errors has reached the maximum allowed, False otherwise.
    """
    return game_state["errors"] >= game_state["max_errors"]

def get_played_letters(game_state: dict) -> list:
    """
    Returns a sorted list of played letters.
    This corresponds to "Méthode get_lettres_jouees()" from the Trello card.

    Args:
        game_state (dict): The current game state.

    Returns:
        list: A sorted list of unique letters that have been played.
    """
    return sorted(list(game_state["letters_played"]))
