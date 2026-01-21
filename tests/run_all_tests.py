# tests/run_all_tests.py

"""
Main test runner that executes all test suites and logs results.
This script runs all unit tests in a procedural style and generates a comprehensive log file.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_logger import setup_test_logger

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'test_errors.log')


def run_all_tests():
    """
    Discovers and runs all tests in the tests directory.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = setup_test_logger()

    logger.info(f"\nTEST RUN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("HANGMAN GAME - UNIT TEST SUITE")
    print()

    import tests.test_game_engine as test_game_engine
    import tests.test_word_manager as test_word_manager
    import tests.test_language_manager as test_language_manager

    all_success = True

    print("Running Game Engine Tests...")
    success = test_game_engine.run_all_tests()
    all_success = all_success and success
    print()

    print("Running Word Manager Tests...")
    success = test_word_manager.run_all_tests()
    all_success = all_success and success
    print()

    print("Running Language Manager Tests...")
    success = test_language_manager.run_all_tests()
    all_success = all_success and success
    print()

    logger.info(f"\nTEST RUN COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if all_success:
        logger.info("\nALL TESTS PASSED!")
        print("ALL TESTS PASSED!")
    else:
        logger.error("\nSOME TESTS FAILED!")
        print("SOME TESTS FAILED!")

    print(f"\nDetailed logs written to: {LOG_FILE}")
    print()

    return all_success


def main():
    """
    Main entry point for the test runner.
    """
    success = run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
