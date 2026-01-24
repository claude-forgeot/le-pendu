# Tests for language_manager module: get/set language, get_text

from utils import language_manager
from tests import test_logger


# Verify default language is French
def test_default_language():
    language = language_manager.get_current_language()

    if language != "fr":
        raise AssertionError(f"expected 'fr', got '{language}'")


# Verify set_language to English succeeds
def test_set_language_english():
    result = language_manager.set_language("en")

    if result != True:
        raise AssertionError("set_language should return True")

    language_manager.set_language("fr")


# Verify set_language with invalid code returns False
def test_set_language_invalid():
    result = language_manager.set_language("xyz")

    if result != False:
        raise AssertionError("should return False")


# Verify get_text returns correct French translation
def test_get_text_french():
    language_manager.set_language("fr")
    text = language_manager.get_text("welcome")

    if text != "BIENVENUE AU JEU DU PENDU":
        raise AssertionError("incorrect text")


# Verify get_text returns correct English translation
def test_get_text_english():
    language_manager.set_language("en")
    text = language_manager.get_text("welcome")

    if text != "WELCOME TO THE HANGMAN GAME":
        raise AssertionError("incorrect text")

    language_manager.set_language("fr")


# Verify missing key returns the key string as fallback
def test_nonexistent_key():
    text = language_manager.get_text("key_that_does_not_exist")

    if text != "key_that_does_not_exist":
        raise AssertionError("should return the key")


# Verify both fr and en are in available languages
def test_available_languages():
    languages = language_manager.get_available_languages()

    if "fr" not in languages or "en" not in languages:
        raise AssertionError("fr and en should be available")


# Verify _locales_data is populated from locales.txt
def test_locales_data_loaded():
    if len(language_manager._locales_data) == 0:
        raise AssertionError("_locales_data is empty")


# Execute all tests and log pass/fail summary
def run_all_tests():
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
