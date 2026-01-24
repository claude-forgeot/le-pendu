# tests/test_language_manager.py

"""
Simple tests for the language_manager module.
Run with: python -m tests.test_language_manager
"""

from utils import language_manager
from tests import test_logger


def test_default_language():
    """Check that the default language is French."""
    language = language_manager.get_current_language()

    if language != "fr":
        raise AssertionError(f"expected 'fr', got '{language}'")


def test_set_language_english():
    """Check that we can change the language to English."""
    result = language_manager.set_language("en")

    if result != True:
        raise AssertionError("set_language should return True")

    language_manager.set_language("fr")


def test_set_language_invalid():
    """Check that an invalid language returns False."""
    result = language_manager.set_language("xyz")

    if result != False:
        raise AssertionError("should return False")


def test_get_text_french():
    """Check that we get the correct text in French."""
    language_manager.set_language("fr")
    text = language_manager.get_text("welcome")

    if text != "BIENVENUE AU JEU DU PENDU":
        raise AssertionError("incorrect text")


def test_get_text_english():
    """Check that we get the correct text in English."""
    language_manager.set_language("en")
    text = language_manager.get_text("welcome")

    if text != "WELCOME TO THE HANGMAN GAME":
        raise AssertionError("incorrect text")

    language_manager.set_language("fr")


def test_nonexistent_key():
    """Check that a nonexistent key returns the key itself."""
    text = language_manager.get_text("key_that_does_not_exist")

    if text != "key_that_does_not_exist":
        raise AssertionError("should return the key")


def test_available_languages():
    """Check that French and English are available."""
    languages = language_manager.get_available_languages()

    if "fr" not in languages or "en" not in languages:
        raise AssertionError("fr and en should be available")


def test_locales_data_loaded():
    """Check that the data is loaded."""
    if len(language_manager._locales_data) == 0:
        raise AssertionError("_locales_data is empty")


def run_all_tests():
    """Run all language manager tests."""
    tests = [
        test_default_language,
        test_set_language_english,
        test_set_language_invalid,
        test_get_text_french,
        test_get_text_english,
        test_nonexistent_key,
        test_available_languages,
        test_locales_data_loaded,
    ]

    test_logger.log_header("Language Manager Tests")

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

    test_logger.log_summary("Language Manager Tests", passed, failed)
    return failed == 0


if __name__ == '__main__':
    test_logger.clear()
    run_all_tests()
    test_logger.save()
