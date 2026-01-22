# Coding Standards

This document defines the coding standards and conventions for the Hangman (Le Pendu) project.

## CRITICAL RULE: No Decorations

NEVER add decorative elements to code, comments, or output unless explicitly requested by the user:
- No separator lines using `=`, `*`, `-`, `#`, or any other repeated characters
- No emojis, emoticons, or smileys
- No ASCII art or decorative borders
- No banner text or fancy headers
- No excessive punctuation for emphasis

This applies to all code, comments, docstrings, print statements, and log messages.

## CRITICAL RULE: No Classes (No OOP)

NEVER use object-oriented programming with classes. Use procedural programming style only:
- Use functions, not classes or methods
- Use dictionaries or named tuples for data structures instead of class instances
- Keep functions simple and focused on a single responsibility

## CRITICAL RULE: Language Requirements

Code and comments must be written in English. Only UI-facing text should be in French:
- All variable names, function names, and identifiers: English
- All code comments and docstrings: English
- All log messages and debug output: English
- User interface text (displayed to users): French (for localization)

## General Principles

### Language
See CRITICAL RULE: Language Requirements above.

### Code Style
See CRITICAL RULE: No Classes (No OOP) above.

## Comment and Documentation Rules

### No Decorations
Comments and code output must remain clean and functional without any decorative elements.

**PROHIBITED**:
- No separator lines with equals signs (====)
- No separator lines with asterisks (****)
- No separator lines with hyphens (----)
- No emojis or emoticons in comments
- No ASCII art or decorative borders
- No excessive punctuation for emphasis (!!!)

**ALLOWED**:
- Simple single-line comments explaining code logic
- Docstrings for functions with plain text descriptions
- Plain text log messages

**Examples**:

BAD:
```python
# ====================================
# This is a function
# ====================================
def my_function():
    pass

# ************************************
# Important section
# ************************************

print("=" * 50)
print("Welcome")
print("=" * 50)
```

GOOD:
```python
# This is a function
def my_function():
    pass

# Important section

print("Welcome")
```

### Docstrings
Use simple docstrings without decorations:

```python
def calculate_score(points, multiplier):
    """
    Calculate the final score by multiplying points by the multiplier.
    Returns the calculated score as an integer.
    """
    return points * multiplier
```

## Output and Logging

### Console Output
- Keep output messages simple and direct
- No decorative separators in printed messages
- Use clear, concise language

### Log Files
- Log messages should be plain text
- Include timestamp, level, and message only
- No decorative formatting

## Testing

### Test Functions
- Use procedural style with simple functions
- Name tests with `test_` prefix
- Include docstring describing what is tested
- Use custom assert helpers for error logging

### Test Output
- Use simple checkmarks (✓) or crosses (✗) for pass/fail indicators
- No banner text or decorative elements
- Keep summary output minimal

## File Organization

### Imports
- Standard library imports first
- Third-party imports second
- Local imports last
- Separate groups with a single blank line

### Function Order
- Helper functions before main functions
- Public functions before private functions
- Logical grouping of related functions

## Naming Conventions

### Variables and Functions
- Use snake_case for variables and function names
- Use descriptive names that explain purpose
- Avoid single-letter names except for loop counters

### Constants
- Use UPPER_SNAKE_CASE for constants
- Define constants at module level

### Files
- Use snake_case for Python module names
- Use descriptive names that indicate content

## Error Handling

### Error Messages
- Clear and informative without being verbose
- Include context about what went wrong
- No decorative formatting

### Logging Errors
- Log to appropriate file or stream
- Include relevant context (function name, input values)
- Use appropriate log level

## Git Commit Messages

### Format
- Use imperative mood (Add feature, Fix bug)
- Keep first line under 50 characters
- Add detailed description if needed after blank line
- No decorative elements

### Examples

GOOD:
```
Add language switching functionality

Implement set_language() function to switch between
French and English locales at runtime.
```

BAD:
```
**** NEW FEATURE ****
Added super cool language switching!!!
```
