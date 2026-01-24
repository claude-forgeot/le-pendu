# Main test runner executing all test suites and logging results

from tests import test_logger

# Logger tests
test_logger.clear()
test_logger.log("HANGMAN GAME - UNIT TESTS")

# Run Game Engine tests
from tests import test_game_engine
test_game_engine.run_all_tests()

# Run Word Manager tests
from tests import test_word_manager
test_word_manager.run_all_tests()

# Run Language Manager tests
from tests import test_language_manager
test_language_manager.run_all_tests()

# Run Score Manager tests
from tests import test_score_manager
test_score_manager.run_all_tests()

test_logger.log("\nALL TESTS COMPLETED")
test_logger.save()
