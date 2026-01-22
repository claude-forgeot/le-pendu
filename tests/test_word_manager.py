# tests/test_word_manager.py

"""
Tests for the word_manager module.
Run with: python -m tests.test_word_manager
"""

from utils import word_manager


def test_load_words_french():
    """Test loading French words file."""
    words = word_manager.load_words("fr")

    if type(words) == dict and len(words) > 0:
        print("OK - test_load_words_french")
    else:
        print("ERROR - test_load_words_french: words should be a non-empty dict")


def test_load_words_english():
    """Test loading English words file."""
    words = word_manager.load_words("en")

    if type(words) == dict and len(words) > 0:
        print("OK - test_load_words_english")
    else:
        print("ERROR - test_load_words_english: words should be a non-empty dict")


def test_load_words_has_difficulties():
    """Test that loaded words have all difficulty levels."""
    words = word_manager.load_words("fr")

    if "facile" in words and "moyen" in words and "difficile" in words:
        print("OK - test_load_words_has_difficulties")
    else:
        print("ERROR - test_load_words_has_difficulties: missing difficulty levels")


def test_load_words_invalid_language():
    """Test loading words for a nonexistent language."""
    words = word_manager.load_words("xyz")

    if words == {}:
        print("OK - test_load_words_invalid_language")
    else:
        print("ERROR - test_load_words_invalid_language: should return empty dict")


def test_get_random_word_facile():
    """Test getting a random easy word."""
    test_words = {
        "facile": ["CAT", "DOG", "RAT"],
        "moyen": ["PYTHON"],
        "difficile": ["ALGORITHM"]
    }
    word = word_manager.get_random_word(test_words, "facile")

    if word in ["CAT", "DOG", "RAT"]:
        print("OK - test_get_random_word_facile")
    else:
        print("ERROR - test_get_random_word_facile: word not in expected list")


def test_get_random_word_invalid_difficulty():
    """Test getting word with invalid difficulty."""
    test_words = {"facile": ["CAT"]}
    word = word_manager.get_random_word(test_words, "invalid")

    if word == "":
        print("OK - test_get_random_word_invalid_difficulty")
    else:
        print("ERROR - test_get_random_word_invalid_difficulty: should return empty string")


def test_get_random_word_uppercase():
    """Test that returned word is in uppercase."""
    lowercase_words = {"facile": ["cat", "dog"]}
    word = word_manager.get_random_word(lowercase_words, "facile")

    if word.isupper():
        print("OK - test_get_random_word_uppercase")
    else:
        print("ERROR - test_get_random_word_uppercase: word should be uppercase")


def test_get_word_french_facile():
    """Test getting a French easy word."""
    word = word_manager.get_word("fr", "facile")

    if type(word) == str and len(word) > 0 and word.isupper():
        print("OK - test_get_word_french_facile")
    else:
        print("ERROR - test_get_word_french_facile: invalid word returned")


def test_get_word_invalid_language():
    """Test getting word with invalid language."""
    word = word_manager.get_word("xyz", "facile")

    if word == "":
        print("OK - test_get_word_invalid_language")
    else:
        print("ERROR - test_get_word_invalid_language: should return empty string")


def test_get_word_invalid_difficulty():
    """Test getting word with invalid difficulty."""
    word = word_manager.get_word("fr", "invalid")

    if word == "":
        print("OK - test_get_word_invalid_difficulty")
    else:
        print("ERROR - test_get_word_invalid_difficulty: should return empty string")


# Run all tests
print("Word Manager Tests")
print("")

test_load_words_french()
test_load_words_english()
test_load_words_has_difficulties()
test_load_words_invalid_language()
test_get_random_word_facile()
test_get_random_word_invalid_difficulty()
test_get_random_word_uppercase()
test_get_word_french_facile()
test_get_word_invalid_language()
test_get_word_invalid_difficulty()

print("")
print("Tests finished")
