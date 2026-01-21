# tests/test_word_manager.py

"""
Unit tests for the word_manager module.
Tests are written in a procedural style without classes.
"""

import sys
import os
import tempfile
import shutil
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import word_manager
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


def assert_in(item, container, test_name):
    """Helper function to assert item is in container and log errors."""
    if item not in container:
        error_msg = f"Expected {item} to be in {container}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_greater(value, threshold, test_name):
    """Helper function to assert value is greater than threshold."""
    if not (value > threshold):
        error_msg = f"Expected {value} > {threshold}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def assert_is_instance(obj, expected_type, test_name):
    """Helper function to assert object is instance of expected type."""
    if not isinstance(obj, expected_type):
        error_msg = f"Expected instance of {expected_type}, got {type(obj)}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)


def test_load_words_french():
    """Test loading French words file."""
    words = word_manager.load_words("fr")

    assert_is_instance(words, dict, "test_load_words_french")
    assert_greater(len(words), 0, "test_load_words_french")
    assert_in("facile", words, "test_load_words_french")


def test_load_words_english():
    """Test loading English words file."""
    words = word_manager.load_words("en")

    assert_is_instance(words, dict, "test_load_words_english")
    assert_greater(len(words), 0, "test_load_words_english")
    assert_in("facile", words, "test_load_words_english")


def test_load_words_nonexistent_language():
    """Test loading words for a nonexistent language."""
    words = word_manager.load_words("xyz")

    assert_equal(words, {}, "test_load_words_nonexistent_language")


def test_load_words_structure():
    """Test that loaded words have the expected structure."""
    words = word_manager.load_words("fr")

    assert_is_instance(words, dict, "test_load_words_structure")
    for difficulty in ["facile", "moyen", "difficile"]:
        if difficulty in words:
            assert_is_instance(words[difficulty], list, "test_load_words_structure")


def test_get_random_word_facile():
    """Test getting a random easy word."""
    test_words = {
        "facile": ["CAT", "DOG", "RAT"],
        "moyen": ["PYTHON"],
        "difficile": ["ALGORITHM"]
    }
    word = word_manager.get_random_word(test_words, "facile")

    assert_in(word, ["CAT", "DOG", "RAT"], "test_get_random_word_facile")


def test_get_random_word_case_insensitive():
    """Test that difficulty parameter is case insensitive."""
    test_words = {"facile": ["CAT", "DOG"]}
    word = word_manager.get_random_word(test_words, "FACILE")

    assert_in(word, ["CAT", "DOG"], "test_get_random_word_case_insensitive")


def test_get_random_word_invalid_difficulty():
    """Test getting word with invalid difficulty."""
    test_words = {"facile": ["CAT"]}
    word = word_manager.get_random_word(test_words, "invalid")

    assert_equal(word, "", "test_get_random_word_invalid_difficulty")


def test_get_random_word_empty_list():
    """Test getting word from empty difficulty list."""
    empty_words = {"facile": []}
    word = word_manager.get_random_word(empty_words, "facile")

    assert_equal(word, "", "test_get_random_word_empty_list")


def test_get_random_word_uppercase():
    """Test that returned word is in uppercase."""
    lowercase_words = {"facile": ["cat", "dog"]}
    word = word_manager.get_random_word(lowercase_words, "facile")

    assert_true(word.isupper(), "test_get_random_word_uppercase")


def test_get_random_word_multiple_calls():
    """Test that multiple calls can return different words."""
    test_words = {"facile": ["A", "B", "C", "D", "E"]}
    words_obtained = set()

    for _ in range(20):
        word = word_manager.get_random_word(test_words, "facile")
        words_obtained.add(word)

    assert_greater(len(words_obtained), 1, "test_get_random_word_multiple_calls")


def test_get_word_french_facile():
    """Test getting a French easy word."""
    word = word_manager.get_word("fr", "facile")

    assert_is_instance(word, str, "test_get_word_french_facile")
    assert_true(word.isupper(), "test_get_word_french_facile")
    assert_greater(len(word), 0, "test_get_word_french_facile")


def test_get_word_invalid_language():
    """Test getting word with invalid language."""
    word = word_manager.get_word("xyz", "facile")

    assert_equal(word, "", "test_get_word_invalid_language")


def test_get_word_invalid_difficulty():
    """Test getting word with invalid difficulty."""
    word = word_manager.get_word("fr", "invalid")

    assert_equal(word, "", "test_get_word_invalid_difficulty")


def test_load_words_corrupted_json():
    """Test loading words from a corrupted JSON file."""
    test_dir = tempfile.mkdtemp()
    original_data_dir = word_manager.DATA_DIR

    try:
        word_manager.DATA_DIR = test_dir
        corrupted_file = os.path.join(test_dir, "words_corrupt.json")

        with open(corrupted_file, 'w', encoding='utf-8') as f:
            f.write("{invalid json content")

        words = word_manager.load_words("corrupt")
        assert_equal(words, {}, "test_load_words_corrupted_json")

    finally:
        word_manager.DATA_DIR = original_data_dir
        shutil.rmtree(test_dir)


def test_load_words_missing_file():
    """Test loading words when file does not exist."""
    test_dir = tempfile.mkdtemp()
    original_data_dir = word_manager.DATA_DIR

    try:
        word_manager.DATA_DIR = test_dir
        words = word_manager.load_words("nonexistent")

        assert_equal(words, {}, "test_load_words_missing_file")

    finally:
        word_manager.DATA_DIR = original_data_dir
        shutil.rmtree(test_dir)


def run_all_tests():
    """Run all word manager tests."""
    tests = [
        test_load_words_french,
        test_load_words_english,
        test_load_words_nonexistent_language,
        test_load_words_structure,
        test_get_random_word_facile,
        test_get_random_word_case_insensitive,
        test_get_random_word_invalid_difficulty,
        test_get_random_word_empty_list,
        test_get_random_word_uppercase,
        test_get_random_word_multiple_calls,
        test_get_word_french_facile,
        test_get_word_invalid_language,
        test_get_word_invalid_difficulty,
        test_load_words_corrupted_json,
        test_load_words_missing_file,
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

    print(f"\nWord Manager Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
