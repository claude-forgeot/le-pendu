# tests/test_word_manager.py

"""
Tests for the word_manager module.
Run with: python -m tests.test_word_manager
"""

from utils import word_manager
from tests import test_logger


def test_load_words_french():
    """Test loading French words file."""
    words = word_manager.load_words("fr")

    if type(words) != dict or len(words) == 0:
        raise AssertionError("words should be a non-empty dict")


def test_load_words_english():
    """Test loading English words file."""
    words = word_manager.load_words("en")

    if type(words) != dict or len(words) == 0:
        raise AssertionError("words should be a non-empty dict")


def test_load_words_has_difficulties():
    """Test that loaded words have all difficulty levels."""
    words = word_manager.load_words("fr")

    if "facile" not in words or "moyen" not in words or "difficile" not in words:
        raise AssertionError("missing difficulty levels")


def test_load_words_invalid_language():
    """Test loading words for a nonexistent language."""
    words = word_manager.load_words("xyz")

    if words != {}:
        raise AssertionError("should return empty dict")


def test_get_random_word_facile():
    """Test getting a random easy word."""
    test_words = {
        "facile": ["CAT", "DOG", "RAT"],
        "moyen": ["PYTHON"],
        "difficile": ["ALGORITHM"]
    }
    word = word_manager.get_random_word(test_words, "facile")

    if word not in ["CAT", "DOG", "RAT"]:
        raise AssertionError("word not in expected list")


def test_get_random_word_invalid_difficulty():
    """Test getting word with invalid difficulty."""
    test_words = {"facile": ["CAT"]}
    word = word_manager.get_random_word(test_words, "invalid")

    if word != "":
        raise AssertionError("should return empty string")


def test_get_random_word_uppercase():
    """Test that returned word is in uppercase."""
    lowercase_words = {"facile": ["cat", "dog"]}
    word = word_manager.get_random_word(lowercase_words, "facile")

    if not word.isupper():
        raise AssertionError("word should be uppercase")


def test_get_word_french_facile():
    """Test getting a French easy word."""
    word = word_manager.get_word("fr", "facile")

    if type(word) != str or len(word) == 0 or not word.isupper():
        raise AssertionError("invalid word returned")


def test_get_word_invalid_language():
    """Test getting word with invalid language."""
    word = word_manager.get_word("xyz", "facile")

    if word != "":
        raise AssertionError("should return empty string")


def test_get_word_invalid_difficulty():
    """Test getting word with invalid difficulty."""
    word = word_manager.get_word("fr", "invalid")

    if word != "":
        raise AssertionError("should return empty string")


def test_load_words_from_txt():
    """Test that English words are loaded from TXT format."""
    words = word_manager.load_words("en")

    if "facile" not in words or len(words["facile"]) == 0:
        raise AssertionError("TXT loading failed")


def test_load_words_french_txt():
    """Test that French words are loaded from TXT format."""
    words = word_manager.load_words("fr")

    if "facile" not in words or len(words["facile"]) == 0:
        raise AssertionError("TXT loading failed")


def test_add_word_validation():
    """Test add_word input validation."""
    result1 = word_manager.add_word("fr", "", "facile")
    result2 = word_manager.add_word("fr", "test", "invalid_difficulty")
    result3 = word_manager.add_word("xyz", "test", "facile")

    if result1 or result2 or result3:
        raise AssertionError("should reject invalid inputs")


def run_all_tests():
    """Run all word manager tests."""
    tests = [
        test_load_words_french,
        test_load_words_english,
        test_load_words_has_difficulties,
        test_load_words_invalid_language,
        test_get_random_word_facile,
        test_get_random_word_invalid_difficulty,
        test_get_random_word_uppercase,
        test_get_word_french_facile,
        test_get_word_invalid_language,
        test_get_word_invalid_difficulty,
        test_load_words_from_txt,
        test_load_words_french_txt,
        test_add_word_validation,
    ]

    test_logger.log_header("Word Manager Tests")

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
            test_logger.log_result(test.__name__, True)
        except AssertionError as e:
            failed += 1
            test_logger.log_result(test.__name__, False, str(e))

    test_logger.log_summary("Word Manager Tests", passed, failed)
    return failed == 0


if __name__ == '__main__':
    test_logger.clear()
    run_all_tests()
    test_logger.save()
