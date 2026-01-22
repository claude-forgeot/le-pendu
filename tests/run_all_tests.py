# tests/run_all_tests.py

"""
Main test runner that executes all test suites.
Run with: python -m tests.run_all_tests
"""

print("HANGMAN GAME - UNIT TESTS")
print("")

# Run Game Engine tests
from tests import test_game_engine
test_game_engine.run_all_tests()
print("")

# Run Word Manager tests (runs on import)
from tests import test_word_manager
print("")

# Run Language Manager tests (runs on import)
from tests import test_language_manager
print("")

print("ALL TESTS COMPLETED")
