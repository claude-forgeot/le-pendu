# tests/test_logger.py

"""
Logger for test results.
Writes results to logs/test_results.log
"""

import os
from datetime import datetime

LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOGS_DIR, 'test_results.log')

_log_lines = []


def clear():
    """Clear the log buffer for a new test run."""
    global _log_lines
    _log_lines = []


def log(message):
    """Add a message to the log buffer and print it."""
    global _log_lines
    _log_lines.append(message)
    print(message)


def log_header(title):
    """Log a section header."""
    log("")
    log(title)
    log("")


def log_result(test_name, passed, error_message=None):
    """Log a single test result."""
    if passed:
        log(f"OK - {test_name}")
    else:
        log(f"ERROR - {test_name}: {error_message}")


def log_summary(module_name, passed, failed):
    """Log the summary for a test module."""
    log(f"\n{module_name}: {passed} passed, {failed} failed")


def save():
    """Save all logged messages to the log file."""
    global _log_lines

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file = open(LOG_FILE, 'a', encoding='utf-8')
        file.write(f"[{timestamp}]\n")
        for line in _log_lines:
            file.write(line + "\n")
        file.write("\n")
        file.close()
        print(f"\nResults saved to: {LOG_FILE}")
    except Exception as e:
        print(f"Error saving log: {e}")
