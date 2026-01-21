# Testing Documentation

## Overview

This document describes the comprehensive test suite for the Hangman (Le Pendu) game project.

## Test Suite Summary

The test suite includes 56 unit tests written in procedural style across 3 main test modules:

### Test Files

1. **tests/test_game_engine.py** (23 tests)
   - Tests for core game logic
   - Game state creation and management
   - Letter playing mechanics
   - Win/loss condition validation
   - Masked word generation
   - Complete game flow scenarios

2. **tests/test_word_manager.py** (15 tests)
   - Word file loading and parsing
   - Random word selection by difficulty
   - Error handling for missing files
   - JSON parsing error handling
   - Multi-language support

3. **tests/test_language_manager.py** (18 tests)
   - Locale file loading
   - Language switching functionality
   - Text retrieval and formatting
   - Error handling for missing translations
   - Multi-language support validation

### Supporting Files

- **tests/test_logger.py**: Logging utility for test errors
- **tests/run_all_tests.py**: Main test runner with detailed logging
- **tests/README.md**: Detailed testing documentation

## Running Tests

### Run All Tests

```bash
python tests/run_all_tests.py
```

### Run Specific Test Module

```bash
python tests/test_game_engine.py
python tests/test_word_manager.py
python tests/test_language_manager.py
```

## Test Coverage

### Game Engine Tests (test_game_engine.py)

**TestGameCreation** - 5 tests
- Basic game creation
- Custom max errors
- Lowercase to uppercase conversion
- Empty word handling
- Single letter words

**TestGetMaskedWord** - 5 tests
- No letters played
- Partial guess display
- All letters guessed
- Single letter words
- Repeated letters in word

**TestPlayLetter** - 8 tests
- Valid correct letters
- Valid incorrect letters
- Lowercase conversion
- Already played letters
- Multiple letters validation
- Number validation
- Special character validation
- Empty string validation

**TestIsWon** - 5 tests
- All letters guessed
- Some letters missing
- Extra wrong letters played
- No letters played
- Single letter word win

**TestIsLost** - 4 tests
- Max errors reached
- Errors below max
- No errors
- Errors exceeding max

**TestGetPlayedLetters** - 3 tests
- Empty played letters
- Sorted letter order
- Multiple played letters

**TestGameFlow** - 4 tests
- Complete winning game
- Complete losing game
- Mixed correct/incorrect guesses
- Repeated letter words

### Word Manager Tests (test_word_manager.py)

**TestLoadWords** - 4 tests
- French word file loading
- English word file loading
- Nonexistent language handling
- Data structure validation

**TestGetRandomWord** - 8 tests
- Easy difficulty selection
- Medium difficulty selection
- Hard difficulty selection
- Case insensitive difficulty
- Invalid difficulty handling
- Empty word list handling
- Uppercase conversion
- Multiple random selections

**TestGetWord** - 5 tests
- French easy words
- English medium words
- Invalid language handling
- Invalid difficulty handling
- Random word variation

**TestWordManagerWithCorruptedData** - 3 tests
- Corrupted JSON handling
- Missing file handling
- Missing data file in get_word

### Language Manager Tests (test_language_manager.py)

**TestInitialize** - 2 tests
- Locale data loading
- Default language setting

**TestSetLanguage** - 4 tests
- French language setting
- English language setting
- Invalid language handling
- Empty string handling

**TestGetCurrentLanguage** - 2 tests
- Default language retrieval
- Language after change

**TestGetText** - 6 tests
- French text retrieval
- English text retrieval
- Nonexistent key handling
- Text formatting with arguments
- Missing format arguments
- Multiple key retrieval

**TestGetAvailableLanguages** - 4 tests
- List return type
- French language presence
- English language presence
- Language count validation

**TestLoadLocales** - 3 tests
- Dictionary return type
- Language presence validation
- Data structure validation

**TestLanguageManagerWithCorruptedData** - 4 tests
- Missing file handling
- Corrupted JSON handling
- Initialize with missing file
- Get text with no locales

**TestLanguageManagerIntegration** - 2 tests
- Language switching with text retrieval
- Multiple text retrievals in same language

## Error Logging

All test failures and errors are automatically logged to:
```
logs/test_errors.log
```

The log file includes:
- Timestamp for each test run
- Detailed error messages
- Full stack traces
- Test execution summary
- Pass/fail statistics

## Test Conventions

All tests follow these conventions:

1. **Procedural Style**: Tests use simple functions without classes
2. **Naming**: Test functions start with `test_` and have descriptive names
3. **Documentation**: Each test has a docstring explaining what it tests
4. **Helper Functions**: Custom assert functions for logging errors
5. **Error Logging**: Test failures are logged using the test_logger module
6. **Isolation**: Tests are independent and can run in any order
7. **Clean Up**: Temporary files are cleaned up after tests
8. **Language**: Code and comments in English (except UI text testing)

## Continuous Integration

The test suite is designed for CI/CD integration:

- Exit code 0 on success, 1 on failure
- Machine-readable output format
- Detailed error logs for debugging
- Fast execution (all tests run in < 1 second)
- No external dependencies required

## Adding New Tests

To add new tests:

1. Create test methods in appropriate test class
2. Use descriptive names (e.g., `test_play_letter_with_special_character`)
3. Add docstring explaining what is being tested
4. Use try-except blocks with log_test_error for assertion failures
5. Test both normal and edge cases
6. Include error handling tests

Example:
```python
def test_new_feature(self):
    """Test description here."""
    try:
        result = function_to_test()
        self.assertEqual(result, expected_value)
    except AssertionError as e:
        log_test_error("test_new_feature", str(e))
        raise
```

## Test Results

Current test status: **56/56 tests passing** (100% pass rate)

- Game Engine: 23/23 passing
- Word Manager: 15/15 passing
- Language Manager: 18/18 passing

## Requirements

- Python 3.6 or higher
- Standard library only
- No external test framework dependencies
