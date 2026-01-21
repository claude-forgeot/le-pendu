"""
Point d'entrée principal du jeu du Pendu
Permet de lancer soit l'interface graphique (Pygame) soit l'interface console (CLI)
"""
import os
import sys

# Ajout du répertoire courant au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import des modules
from controllers import game_controller
from UI import main_gui

if __name__ == "__main__":
    print(f"sys.argv: {sys.argv}")

    # Vérification de l'argument en ligne de commande pour lancer la version CLI
    if "--cli" in sys.argv:
        game_controller.start_game()
    else:
        # Lancement de l'interface graphique Pygame
        main_gui()
