# Unit tests for game_engine module: create_game, play_letter, is_won, is_lost

from models import game_engine
from tests import test_logger


# Raise AssertionError if actual != expected
def assert_equal(actual, expected, test_name):
    if actual != expected:
        raise AssertionError(f"Expected {expected}, got {actual}")


# Raise AssertionError if value is not True
def assert_true(value, test_name):
    if not value:
        raise AssertionError(f"Expected True, got {value}")


# Raise AssertionError if value is not False
def assert_false(value, test_name):
    if value:
        raise AssertionError(f"Expected False, got {value}")


# Raise AssertionError if item not in container
def assert_in(item, container, test_name):
    if item not in container:
        raise AssertionError(f"Expected {item} to be in {container}")


# Verify create_game returns correct initial state with defaults
def test_create_game_basic():
    game_state = game_engine.create_game("PYTHON")

    assert_equal(game_state["secret_word"], "PYTHON", "test_create_game_basic")
    assert_equal(game_state["max_errors"], 7, "test_create_game_basic")
    assert_equal(game_state["errors"], 0, "test_create_game_basic")
    assert_equal(game_state["status"], "in_progress", "test_create_game_basic")
    assert_equal(len(game_state["letters_played"]), 0, "test_create_game_basic")


# Verify create_game respects custom max_errors parameter
def test_create_game_custom_max_errors():
    game_state = game_engine.create_game("HANGMAN", max_errors=10)

    assert_equal(game_state["secret_word"], "HANGMAN", "test_create_game_custom_max_errors")
    assert_equal(game_state["max_errors"], 10, "test_create_game_custom_max_errors")


# Verify lowercase input is converted to uppercase
def test_create_game_lowercase_word():
    game_state = game_engine.create_game("python")

    assert_equal(game_state["secret_word"], "PYTHON", "test_create_game_lowercase_word")


# Verify masked word shows all underscores initially
def test_masked_word_no_letters_played():
    game_state = game_engine.create_game("PYTHON")
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "_ _ _ _ _ _", "test_masked_word_no_letters_played")


# Verify masked word reveals guessed letters correctly
def test_masked_word_partial_guess():
    game_state = game_engine.create_game("PYTHON")
    game_state["letters_played"].add("P")
    game_state["letters_played"].add("O")
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "P _ _ _ O _", "test_masked_word_partial_guess")


# Verify masked word shows full word when all letters guessed
def test_masked_word_all_letters_guessed():
    game_state = game_engine.create_game("PYTHON")
    for letter in "PYTHON":
        game_state["letters_played"].add(letter)
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "P Y T H O N", "test_masked_word_all_letters_guessed")


# Verify duplicate letters are all revealed at once
def test_masked_word_repeated_letters():
    game_state = game_engine.create_game("HELLO")
    game_state["letters_played"].add("L")
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "_ _ L L _", "test_masked_word_repeated_letters")


# Verify correct letter is added without incrementing errors
def test_play_valid_correct_letter():
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "P")

    assert_true(result, "test_play_valid_correct_letter")
    assert_in("P", game_state["letters_played"], "test_play_valid_correct_letter")
    assert_equal(game_state["errors"], 0, "test_play_valid_correct_letter")


# Verify wrong letter is added and error count increases
def test_play_valid_incorrect_letter():
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "Z")

    assert_true(result, "test_play_valid_incorrect_letter")
    assert_in("Z", game_state["letters_played"], "test_play_valid_incorrect_letter")
    assert_equal(game_state["errors"], 1, "test_play_valid_incorrect_letter")


# Verify lowercase letter is converted to uppercase in play
def test_play_lowercase_letter():
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "p")

    assert_true(result, "test_play_lowercase_letter")
    assert_in("P", game_state["letters_played"], "test_play_lowercase_letter")


# Verify duplicate letter play returns False
def test_play_already_played_letter():
    game_state = game_engine.create_game("PYTHON")
    game_engine.play_letter(game_state, "P")
    result = game_engine.play_letter(game_state, "P")

    assert_false(result, "test_play_already_played_letter")


# Verify multi-char input is rejected
def test_play_invalid_multiple_letters():
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "PY")

    assert_false(result, "test_play_invalid_multiple_letters")


# Verify numeric input is rejected
def test_play_invalid_number():
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "5")

    assert_false(result, "test_play_invalid_number")


# Verify empty string input is rejected
def test_play_invalid_empty_string():
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "")

    assert_false(result, "test_play_invalid_empty_string")


# Verify is_won returns True when all letters found
def test_is_won_all_letters_guessed():
    game_state = game_engine.create_game("CAT")
    for letter in "CAT":
        game_state["letters_played"].add(letter)

    assert_true(game_engine.is_won(game_state), "test_is_won_all_letters_guessed")


# Verify is_won returns False with incomplete word
def test_is_won_some_letters_missing():
    game_state = game_engine.create_game("PYTHON")
    game_state["letters_played"].add("P")
    game_state["letters_played"].add("Y")

    assert_false(game_engine.is_won(game_state), "test_is_won_some_letters_missing")


# Verify is_won returns True even with extra wrong letters
def test_is_won_extra_letters():
    game_state = game_engine.create_game("CAT")
    for letter in "CATZYX":
        game_state["letters_played"].add(letter)

    assert_true(game_engine.is_won(game_state), "test_is_won_extra_letters")


# Verify is_lost returns True at max errors
def test_is_lost_max_errors_reached():
    game_state = game_engine.create_game("PYTHON", max_errors=3)
    game_state["errors"] = 3

    assert_true(game_engine.is_lost(game_state), "test_is_lost_max_errors_reached")


# Verify is_lost returns False below max errors
def test_is_lost_errors_below_max():
    game_state = game_engine.create_game("PYTHON", max_errors=6)
    game_state["errors"] = 3

    assert_false(game_engine.is_lost(game_state), "test_is_lost_errors_below_max")


# Verify get_played_letters returns empty list initially
def test_get_played_letters_empty():
    game_state = game_engine.create_game("PYTHON")
    letters = game_engine.get_played_letters(game_state)

    assert_equal(letters, [], "test_get_played_letters_empty")


# Verify get_played_letters returns alphabetically sorted list
def test_get_played_letters_sorted():
    game_state = game_engine.create_game("PYTHON")
    for letter in "ZAP":
        game_state["letters_played"].add(letter)
    letters = game_engine.get_played_letters(game_state)

    assert_equal(letters, ["A", "P", "Z"], "test_get_played_letters_sorted")


# Verify full win scenario with status change to won
def test_winning_game_flow():
    game_state = game_engine.create_game("CAT", max_errors=6)

    game_engine.play_letter(game_state, "C")
    assert_equal(game_state["status"], "in_progress", "test_winning_game_flow")

    game_engine.play_letter(game_state, "A")
    assert_equal(game_state["status"], "in_progress", "test_winning_game_flow")

    game_engine.play_letter(game_state, "T")
    assert_equal(game_state["status"], "won", "test_winning_game_flow")
    assert_true(game_engine.is_won(game_state), "test_winning_game_flow")


# Verify full loss scenario with status change to lost
def test_losing_game_flow():
    game_state = game_engine.create_game("CAT", max_errors=3)

    game_engine.play_letter(game_state, "X")
    assert_equal(game_state["errors"], 1, "test_losing_game_flow")

    game_engine.play_letter(game_state, "Y")
    assert_equal(game_state["errors"], 2, "test_losing_game_flow")

    game_engine.play_letter(game_state, "Z")
    assert_equal(game_state["errors"], 3, "test_losing_game_flow")
    assert_equal(game_state["status"], "lost", "test_losing_game_flow")
    assert_true(game_engine.is_lost(game_state), "test_losing_game_flow")


# Execute all tests and log pass/fail summary
def run_all_tests():
    tests = [
        test_create_game_basic,
        test_create_game_custom_max_errors,
        test_create_game_lowercase_word,
        test_masked_word_no_letters_played,
        test_masked_word_partial_guess,
        test_masked_word_all_letters_guessed,
        test_masked_word_repeated_letters,
        test_play_valid_correct_letter,
        test_play_valid_incorrect_letter,
        test_play_lowercase_letter,
        test_play_already_played_letter,
        test_play_invalid_multiple_letters,
        test_play_invalid_number,
        test_play_invalid_empty_string,
        test_is_won_all_letters_guessed,
        test_is_won_some_letters_missing,
        test_is_won_extra_letters,
        test_is_lost_max_errors_reached,
        test_is_lost_errors_below_max,
        test_get_played_letters_empty,
        test_get_played_letters_sorted,
        test_winning_game_flow,
        test_losing_game_flow,
    ]

    test_logger.log_header("Game Engine Tests")

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

    test_logger.log_summary("Game Engine Tests", passed, failed)
    return failed == 0


if __name__ == '__main__':
    test_logger.clear()
    run_all_tests()
    test_logger.save()
