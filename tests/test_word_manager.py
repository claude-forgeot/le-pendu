# Tests for word_manager module: load_words, get_word, add_word

from utils import word_manager
from tests import test_logger


# Verify French words load as non-empty dict
def test_load_words_french():
    words = word_manager.load_words("fr")

    if type(words) != dict or len(words) == 0:
        raise AssertionError("words should be a non-empty dict")


# Verify English words load as non-empty dict
def test_load_words_english():
    words = word_manager.load_words("en")

    if type(words) != dict or len(words) == 0:
        raise AssertionError("words should be a non-empty dict")


# Verify all three difficulty keys exist in loaded words
def test_load_words_has_difficulties():
    words = word_manager.load_words("fr")

    if "facile" not in words or "moyen" not in words or "difficile" not in words:
        raise AssertionError("missing difficulty levels")


# Verify invalid language returns empty dict
def test_load_words_invalid_language():
    words = word_manager.load_words("xyz")

    if words != {}:
        raise AssertionError("should return empty dict")


# Verify get_random_word returns word from correct difficulty
def test_get_random_word_facile():
    test_words = {
        "facile": ["CAT", "DOG", "RAT"],
        "moyen": ["PYTHON"],
        "difficile": ["ALGORITHM"]
    }
    word = word_manager.get_random_word(test_words, "facile")

    if word not in ["CAT", "DOG", "RAT"]:
        raise AssertionError("word not in expected list")


# Verify invalid difficulty returns empty string
def test_get_random_word_invalid_difficulty():
    test_words = {"facile": ["CAT"]}
    word = word_manager.get_random_word(test_words, "invalid")

    if word != "":
        raise AssertionError("should return empty string")


# Verify returned word is converted to uppercase
def test_get_random_word_uppercase():
    lowercase_words = {"facile": ["cat", "dog"]}
    word = word_manager.get_random_word(lowercase_words, "facile")

    if not word.isupper():
        raise AssertionError("word should be uppercase")


# Verify get_word returns valid uppercase French word
def test_get_word_french_facile():
    word = word_manager.get_word("fr", "facile")

    if type(word) != str or len(word) == 0 or not word.isupper():
        raise AssertionError("invalid word returned")


# Verify get_word with invalid language returns empty
def test_get_word_invalid_language():
    word = word_manager.get_word("xyz", "facile")

    if word != "":
        raise AssertionError("should return empty string")


# Verify get_word with invalid difficulty returns empty
def test_get_word_invalid_difficulty():
    word = word_manager.get_word("fr", "invalid")

    if word != "":
        raise AssertionError("should return empty string")


# Verify English TXT file loads with words in facile
def test_load_words_from_txt():
    words = word_manager.load_words("en")

    if "facile" not in words or len(words["facile"]) == 0:
        raise AssertionError("TXT loading failed")


# Verify French TXT file loads with words in facile
def test_load_words_french_txt():
    words = word_manager.load_words("fr")

    if "facile" not in words or len(words["facile"]) == 0:
        raise AssertionError("TXT loading failed")


# Verify add_word rejects empty word, invalid difficulty, invalid lang
def test_add_word_validation():
    result1 = word_manager.add_word("fr", "", "facile")
    result2 = word_manager.add_word("fr", "test", "invalid_difficulty")
    result3 = word_manager.add_word("xyz", "test", "facile")

    if result1 or result2 or result3:
        raise AssertionError("should reject invalid inputs")


# Execute all tests and log pass/fail summary
def run_all_tests():
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
