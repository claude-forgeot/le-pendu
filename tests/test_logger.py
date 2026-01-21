# tests/test_logger.py

"""
Utility module for logging test errors and results.
Provides a simple interface to log test failures to a file for analysis.
"""

import os
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'test_errors.log')

def setup_test_logger():
    """
    Sets up a logger for test errors.
    Creates the logs directory if it doesn't exist.

    Returns:
        logging.Logger: Configured logger instance.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.ERROR)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger

def log_test_error(test_name: str, error_message: str):
    """
    Logs a test error to the log file.

    Args:
        test_name (str): Name of the test that failed.
        error_message (str): Description of the error.
    """
    logger = setup_test_logger()
    logger.error(f"Test '{test_name}' failed: {error_message}")

def log_test_start(test_suite_name: str):
    """
    Logs the start of a test suite.

    Args:
        test_suite_name (str): Name of the test suite being run.
    """
    logger = setup_test_logger()
    logger.info(f"\n{'='*60}\nStarting test suite: {test_suite_name}\n{'='*60}")

def log_test_summary(passed: int, failed: int, errors: int):
    """
    Logs a summary of test results.

    Args:
        passed (int): Number of tests that passed.
        failed (int): Number of tests that failed.
        errors (int): Number of tests with errors.
    """
    logger = setup_test_logger()
    summary = f"\nTest Summary: Passed={passed}, Failed={failed}, Errors={errors}"
    logger.info(summary)
