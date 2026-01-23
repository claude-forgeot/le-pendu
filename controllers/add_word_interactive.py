#!/usr/bin/env python3

"""
Interactive script to add words to the game.
Run with: python3 -m controllers.add_word_interactive
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import word_manager

def main():
    print("HANGMAN GAME - ADD WORD")
    print("")

    while True:
        print("Choose language:")
        print("1. English (stored in TXT)")
        print("2. French (stored in TXT)")
        print("3. Quit")
        print("")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "3":
            print("Goodbye!")
            break

        if choice == "1":
            language = "en"
            language_name = "English"
        elif choice == "2":
            language = "fr"
            language_name = "French"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            print("")
            continue

        print("")
        print(f"Adding {language_name} word")
        print("")

        word = input("Enter word: ").strip()

        if not word:
            print("Word cannot be empty.")
            print("")
            continue

        print("")
        print("Choose difficulty:")
        print("1. Facile (easy)")
        print("2. Moyen (medium)")
        print("3. Difficile (hard)")
        print("")

        diff_choice = input("Enter difficulty (1-3): ").strip()

        if diff_choice == "1":
            difficulty = "facile"
        elif diff_choice == "2":
            difficulty = "moyen"
        elif diff_choice == "3":
            difficulty = "difficile"
        else:
            print("Invalid difficulty. Skipping.")
            print("")
            continue

        print("")
        success = word_manager.add_word(language, word, difficulty)

        if success:
            print(f"Word '{word}' added successfully!")
        else:
            print(f"Failed to add word '{word}'.")

        print("")
        print("")

if __name__ == "__main__":
    main()
