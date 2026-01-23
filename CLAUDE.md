# Coding Standards

This document defines the coding standards and conventions for the Hangman (Le Pendu) project.

Project uses Pygame for graphical interface only (no CLI).

## Project Structure Snapshot

Last verified: 2025-01-23

```
le-pendu/
    main.py                 # Entry point - calls UI.main_gui()
    requirements.txt        # Dependencies (pygame-ce, opencv-python)
    README.md               # Project documentation
    CLAUDE.md               # This file - coding standards
    convert_audio_to_ogg.sh # Utility script for audio conversion
    UI/
        __init__.py
        graphic_view.py     # Main controller and view manager
        constants.py        # Shared constants (colors, paths, sizes)
        pygame_utils.py     # Helper functions for pygame
        easy_mode_view.py   # Easy mode game view (7 lives)
        normal_mode_view.py # Normal mode game view (7 lives)
        hard_mode_view.py   # Hard mode game view (5 lives)
        infinite_mode_view.py # Infinite mode game view
        add_word_view.py    # Add word form view
    models/
        __init__.py
        game_engine.py      # Core game logic
    utils/
        __init__.py
        word_manager.py     # Word loading and management
        language_manager.py # Localization
        score_manager.py    # Score tracking (TXT format)
    data/
        words_fr.txt        # French words by difficulty
        words_en.txt        # English words by difficulty
        locales.txt         # UI translations
        highscores.txt      # Persisted high scores by category
    assets/
        images/             # Background images, hangman sprites
        audios/             # Music and sound effects (OGG preferred, some MP3)
        video/              # Video files for loss sequences (MP4)
    tests/
        __init__.py
        run_all_tests.py    # Test runner
        test_game_engine.py
        test_word_manager.py
        test_language_manager.py
        test_word_addition.py
    logs/
        .gitkeep            # Directory placeholder
```

### Verification Checklist

Before making changes, verify the codebase matches this structure:
- NO `controllers/` folder (CLI tools removed - game is Pygame only)
- NO `UI/base_view.py` (empty file removed)
- NO `UI/addword_mode_view.py` (duplicate removed - use add_word_view.py)
- NO `highscores.json` at root (use data/highscores.txt)
- NO duplicate MP3 files when OGG equivalent exists

### Audio Files

OGG files (preferred format):
- main.ogg, facile.ogg, difficile.ogg, victoire.ogg
- macron.ogg, winhard.ogg, losehard.ogg

MP3 files (no OGG equivalent):
- infinite.mp3, lose_infinite.mp3, normal.mp3

Known issue: normal_mode_view.py references normal.ogg but only normal.mp3 exists

## Dependencies

Required packages:
- `pygame-ce` (Community Edition) - Graphics and audio
- `opencv-python` - Video playback for loss sequences

Install with: `pip install pygame-ce opencv-python`

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

Code and comments must be written in English. UI-facing text must be localized:
- All variable names, function names, and identifiers: English
- All code comments and docstrings: English
- All log messages and debug output: English
- User interface text (displayed to users): Use `language_manager.get_text()` for localization

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
- Advanced modules unless necessary (cv2 is an exception for video playback)

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

## Localization System

The game supports French and English. Language selection in the main menu affects the entire application.

### Language Manager Usage

All UI text must use the localization system via [utils/language_manager.py](utils/language_manager.py):

```python
from utils import language_manager

# Get localized text
title = language_manager.get_text("victory")
button_label = language_manager.get_text("retry")

# Get current language
current_lang = language_manager.get_current_language()  # Returns "fr" or "en"

# Set language (called from main menu)
language_manager.set_language("en")
```

### Adding New Locale Keys

When adding new UI text, add keys to both language sections in `data/locales.txt`:

```
[fr]
my_new_key=Mon texte en francais

[en]
my_new_key=My English text
```

### Word Dictionary Integration

Words are loaded from the dictionary matching the current language:
- French: `data/words_fr.txt`
- English: `data/words_en.txt`

```python
from utils import word_manager
from utils import language_manager

# Get word from correct dictionary based on current language
current_lang = language_manager.get_current_language()
word = word_manager.get_word(current_lang, "facile")

# Add word to correct dictionary
word_manager.add_word(current_lang, "newword", "moyen")
```

### Common Locale Keys

Available keys in `data/locales.txt`:
- `victory`, `game_over`, `word_was` - Game result messages
- `pause`, `continue`, `restart`, `quit`, `menu` - Pause menu buttons
- `retry`, `replay` - End screen buttons
- `hint`, `letters_used` - Game interface labels
- `new_record`, `press_enter` - Highscore input
- `add_word_title`, `add_word_button`, `add_word_back` - Add word view
- `button_facile`, `button_normal`, `button_difficile`, `button_infini` - Main menu buttons
- `difficulty_facile`, `difficulty_moyen`, `difficulty_difficile` - Difficulty labels

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

## Single-Window Architecture

The game runs in a single pygame window. Navigation between views is handled by returning view names.

### View Manager

The main controller [UI/graphic_view.py](UI/graphic_view.py) manages all view transitions:
- Initializes pygame once at startup
- Creates shared screen, fonts, and clock objects
- Routes between views based on return values

```python
def run_game():
    """Main game loop - manages view transitions."""
    initialize_pygame()
    current_view = "main_menu"

    while current_view is not None:
        if current_view == "main_menu":
            current_view = main_menu_view()
        elif current_view == "easy_mode":
            from UI import easy_mode_view
            current_view = easy_mode_view.run_view(screen, fonts, clock)
        # ... other views

    pygame.quit()
    sys.exit()
```

### View Entry Point

Each view module must export a `run_view(screen, fonts, clock)` function:

```python
def run_view(screen, fonts, clock):
    """
    Main entry point for this view.
    Returns the next view name: "main_menu", "easy_mode", "quit", etc.
    Returns None to quit the game.
    """
    load_resources()
    # ... view logic
    return "main_menu"  # Navigate to next view
```

### View Return Values

Views return strings to indicate the next view:
- `"main_menu"` - Return to main menu
- `"easy_mode"` - Start easy mode
- `"normal_mode"` - Start normal mode
- `"hard_mode"` - Start hard mode
- `"infinite_mode"` - Start infinite mode
- `"add_word"` - Open add word screen
- `"settings"` - Open settings
- `"highscores"` - Show highscores
- `None` - Quit the game

### No Subprocess

NEVER use subprocess to launch game modes. All navigation is done via return values:

BAD:
```python
subprocess.Popen([sys.executable, "UI/easy_mode_view.py"])
```

GOOD:
```python
return "easy_mode"
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

All view modules must follow this structure with a `run_view` entry point:

```python
# Module-level variables for resources
img_bg = None
imgs = {}

def load_resources():
    """Load resources for this view."""
    global img_bg, imgs
    # Load images, sounds, etc.
    pass

def initialize_game():
    """Initialize game state for this view."""
    # Set up initial state
    pass

def run_view(screen, fonts, clock):
    """
    Main entry point for this view.
    Returns the next view name: "main_menu", "quit", etc.
    """
    load_resources()
    game_state = initialize_game()
    paused = False

    # Define UI rects
    btn_back = pygame.Rect(20, 20, 100, 40)

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Quit game

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return "main_menu"  # Navigate back

            if event.type == pygame.KEYDOWN:
                # Handle keyboard input
                pass

        # Draw UI
        screen.blit(img_bg, (0, 0))
        # ... draw other elements

        pygame.display.flip()
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

Audio files should be in OGG format for SDL_mixer compatibility. Exception: infinite.mp3, lose_infinite.mp3, normal.mp3 (no OGG versions exist).

### Helper Functions

Use helper functions from [UI/pygame_utils.py](UI/pygame_utils.py) when available:

```python
from UI.pygame_utils import draw_rounded_button, draw_text_centered

# Use helper instead of manual drawing
draw_rounded_button(screen, btn_rect, "Click Me", fonts['medium'],
                   constants.DARK_BLUE, constants.WHITE, is_hover)
```

### Example UI Views

See these files for reference implementations:

**[UI/add_word_view.py](UI/add_word_view.py)** - Simple view with form input:
- `run_view(screen, fonts, clock)` entry point
- Text input with active state
- Difficulty selection with visual feedback
- Hover effects on all interactive elements
- Back button returning "main_menu"
- Full localization with `language_manager.get_text()`

**[UI/easy_mode_view.py](UI/easy_mode_view.py)** - Game mode view:
- Module-level resource loading
- Game loop with pause functionality
- Win/lose sequences with localized messages
- Hint system
- Localized button labels and game text

**[UI/graphic_view.py](UI/graphic_view.py)** - Main controller:
- Single pygame initialization
- View manager pattern
- View routing based on return values
- Language selection (flag buttons)
