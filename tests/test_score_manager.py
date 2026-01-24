# tests/test_score_manager.py

"""
Unit tests for the score_manager module.
Run with: python -m tests.test_score_manager
"""

from utils import score_manager
from tests import test_logger


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


def test_calculate_score_basic():
    """Test basic score calculation with correct and wrong letters."""
    state = {
        "secret_word": "cat",
        "letters_played": ["c", "a", "t", "x", "z"]
    }
    score = score_manager.calculate_score(state)
    # 3 correct (c, a, t) * 20 = 60
    # 2 wrong (x, z) * 10 = 20
    # Score = 60 - 20 = 40
    assert_equal(score, 40, "test_calculate_score_basic")


def test_calculate_score_with_time_bonus():
    """Test score calculation with time remaining bonus."""
    state = {
        "secret_word": "cat",
        "letters_played": ["c", "a", "t"]
    }
    score = score_manager.calculate_score(state, time_remaining=10)
    # 3 correct * 20 = 60
    # Time bonus = 10 * 2 = 20
    # Score = 60 + 20 = 80
    assert_equal(score, 80, "test_calculate_score_with_time_bonus")


def test_calculate_score_with_hints():
    """Test score calculation with hint penalty."""
    state = {
        "secret_word": "cat",
        "letters_played": ["c", "a", "t"]
    }
    score = score_manager.calculate_score(state, hints_used=2)
    # 3 correct * 20 = 60
    # Hint penalty = 2 * 20 = 40
    # Score = 60 - 40 = 20
    assert_equal(score, 20, "test_calculate_score_with_hints")


def test_calculate_score_minimum_zero():
    """Test that score cannot go below zero."""
    state = {
        "secret_word": "cat",
        "letters_played": ["x", "y", "z", "w", "q", "r", "s"]
    }
    score = score_manager.calculate_score(state)
    # 0 correct, 7 wrong * 10 = 70
    # Score = 0 - 70 = -70 -> should be 0
    assert_equal(score, 0, "test_calculate_score_minimum_zero")


def test_calculate_score_empty_game():
    """Test score calculation with no letters played."""
    state = {
        "secret_word": "cat",
        "letters_played": []
    }
    score = score_manager.calculate_score(state)
    assert_equal(score, 0, "test_calculate_score_empty_game")


def test_calculate_score_with_set():
    """Test that duplicate letters in played are handled correctly."""
    state = {
        "secret_word": "hello",
        "letters_played": {"h", "e", "l", "o"}
    }
    score = score_manager.calculate_score(state)
    # 4 unique correct letters * 20 = 80
    assert_equal(score, 80, "test_calculate_score_with_set")


def test_calculate_score_combined():
    """Test score calculation with all factors combined."""
    state = {
        "secret_word": "python",
        "letters_played": ["p", "y", "t", "h", "o", "n", "x", "z"]
    }
    score = score_manager.calculate_score(state, time_remaining=15, hints_used=1)
    # 6 correct * 20 = 120
    # 2 wrong * 10 = 20
    # Hint penalty = 1 * 20 = 20
    # Time bonus = 15 * 2 = 30
    # Score = 120 - 20 - 20 + 30 = 110
    assert_equal(score, 110, "test_calculate_score_combined")


def test_check_if_highscore_zero_score():
    """Test that zero score does not qualify as highscore."""
    result = score_manager.check_if_highscore(0, "test_category")
    assert_false(result, "test_check_if_highscore_zero_score")


def test_check_if_highscore_negative_score():
    """Test that negative score does not qualify as highscore."""
    result = score_manager.check_if_highscore(-10, "test_category")
    assert_false(result, "test_check_if_highscore_negative_score")


def test_check_if_highscore_new_category():
    """Test that any positive score qualifies in a new category."""
    result = score_manager.check_if_highscore(1, "brand_new_category_xyz")
    assert_true(result, "test_check_if_highscore_new_category")


def run_all_tests():
    """Run all score manager tests."""
    tests = [
        test_calculate_score_basic,
        test_calculate_score_with_time_bonus,
        test_calculate_score_with_hints,
        test_calculate_score_minimum_zero,
        test_calculate_score_empty_game,
        test_calculate_score_with_set,
        test_calculate_score_combined,
        test_check_if_highscore_zero_score,
        test_check_if_highscore_negative_score,
        test_check_if_highscore_new_category,
    ]

    test_logger.log_header("Score Manager Tests")

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

    test_logger.log_summary("Score Manager Tests", passed, failed)
    return failed == 0


if __name__ == '__main__':
    test_logger.clear()
    run_all_tests()
    test_logger.save()
