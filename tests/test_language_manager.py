# tests/test_language_manager.py

"""
Simple tests for the language_manager module.
Run with: python -m tests.test_language_manager
"""

from utils import language_manager


def test_default_language():
    """Check that the default language is French."""
    language = language_manager.get_current_language()

    if language == "fr":
        print("OK - test_default_language")
    else:
        print("ERROR - test_default_language: expected 'fr', got '" + language + "'")


def test_set_language_english():
    """Check that we can change the language to English."""
    result = language_manager.set_language("en")

    if result == True:
        print("OK - test_set_language_english")
    else:
        print("ERROR - test_set_language_english: set_language should return True")

    language_manager.set_language("fr")


def test_set_language_invalid():
    """Check that an invalid language returns False."""
    result = language_manager.set_language("xyz")

    if result == False:
        print("OK - test_set_language_invalid")
    else:
        print("ERROR - test_set_language_invalid: should return False")


def test_get_text_french():
    """Check that we get the correct text in French."""
    language_manager.set_language("fr")
    text = language_manager.get_text("welcome")

    if text == "BIENVENUE AU JEU DU PENDU":
        print("OK - test_get_text_french")
    else:
        print("ERROR - test_get_text_french: incorrect text")


def test_get_text_english():
    """Check that we get the correct text in English."""
    language_manager.set_language("en")
    text = language_manager.get_text("welcome")

    if text == "WELCOME TO THE HANGMAN GAME":
        print("OK - test_get_text_english")
    else:
        print("ERROR - test_get_text_english: incorrect text")

    language_manager.set_language("fr")


def test_nonexistent_key():
    """Check that a nonexistent key returns the key itself."""
    text = language_manager.get_text("key_that_does_not_exist")

    if text == "key_that_does_not_exist":
        print("OK - test_nonexistent_key")
    else:
        print("ERROR - test_nonexistent_key: should return the key")


def test_available_languages():
    """Check that French and English are available."""
    languages = language_manager.get_available_languages()

    if "fr" in languages and "en" in languages:
        print("OK - test_available_languages")
    else:
        print("ERROR - test_available_languages: fr and en should be available")


def test_locales_data_loaded():
    """Check that the data is loaded."""
    if len(language_manager._locales_data) > 0:
        print("OK - test_locales_data_loaded")
    else:
        print("ERROR - test_locales_data_loaded: _locales_data is empty")


# Run all tests
print("Language Manager Tests")
print("")

test_default_language()
test_set_language_english()
test_set_language_invalid()
test_get_text_french()
test_get_text_english()
test_nonexistent_key()
test_available_languages()
test_locales_data_loaded()

print("")
print("Tests finished")
