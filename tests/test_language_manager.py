# tests/test_language_manager.py

"""
Unit tests for the language_manager module.
Tests are written in a procedural style without classes.
"""

import sys
import os
import tempfile
import shutil
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import language_manager
from tests.test_logger import log_test_error


def assert_equal(actual, expected, test_name):
    """Helper function to assert equality and log errors."""
    if actual != expected:
        error_msg = f"Expected {expected}, got {actual}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_true(value, test_name):
    """Helper function to assert true and log errors."""
    if not value:
        error_msg = f"Expected True, got {value}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_false(value, test_name):
    """Helper function to assert false and log errors."""
    if value:
        error_msg = f"Expected False, got {value}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_in(item, container, test_name):
    """Helper function to assert item is in container and log errors."""
    if item not in container:
        error_msg = f"Expected {item} to be in {container}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_greater_equal(value, threshold, test_name):
    """Helper function to assert value is greater than or equal to threshold."""
    if not (value >= threshold):
        error_msg = f"Expected {value} >= {threshold}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_is_instance(obj, expected_type, test_name):
    """Helper function to assert object is instance of expected type."""
    if not isinstance(obj, expected_type):
        error_msg = f"Expected instance of {expected_type}, got {type(obj)}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def test_initialize_loads_locales():
    """Test that initialize loads locale data."""
    language_manager.initialize()

    assert_is_instance(language_manager._locales_data, dict, "test_initialize_loads_locales")
    assert_true(len(language_manager._locales_data) > 0, "test_initialize_loads_locales")


def test_set_language_french():
    """Test setting language to French."""
    language_manager.initialize()
    result = language_manager.set_language("fr")

    assert_true(result, "test_set_language_french")
    assert_equal(language_manager.get_current_language(), "fr", "test_set_language_french")


def test_set_language_english():
    """Test setting language to English."""
    language_manager.initialize()
    result = language_manager.set_language("en")

    assert_true(result, "test_set_language_english")
    assert_equal(language_manager.get_current_language(), "en", "test_set_language_english")

    language_manager.set_language("fr")


def test_set_language_invalid():
    """Test setting an invalid language."""
    language_manager.initialize()
    original_language = language_manager.get_current_language()
    result = language_manager.set_language("xyz")

    assert_false(result, "test_set_language_invalid")
    assert_equal(language_manager.get_current_language(), original_language, "test_set_language_invalid")


def test_get_current_language_default():
    """Test getting current language returns default."""
    language_manager.initialize()
    language = language_manager.get_current_language()

    assert_equal(language, "fr", "test_get_current_language_default")


def test_get_text_existing_key_french():
    """Test getting text for an existing key in French."""
    language_manager.initialize()
    language_manager.set_language("fr")
    text = language_manager.get_text("welcome")

    assert_equal(text, "BIENVENUE AU JEU DU PENDU", "test_get_text_existing_key_french")


def test_get_text_existing_key_english():
    """Test getting text for an existing key in English."""
    language_manager.initialize()
    language_manager.set_language("en")
    text = language_manager.get_text("welcome")

    assert_equal(text, "WELCOME TO THE HANGMAN GAME", "test_get_text_existing_key_english")

    language_manager.set_language("fr")


def test_get_text_nonexistent_key():
    """Test getting text for a nonexistent key returns the key itself."""
    language_manager.initialize()
    text = language_manager.get_text("nonexistent_key")

    assert_equal(text, "nonexistent_key", "test_get_text_nonexistent_key")


def test_get_text_with_formatting():
    """Test getting text with string formatting."""
    language_manager.initialize()
    language_manager.set_language("fr")
    text = language_manager.get_text("game_start_error", language="fr", difficulty="facile")

    expected = "Impossible de démarrer le jeu. Aucun mot disponible pour 'fr' et difficulté 'facile'."
    assert_equal(text, expected, "test_get_text_with_formatting")


def test_get_text_with_missing_format_args():
    """Test getting text with missing format arguments returns unformatted string."""
    language_manager.initialize()
    language_manager.set_language("fr")
    text = language_manager.get_text("game_start_error", language="fr")

    assert_in("{difficulty}", text, "test_get_text_with_missing_format_args")


def test_get_available_languages_returns_list():
    """Test that get_available_languages returns a list."""
    language_manager.initialize()
    languages = language_manager.get_available_languages()

    assert_is_instance(languages, list, "test_get_available_languages_returns_list")


def test_get_available_languages_contains_french():
    """Test that available languages include French."""
    language_manager.initialize()
    languages = language_manager.get_available_languages()

    assert_in("fr", languages, "test_get_available_languages_contains_french")


def test_get_available_languages_contains_english():
    """Test that available languages include English."""
    language_manager.initialize()
    languages = language_manager.get_available_languages()

    assert_in("en", languages, "test_get_available_languages_contains_english")


def test_load_locales_returns_dict():
    """Test that load_locales returns a dictionary."""
    locales = language_manager.load_locales()

    assert_is_instance(locales, dict, "test_load_locales_returns_dict")


def test_load_locales_contains_languages():
    """Test that loaded locales contain expected languages."""
    locales = language_manager.load_locales()

    assert_in("fr", locales, "test_load_locales_contains_languages")
    assert_in("en", locales, "test_load_locales_contains_languages")


def test_load_locales_missing_file():
    """Test loading locales when file is missing."""
    test_dir = tempfile.mkdtemp()
    original_data_dir = language_manager.DATA_DIR
    original_locales_file = language_manager.LOCALES_FILE

    try:
        language_manager.DATA_DIR = test_dir
        language_manager.LOCALES_FILE = os.path.join(test_dir, "locales.json")

        locales = language_manager.load_locales()
        assert_equal(locales, {}, "test_load_locales_missing_file")

    finally:
        language_manager.DATA_DIR = original_data_dir
        language_manager.LOCALES_FILE = original_locales_file
        language_manager.initialize()
        shutil.rmtree(test_dir)


def test_load_locales_corrupted_json():
    """Test loading locales from corrupted JSON."""
    test_dir = tempfile.mkdtemp()
    original_data_dir = language_manager.DATA_DIR
    original_locales_file = language_manager.LOCALES_FILE

    try:
        language_manager.DATA_DIR = test_dir
        language_manager.LOCALES_FILE = os.path.join(test_dir, "locales.json")

        with open(language_manager.LOCALES_FILE, 'w', encoding='utf-8') as f:
            f.write("{invalid json content")

        locales = language_manager.load_locales()
        assert_equal(locales, {}, "test_load_locales_corrupted_json")

    finally:
        language_manager.DATA_DIR = original_data_dir
        language_manager.LOCALES_FILE = original_locales_file
        language_manager.initialize()
        shutil.rmtree(test_dir)


def test_switch_language_and_get_text():
    """Test switching languages and retrieving text."""
    language_manager.initialize()

    language_manager.set_language("fr")
    fr_text = language_manager.get_text("welcome")

    language_manager.set_language("en")
    en_text = language_manager.get_text("welcome")

    assert_true(fr_text != en_text, "test_switch_language_and_get_text")
    assert_in("BIENVENUE", fr_text, "test_switch_language_and_get_text")
    assert_in("WELCOME", en_text, "test_switch_language_and_get_text")

    language_manager.set_language("fr")


def run_all_tests():
    """Run all language manager tests."""
    tests = [
        test_initialize_loads_locales,
        test_set_language_french,
        test_set_language_english,
        test_set_language_invalid,
        test_get_current_language_default,
        test_get_text_existing_key_french,
        test_get_text_existing_key_english,
        test_get_text_nonexistent_key,
        test_get_text_with_formatting,
        test_get_text_with_missing_format_args,
        test_get_available_languages_returns_list,
        test_get_available_languages_contains_french,
        test_get_available_languages_contains_english,
        test_load_locales_returns_dict,
        test_load_locales_contains_languages,
        test_load_locales_missing_file,
        test_load_locales_corrupted_json,
        test_switch_language_and_get_text,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
            print(f"✓ {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"✗ {test.__name__}: {e}")

    print(f"\nLanguage Manager Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
