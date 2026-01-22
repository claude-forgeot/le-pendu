"""
Module UI - Interfaces utilisateur pour le jeu du Pendu
Contient les vues graphique (Pygame) et console (CLI)
"""

from .graphic_view import main_gui
from . import console_view
from . import constants
from . import pygame_utils

__all__ = [
    'main_gui',
    'console_view',
    'constants',
    'pygame_utils'
]
