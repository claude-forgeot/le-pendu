"""
Module UI - Interfaces utilisateur pour le jeu du Pendu
Contient les vues graphique (Pygame) et console (CLI)
"""

# Import des fonctions principales des vues
from .graphic_view import main_gui, draw_rounded_button
from . import console_view

# Exports explicites
__all__ = [
    'main_gui',
    'draw_rounded_button',
    'console_view'
]
