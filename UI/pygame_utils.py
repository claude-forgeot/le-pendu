# UI/pygame_utils.py

"""
Shared Pygame utilities for the Hangman game.
Contains font creation, image loading, and common UI functions.
"""

import pygame
import sys
import os
import subprocess

from UI import constants


# Global sound object (initialized by load_sounds)
_sound_click = None


def create_fonts():
    """
    Create and return a dictionary of commonly used fonts.
    Call this after pygame.init().
    """
    return {
        "word": pygame.font.SysFont("Arial", 60, bold=True),
        "info": pygame.font.SysFont("Arial", 30, bold=True),
        "button": pygame.font.SysFont("Arial", 20, bold=True),
        "timer": pygame.font.SysFont("Consolas", 60, bold=True),
        "small": pygame.font.SysFont("Arial", 20, bold=True),
    }


def load_hangman_images(size=None):
    """
    Load and scale hangman body part images.
    Returns a dictionary mapping error count (1-5) to image surfaces.
    """
    if size is None:
        size = constants.HANGMAN_SPRITE_SIZE

    images = {}
    image_paths = {
        1: constants.IMG_HEAD,
        2: constants.IMG_RIGHT_ARM,
        3: constants.IMG_LEFT_ARM,
        4: constants.IMG_RIGHT_LEG,
        5: constants.IMG_LEFT_LEG,
    }

    for key, path in image_paths.items():
        try:
            img = pygame.image.load(path)
            images[key] = pygame.transform.scale(img, (size, size))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")

    return images


def load_sounds():
    """
    Load sound effects. Call this after pygame.mixer.init().
    """
    global _sound_click

    try:
        if os.path.exists(constants.AUDIO_CLICK):
            _sound_click = pygame.mixer.Sound(constants.AUDIO_CLICK)
    except pygame.error as e:
        print(f"Error loading click sound: {e}")
        _sound_click = None


def play_click_sound():
    """Play the click sound effect if available."""
    if _sound_click:
        _sound_click.play()


def return_to_menu():
    """
    Stop all audio, quit pygame, and launch the main menu.
    """
    play_click_sound()
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.quit()

    menu_path = os.path.join(constants.BASE_DIR, "UI", "graphic_view.py")
    subprocess.Popen([sys.executable, menu_path])
    sys.exit()


def draw_rounded_button(surface, color, rect, text, font, text_color=None):
    """
    Draw a rounded button with centered text.

    Args:
        surface: Pygame surface to draw on
        color: Button fill color
        rect: pygame.Rect defining button position and size
        text: Text to display on button
        font: Pygame font for text
        text_color: Color for text (defaults to WHITE)
    """
    if text_color is None:
        text_color = constants.WHITE

    pygame.draw.rect(surface, color, rect, border_radius=int(rect.height / 3))
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def draw_button_with_border(surface, rect, color, hover_color, mouse_pos, label, font):
    """
    Draw a button with border and hover effect.

    Args:
        surface: Pygame surface to draw on
        rect: pygame.Rect defining button position and size
        color: Normal button color
        hover_color: Color when mouse hovers
        mouse_pos: Current mouse position tuple
        label: Text to display
        font: Pygame font for text
    """
    is_hover = rect.collidepoint(mouse_pos)

    if is_hover:
        pygame.draw.rect(surface, constants.GOLD, rect.inflate(6, 6), border_radius=12)

    pygame.draw.rect(
        surface,
        hover_color if is_hover else color,
        rect,
        border_radius=10
    )
    pygame.draw.rect(surface, constants.WHITE, rect, 2, border_radius=10)

    text_surf = font.render(label, True, constants.WHITE)
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))

    return is_hover
