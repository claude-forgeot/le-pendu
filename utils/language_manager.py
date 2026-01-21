# utils/language_manager.py

"""
This file manages internationalization (i18n) for the Hangman game.
It loads translations from locales.json and provides functions to get text
in the current language.

It implements the Trello card: "🌍 [I18N] Système Multilingue" for a procedural style.
"""

import json
import os
from typing import Dict, Any

# Path to the locales file
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOCALES_FILE = os.path.join(DATA_DIR, 'locales.json')

# Global state to store locales data and current language
_locales_data: Dict[str, Dict[str, str]] = {}
_current_language: str = "fr"  # Default language

def load_locales() -> Dict[str, Dict[str, str]]:
    """
    Loads all translations from the locales.json file.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary containing all translations
                                    for all supported languages.
                                    Returns an empty dictionary if the file
                                    is not found or cannot be decoded.
    """
    try:
        with open(LOCALES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Locales file not found at {LOCALES_FILE}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {LOCALES_FILE}")
        return {}

def initialize():
    """
    Initializes the language manager by loading the locales file.
    This should be called once at the start of the application.
    """
    global _locales_data
    _locales_data = load_locales()
    if not _locales_data:
        print("Warning: No locales data loaded. Using default texts.")

def set_language(language_code: str) -> bool:
    """
    Sets the current language for the application.

    Args:
        language_code (str): The language code to set ('fr', 'en', etc.)

    Returns:
        bool: True if the language was set successfully, False otherwise.
    """
    global _current_language

    if not _locales_data:
        initialize()

    if language_code in _locales_data:
        _current_language = language_code
        return True
    else:
        print(f"Warning: Language '{language_code}' not found. Keeping '{_current_language}'.")
        return False

def get_current_language() -> str:
    """
    Returns the current language code.

    Returns:
        str: The current language code (e.g., 'fr', 'en')
    """
    return _current_language

def get_text(key: str, **kwargs) -> str:
    """
    Gets a translated text for the given key in the current language.
    Supports string formatting with keyword arguments.

    Args:
        key (str): The translation key to look up.
        **kwargs: Optional keyword arguments for string formatting.

    Returns:
        str: The translated and formatted text. If the key is not found,
             returns the key itself as a fallback.

    Example:
        get_text("welcome")
        get_text("game_start_error", language="fr", difficulty="facile")
    """
    global _locales_data, _current_language

    # Ensure locales are loaded
    if not _locales_data:
        initialize()

    # Get the text for the current language
    if _current_language in _locales_data:
        text = _locales_data[_current_language].get(key, key)
    else:
        text = key

    # Apply formatting if kwargs are provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text

    return text

def get_available_languages() -> list:
    """
    Returns a list of available language codes.

    Returns:
        list: A list of language codes (e.g., ['fr', 'en'])
    """
    if not _locales_data:
        initialize()
    return list(_locales_data.keys())

# Initialize locales on module import
initialize()
