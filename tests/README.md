# Hangman Game Test Suite

Comprehensive unit tests for the Hangman game project written in procedural style.

## Test Structure

The test suite is organized into the following modules using simple functions without classes:

- **test_game_engine.py**: Tests for core game logic (23 tests)
  - Game creation
  - Letter playing mechanics
  - Win/loss conditions
  - Masked word generation
  - Game flow integration

- **test_word_manager.py**: Tests for word management (15 tests)
  - Word loading from files
  - Random word selection
  - Error handling for missing/corrupted data

- **test_language_manager.py**: Tests for internationalization (18 tests)
  - Locale loading
  - Language switching
  - Text retrieval and formatting
  - Multi-language support

- **test_logger.py**: Test logging utilities
  - Error logging
  - Test result tracking

- **run_all_tests.py**: Main test runner
  - Executes all test suites
  - Generates detailed logs
  - Provides test summary

## Running Tests

### Run All Tests

```bash
python tests/run_all_tests.py
```

### Run Individual Test Module

```bash
python tests/test_game_engine.py
python tests/test_word_manager.py
python tests/test_language_manager.py
```

## Test Coverage

The test suite includes:

- **56 unit tests** covering all major components
  - 23 game engine tests
  - 15 word manager tests
  - 18 language manager tests
- **Normal case testing**: Expected behavior with valid inputs
- **Edge case testing**: Boundary conditions and unusual inputs
- **Error handling testing**: Invalid inputs and missing data
- **Integration testing**: Complete game flow scenarios

## Log Files

Test results and errors are automatically logged to:

```
logs/test_errors.log
```

The log file contains:
- Timestamp of each test run
- Detailed error messages for failures
- Test execution summary
- Full stack traces for debugging

## Test Conventions

All tests follow these conventions:

- **Procedural style**: Tests use simple functions without classes
- **English comments and code**: Code and comments are in English
- **No decorations**: Comments are plain and functional
- **Descriptive names**: Test functions clearly describe what they test
- **Helper functions**: Custom assert functions for common checks
- **Comprehensive coverage**: Each function has multiple test cases
- **Error logging**: All failures are logged for analysis

## Adding New Tests

To add new tests:

1. Create a new test file following the naming convention: `test_<module_name>.py`
2. Import necessary modules and test_logger
3. Create helper assert functions if needed
4. Add test functions starting with `test_`
5. Use helper functions to log errors with `log_test_error()`
6. Create a `run_all_tests()` function that runs all test functions
7. Add a `if __name__ == '__main__':` block to run tests directly

Example:

```python
from tests.test_logger import log_test_error

def assert_equal(actual, expected, test_name):
    """Helper function to assert equality and log errors."""
    if actual != expected:
        error_msg = f"Expected {expected}, got {actual}"
        log_test_error(test_name, error_msg)
        raise AssertionError(error_msg)

def test_new_functionality():
    """Test description here."""
    result = function_to_test()
    assert_equal(result, expected_value, "test_new_functionality")

def run_all_tests():
    """Run all tests."""
    tests = [test_new_functionality]
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

    print(f"\nTests: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
```

## Continuous Integration

The test suite is designed to be easily integrated into CI/CD pipelines:

- Exit code 0 on success
- Exit code 1 on failure
- Detailed logs for debugging
- Summary output to console

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)
