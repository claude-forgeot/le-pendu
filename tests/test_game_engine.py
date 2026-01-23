# tests/test_game_engine.py

"""
Unit tests for the game_engine module.
Run with: python -m tests.test_game_engine
"""

from models import game_engine


def assert_equal(actual, expected, test_name):
    """Helper function to assert equality."""
    if actual != expected:
        raise AssertionError(f"Expected {expected}, got {actual}")


def assert_true(value, test_name):
    """Helper function to assert true."""
    if not value:
        raise AssertionError(f"Expected True, got {value}")


def assert_false(value, test_name):
    """Helper function to assert false."""
    if value:
        raise AssertionError(f"Expected False, got {value}")


def assert_in(item, container, test_name):
    """Helper function to assert item is in container."""
    if item not in container:
        raise AssertionError(f"Expected {item} to be in {container}")


def test_create_game_basic():
    """Test basic game creation with default parameters."""
    game_state = game_engine.create_game("PYTHON")

    assert_equal(game_state["secret_word"], "PYTHON", "test_create_game_basic")
    assert_equal(game_state["max_errors"], 7, "test_create_game_basic")
    assert_equal(game_state["errors"], 0, "test_create_game_basic")
    assert_equal(game_state["status"], "in_progress", "test_create_game_basic")
    assert_equal(len(game_state["letters_played"]), 0, "test_create_game_basic")


def test_create_game_custom_max_errors():
    """Test game creation with custom max errors."""
    game_state = game_engine.create_game("HANGMAN", max_errors=10)

    assert_equal(game_state["secret_word"], "HANGMAN", "test_create_game_custom_max_errors")
    assert_equal(game_state["max_errors"], 10, "test_create_game_custom_max_errors")


def test_create_game_lowercase_word():
    """Test that lowercase words are converted to uppercase."""
    game_state = game_engine.create_game("python")

    assert_equal(game_state["secret_word"], "PYTHON", "test_create_game_lowercase_word")


def test_masked_word_no_letters_played():
    """Test masked word when no letters have been played."""
    game_state = game_engine.create_game("PYTHON")
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "_ _ _ _ _ _", "test_masked_word_no_letters_played")


def test_masked_word_partial_guess():
    """Test masked word with some letters guessed."""
    game_state = game_engine.create_game("PYTHON")
    game_state["letters_played"].add("P")
    game_state["letters_played"].add("O")
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "P _ _ _ O _", "test_masked_word_partial_guess")


def test_masked_word_all_letters_guessed():
    """Test masked word when all letters are guessed."""
    game_state = game_engine.create_game("PYTHON")
    for letter in "PYTHON":
        game_state["letters_played"].add(letter)
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "P Y T H O N", "test_masked_word_all_letters_guessed")


def test_masked_word_repeated_letters():
    """Test masked word with repeated letters in the word."""
    game_state = game_engine.create_game("HELLO")
    game_state["letters_played"].add("L")
    masked = game_engine.get_masked_word(game_state)

    assert_equal(masked, "_ _ L L _", "test_masked_word_repeated_letters")


def test_play_valid_correct_letter():
    """Test playing a valid letter that is in the word."""
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "P")

    assert_true(result, "test_play_valid_correct_letter")
    assert_in("P", game_state["letters_played"], "test_play_valid_correct_letter")
    assert_equal(game_state["errors"], 0, "test_play_valid_correct_letter")


def test_play_valid_incorrect_letter():
    """Test playing a valid letter that is not in the word."""
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "Z")

    assert_true(result, "test_play_valid_incorrect_letter")
    assert_in("Z", game_state["letters_played"], "test_play_valid_incorrect_letter")
    assert_equal(game_state["errors"], 1, "test_play_valid_incorrect_letter")


def test_play_lowercase_letter():
    """Test playing a lowercase letter is converted to uppercase."""
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "p")

    assert_true(result, "test_play_lowercase_letter")
    assert_in("P", game_state["letters_played"], "test_play_lowercase_letter")


def test_play_already_played_letter():
    """Test playing a letter that has already been played."""
    game_state = game_engine.create_game("PYTHON")
    game_engine.play_letter(game_state, "P")
    result = game_engine.play_letter(game_state, "P")

    assert_false(result, "test_play_already_played_letter")


def test_play_invalid_multiple_letters():
    """Test playing multiple letters at once."""
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "PY")

    assert_false(result, "test_play_invalid_multiple_letters")


def test_play_invalid_number():
    """Test playing a number instead of a letter."""
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "5")

    assert_false(result, "test_play_invalid_number")


def test_play_invalid_empty_string():
    """Test playing an empty string."""
    game_state = game_engine.create_game("PYTHON")
    result = game_engine.play_letter(game_state, "")

    assert_false(result, "test_play_invalid_empty_string")


def test_is_won_all_letters_guessed():
    """Test win condition when all letters are guessed."""
    game_state = game_engine.create_game("CAT")
    for letter in "CAT":
        game_state["letters_played"].add(letter)

    assert_true(game_engine.is_won(game_state), "test_is_won_all_letters_guessed")


def test_is_won_some_letters_missing():
    """Test win condition when some letters are not yet guessed."""
    game_state = game_engine.create_game("PYTHON")
    game_state["letters_played"].add("P")
    game_state["letters_played"].add("Y")

    assert_false(game_engine.is_won(game_state), "test_is_won_some_letters_missing")


def test_is_won_extra_letters():
    """Test win condition when extra wrong letters were played."""
    game_state = game_engine.create_game("CAT")
    for letter in "CATZYX":
        game_state["letters_played"].add(letter)

    assert_true(game_engine.is_won(game_state), "test_is_won_extra_letters")


def test_is_lost_max_errors_reached():
    """Test loss condition when max errors is reached."""
    game_state = game_engine.create_game("PYTHON", max_errors=3)
    game_state["errors"] = 3

    assert_true(game_engine.is_lost(game_state), "test_is_lost_max_errors_reached")


def test_is_lost_errors_below_max():
    """Test loss condition when errors are below max."""
    game_state = game_engine.create_game("PYTHON", max_errors=6)
    game_state["errors"] = 3

    assert_false(game_engine.is_lost(game_state), "test_is_lost_errors_below_max")


def test_get_played_letters_empty():
    """Test getting played letters when none have been played."""
    game_state = game_engine.create_game("PYTHON")
    letters = game_engine.get_played_letters(game_state)

    assert_equal(letters, [], "test_get_played_letters_empty")


def test_get_played_letters_sorted():
    """Test that played letters are returned in sorted order."""
    game_state = game_engine.create_game("PYTHON")
    for letter in "ZAP":
        game_state["letters_played"].add(letter)
    letters = game_engine.get_played_letters(game_state)

    assert_equal(letters, ["A", "P", "Z"], "test_get_played_letters_sorted")


def test_winning_game_flow():
    """Test a complete winning game scenario."""
    game_state = game_engine.create_game("CAT", max_errors=6)

    game_engine.play_letter(game_state, "C")
    assert_equal(game_state["status"], "in_progress", "test_winning_game_flow")

    game_engine.play_letter(game_state, "A")
    assert_equal(game_state["status"], "in_progress", "test_winning_game_flow")

    game_engine.play_letter(game_state, "T")
    assert_equal(game_state["status"], "won", "test_winning_game_flow")
    assert_true(game_engine.is_won(game_state), "test_winning_game_flow")


def test_losing_game_flow():
    """Test a complete losing game scenario."""
    game_state = game_engine.create_game("CAT", max_errors=3)

    game_engine.play_letter(game_state, "X")
    assert_equal(game_state["errors"], 1, "test_losing_game_flow")

    game_engine.play_letter(game_state, "Y")
    assert_equal(game_state["errors"], 2, "test_losing_game_flow")

    game_engine.play_letter(game_state, "Z")
    assert_equal(game_state["errors"], 3, "test_losing_game_flow")
    assert_equal(game_state["status"], "lost", "test_losing_game_flow")
    assert_true(game_engine.is_lost(game_state), "test_losing_game_flow")


def run_all_tests():
    """Run all game engine tests."""
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

    print(f"\nGame Engine Tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    run_all_tests()
