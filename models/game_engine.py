# Create a new game state dictionary
def create_game(secret_word: str, max_errors: int = 7) -> dict:
    game_state = {
        "secret_word": secret_word.upper(),
        "max_errors": max_errors,
        "letters_played": set(),  # Using a set for efficient lookup
        "errors": 0,
        "status": "in_progress"  # Can be 'in_progress', 'won', or 'lost'
    }
    return game_state


# Generate masked word with unguessed letters replaced by underscores
def get_masked_word(game_state: dict) -> str:
    masked_word_list = []
    secret_word = game_state["secret_word"]
    letters_played = game_state["letters_played"]
    
    for letter in secret_word:
        if letter in letters_played:
            masked_word_list.append(letter)
        else:
            masked_word_list.append("_")
            
    return " ".join(masked_word_list)

# Process a player's move and update game state
def play_letter(game_state: dict, letter: str) -> bool:
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

# Check if all letters of the secret word have been guessed
def is_won(game_state: dict) -> bool:
    secret_word_letters = set(game_state["secret_word"])
    return secret_word_letters.issubset(game_state["letters_played"])

# Check if the number of errors has reached the maximum allowed
def is_lost(game_state: dict) -> bool:
    return game_state["errors"] >= game_state["max_errors"]

# Return a sorted list of played letters
def get_played_letters(game_state: dict) -> list:
    return sorted(list(game_state["letters_played"]))
