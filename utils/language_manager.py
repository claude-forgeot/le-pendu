# utils/language_manager.py

"""
Language Manager for the Hangman game.
Allows changing the active language and retrieving translated texts.
"""

import json
import os

# Path to the translations file
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOCALES_FILE = os.path.join(DATA_DIR, 'locales.json')

# Global variables
_locales_data = {}
_current_language = "fr"


def load_locales():
    """Load translations from locales.json."""
    file = open(LOCALES_FILE, 'r', encoding='utf-8')
    data = json.load(file)
    file.close()
    return data


def initialize():
    """Load translations at startup."""
    global _locales_data
    _locales_data = load_locales()


def set_language(language_code):
    """Change the active language. Returns True if OK, False otherwise."""
    global _current_language

    if language_code in _locales_data:
        _current_language = language_code
        return True
    else:
        return False


def get_current_language():
    """Return the active language (e.g. 'fr')."""
    return _current_language


def get_text(key):
    """Return the translated text for the given key."""
    global _locales_data, _current_language

    translations = _locales_data[_current_language]

    if key in translations:
        return translations[key]
    else:
        return key


def get_available_languages():
    """Return the list of available languages."""
    return list(_locales_data.keys())


# Load translations at startup
initialize()
