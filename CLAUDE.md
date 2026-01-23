# Coding Standards

This document defines the coding standards and conventions for the Hangman (Le Pendu) project.

Project uses Pygame for graphical interface only (no CLI).

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

## CRITICAL RULE: Beginner-Level Python Only

Use only basic Python concepts that are taught at beginner level:
- Variables and basic data types (str, int, float, bool)
- Lists and dictionaries
- Loops (for, while)
- Conditionals (if/elif/else)
- Functions (def)
- File I/O with open()
- try/except for error handling
- Basic imports (os, sys, random)
- `__main__` and `__init__.py` basics

**AVOID these advanced concepts:**
- Classes and OOP (see No Classes rule)
- List comprehensions (use regular for loops instead)
- Lambda functions
- Decorators
- Generators (yield)
- Type annotations (: str, -> int, etc.)
- Advanced modules unless necessary (cv2 and subprocess are exceptions for video/navigation)

## CRITICAL RULE: Data Storage Format

All data must be stored in TXT format only (NO JSON anywhere):
- English words: `data/words_en.txt`
- French words: `data/words_fr.txt`
- UI translations: `data/locales.txt`

TXT file format for words:
```
[facile]
word1
word2

[moyen]
word3
word4

[difficile]
word5
word6
```

TXT file format for locales:
```
[fr]
key=value

[en]
key=value
```

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

## Pygame UI Design Patterns

### Color Scheme

All UI views must use the color constants defined in [UI/constants.py](UI/constants.py):

```python
from UI import constants

constants.WHITE        # Primary text and borders
constants.BLACK        # Backgrounds
constants.DARK_BLUE    # Primary buttons
constants.GREEN        # Success/easy difficulty
constants.ORANGE       # Warning/medium difficulty
constants.RED          # Error/hard difficulty
constants.PURPLE       # Special actions
constants.GOLD         # Highlights and active states
```

Never define colors inline. Always reference constants for consistency.

### Button Creation

Buttons must follow these patterns:

**Rounded Buttons with Borders**:
```python
# Create button rect (responsive sizing)
btn_w, btn_h = 120, 50
btn = pygame.Rect(x, y, btn_w, btn_h)

# Detect hover state
mouse_pos = pygame.mouse.get_pos()
is_hover = btn.collidepoint(mouse_pos)

# Draw with hover effect
color = constants.PURPLE if is_hover else constants.DARK_BLUE
pygame.draw.rect(screen, color, btn, border_radius=10)
pygame.draw.rect(screen, constants.WHITE, btn, 2, border_radius=10)
```

**Button Text Rendering**:
```python
# Center text in button
text_surf = fonts['medium'].render("Button Text", True, constants.WHITE)
text_rect = text_surf.get_rect(center=btn.center)
screen.blit(text_surf, text_rect)
```

**Visual Highlight for Selection**:
```python
# Draw gold outline for selected items
if is_selected:
    pygame.draw.rect(screen, constants.GOLD, btn.inflate(6, 6), border_radius=12)
```

### Responsive Layout

All UI elements must scale based on window dimensions:

```python
# Get window dimensions
w, h = screen.get_size()

# Calculate positions relative to window size
center_x = w // 2
center_y = h // 2

# Button grid with spacing
spacing = 20
btn_width = 200
x = center_x - btn_width // 2
y = center_y - (num_buttons * (btn_height + spacing)) // 2
```

### Text Input Fields

Text input must follow these patterns:

**Input Box with Active State**:
```python
# Active state changes color
input_active = False  # Toggle on click
color = constants.GOLD if input_active else constants.WHITE

# Draw input box
input_rect = pygame.Rect(x, y, width, height)
pygame.draw.rect(screen, constants.DARK_BLUE, input_rect, border_radius=8)
pygame.draw.rect(screen, color, input_rect, 2, border_radius=8)

# Render text content
text_surf = fonts['medium'].render(input_text, True, constants.WHITE)
screen.blit(text_surf, (input_rect.x + 10, input_rect.y + 10))
```

**Input Event Handling**:
```python
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        input_active = input_rect.collidepoint(event.pos)

    if event.type == pygame.KEYDOWN and input_active:
        if event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        elif event.key == pygame.K_RETURN:
            # Process input
            pass
        else:
            input_text += event.unicode
```

### Overlay Pattern

Modal overlays must use semi-transparent backgrounds:

```python
# Create semi-transparent overlay
overlay = pygame.Surface((w, h))
overlay.set_alpha(200)
overlay.fill(constants.BLACK)
screen.blit(overlay, (0, 0))

# Draw modal content on top
modal_rect = pygame.Rect(center_x - 300, center_y - 200, 600, 400)
pygame.draw.rect(screen, constants.DARK_BLUE, modal_rect, border_radius=15)
pygame.draw.rect(screen, constants.WHITE, modal_rect, 3, border_radius=15)
```

### Navigation Patterns

**Back Button** (standard placement: top-left):
```python
# Back button in top-left corner
back_btn = pygame.Rect(20, 20, 100, 40)
mouse_pos = pygame.mouse.get_pos()
is_hover = back_btn.collidepoint(mouse_pos)

color = constants.ORANGE if is_hover else constants.RED
pygame.draw.rect(screen, color, back_btn, border_radius=8)
pygame.draw.rect(screen, constants.WHITE, back_btn, 2, border_radius=8)

# Handle click
if event.type == pygame.MOUSEBUTTONDOWN:
    if back_btn.collidepoint(event.pos):
        return "main_menu"  # Return to main menu
```

### Font Usage

Use the fonts dictionary from [UI/constants.py](UI/constants.py):

```python
fonts = {
    'small': pygame.font.Font(None, 24),
    'medium': pygame.font.Font(None, 36),
    'large': pygame.font.Font(None, 48),
    'title': pygame.font.Font(None, 72)
}

# Title text
title = fonts['title'].render("Game Title", True, constants.WHITE)

# Body text
body = fonts['medium'].render("Instructions...", True, constants.WHITE)

# Small labels
label = fonts['small'].render("Label:", True, constants.WHITE)
```

### View Function Structure

All view functions must follow this structure:

```python
def my_view(screen, game_state):
    """
    Render my view screen.
    Returns next view name or None to continue current view.
    """
    # Initialize on first call
    if not hasattr(my_view, 'initialized'):
        # Load resources, initialize state
        my_view.initialized = True

    # Get window dimensions
    w, h = screen.get_size()

    # Fill background
    screen.fill(constants.BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle clicks
            pass
        if event.type == pygame.KEYDOWN:
            # Handle keyboard
            pass

    # Get mouse position for hover effects
    mouse_pos = pygame.mouse.get_pos()

    # Draw UI elements with hover detection
    # ...

    # Update display
    pygame.display.flip()

    # Return next view or None
    return None
```

### Audio Integration

Load and play audio using pygame.mixer:

```python
from UI import constants

# Load audio (OGG format required for compatibility)
if not pygame.mixer.get_init():
    pygame.mixer.init()

try:
    pygame.mixer.music.load(constants.AUDIO_MAIN_MENU)
    pygame.mixer.music.play(-1)  # -1 for loop
except pygame.error as e:
    print(f"Could not load audio: {e}")
```

Audio files must be in OGG format (not MP3) for SDL_mixer compatibility.

### Helper Functions

Use helper functions from [UI/pygame_utils.py](UI/pygame_utils.py) when available:

```python
from UI.pygame_utils import draw_rounded_button, draw_text_centered

# Use helper instead of manual drawing
draw_rounded_button(screen, btn_rect, "Click Me", fonts['medium'],
                   constants.DARK_BLUE, constants.WHITE, is_hover)
```

### Example UI View

See [UI/add_word_view.py](UI/add_word_view.py) for a complete reference implementation that demonstrates all these patterns:
- Overlay with semi-transparent background
- Responsive button grid
- Text input with active state
- Difficulty selection with visual feedback
- Hover effects on all interactive elements
- Language selection
- Back button navigation
