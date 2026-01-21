# controllers/game_controller.py

"""
This file orchestrates the game flow by connecting the game logic (model)
with the user interface (view).

It implements the procedural equivalent of the "🎮 [CONTROLLER] Développement du Contrôleur"
Trello card.
"""

# Import the functions from the model, view, and utility modules
from models import game_engine
from UI import console_view
from utils import word_manager

def start_game():
    """
    Initializes and runs the main game loop.
    """
    # Show the main menu and get user's choices
    game_settings = console_view.display_main_menu()

    # If the user chose to quit from the menu
    if game_settings is None:
        console_view.display_goodbye_message()
        return

    language, difficulty = game_settings

    # Get a word from our word manager based on user's choice
    secret_word = word_manager.get_word(language, difficulty)

    # Handle case where no word could be loaded
    if not secret_word:
        print(f"Could not start the game. No words available for '{language}' and '{difficulty}' difficulty.")
        return

    max_errors = len(console_view.HANGMAN_PICS) - 1

    # 1. Create a new game state
    game_state = game_engine.create_game(secret_word, max_errors)

    # 2. Main game loop
    while game_state["status"] == "in_progress":
        # a. Clear the screen for a fresh display
        console_view.clear_screen()

        # b. Display the current game state (hangman, masked word, etc.)
        masked_word = game_engine.get_masked_word(game_state)
        played_letters = game_engine.get_played_letters(game_state)
        errors = game_state["errors"]
        
        console_view.display_game_state(masked_word, played_letters, errors, max_errors)

        # c. Get player input
        letter = console_view.get_letter_input()

        # d. Process the letter
        # We check if the letter was already played to provide specific feedback
        if letter in game_state["letters_played"]:
            console_view.display_message("You have already played this letter. Try another one.", is_error=True)
            input("Press Enter to continue...") # Pause to let the user read the message
            continue # Skip the rest of the loop and start over

        # The play_letter function handles the core logic
        was_processed = game_engine.play_letter(game_state, letter)
        
        # If the input was invalid (e.g., not a single letter), inform the user.
        if not was_processed:
            console_view.display_message("Invalid input. Please enter a single letter.", is_error=True)
            input("Press Enter to continue...") # Pause for user
            continue

    # 3. After the loop, display the final result
    console_view.clear_screen()
    if game_engine.is_won(game_state):
        console_view.display_win_message(secret_word)
    else:
        console_view.display_loss_message(secret_word)
