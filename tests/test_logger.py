# Test result logger with buffered output and file persistence

import os
from datetime import datetime

# __file__ = current file path (test_logger.py)
# os.path.dirname(__file__) = tests/ folder
# os.path.join builds path with correct separator (/ on Linux, \ on Windows)
# '..' goes up one level to project root, then into 'logs'
LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOGS_DIR, 'test_results.log')

_log_lines = []


# Reset log buffer for a new test session
def clear():
    global _log_lines
    _log_lines = []


# Append message to buffer and print to console
def log(message):
    global _log_lines
    _log_lines.append(message)
    print(message)


# Log section title with blank lines around it
def log_header(title):
    log("")
    log(title)
    log("")


# Format and log test result with OK or ERROR prefix
def log_result(test_name, passed, error_message=None):
    if passed:
        log(f"OK - {test_name}")
    else:
        log(f"ERROR - {test_name}: {error_message}")


# Log pass/fail count summary for a test module
def log_summary(module_name, passed, failed):
    log(f"\n{module_name}: {passed} passed, {failed} failed")


# Write buffered log lines to test_results.log with timestamp
def save():
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
