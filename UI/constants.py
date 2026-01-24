# UI/constants.py

"""
Shared constants for the Hangman game UI.
Contains colors, dimensions, and resource paths.
"""

import os

# Screen dimensions
WIDTH = 900
HEIGHT = 600

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (46, 204, 113)
ORANGE = (230, 126, 34)
RED = (231, 76, 60)
DARK_BLUE = (44, 62, 80)
PURPLE = (155, 89, 182)
GOLD = (241, 196, 15)

# Hover colors (lighter variants)
GREEN_HOVER = (82, 222, 139)
ORANGE_HOVER = (255, 159, 67)
RED_HOVER = (255, 107, 91)
DARK_BLUE_HOVER = (52, 73, 94)
PURPLE_HOVER = (187, 143, 206)
GOLD_HOVER = (244, 208, 63)

# Overlay color (RGBA)
BLACK_OVERLAY = (0, 0, 0, 180)

# Resource paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIOS_DIR = os.path.join(ASSETS_DIR, "audios")

# Image paths
IMG_BACKGROUND_HOME = os.path.join(IMAGES_DIR, "home.jpg")
IMG_BACKGROUND_GAME = os.path.join(IMAGES_DIR, "pendu.png")
IMG_LOGO = os.path.join(IMAGES_DIR, "logo.png")
IMG_FLAG_FR = os.path.join(IMAGES_DIR, "france.png")
IMG_FLAG_US = os.path.join(IMAGES_DIR, "usa.png")

# Hangman body parts
IMG_HEAD = os.path.join(IMAGES_DIR, "tete.png")
IMG_RIGHT_ARM = os.path.join(IMAGES_DIR, "bras_droit.png")
IMG_LEFT_ARM = os.path.join(IMAGES_DIR, "bras_gauche.png")
IMG_RIGHT_LEG = os.path.join(IMAGES_DIR, "jambe_droite.png")
IMG_LEFT_LEG = os.path.join(IMAGES_DIR, "jambe_gauche.png")

# Audio paths
AUDIO_MAIN_MENU = os.path.join(AUDIOS_DIR, "main.ogg")
AUDIO_EASY_MODE = os.path.join(AUDIOS_DIR, "facile.ogg")
AUDIO_NORMAL_MODE = os.path.join(AUDIOS_DIR, "normal.ogg")
AUDIO_HARD_MODE = os.path.join(AUDIOS_DIR, "difficile.ogg")
AUDIO_INFINITE_MODE = os.path.join(AUDIOS_DIR, "infinite.mp3")
AUDIO_VICTORY = os.path.join(AUDIOS_DIR, "victoire.ogg")
AUDIO_WIN_HARD = os.path.join(AUDIOS_DIR, "winhard.ogg")
AUDIO_LOSE_NORMAL = os.path.join(AUDIOS_DIR, "macron.ogg")
AUDIO_LOSE_HARD = os.path.join(AUDIOS_DIR, "losehard.ogg")
AUDIO_LOSE_INFINITE = os.path.join(AUDIOS_DIR, "lose_infinite.mp3")

# Video paths (folder is "vidéo" with accent)
VIDEO_LOSE_HARD = os.path.join(ASSETS_DIR, "vidéo", "losehard.mp4")
VIDEO_LOSE_NORMAL = os.path.join(ASSETS_DIR, "vidéo", "macron.mp4")

# Sprite size for hangman parts
HANGMAN_SPRITE_SIZE = 100
