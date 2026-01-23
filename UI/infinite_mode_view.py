"""
Mode Infinite - Hangman
Features: 5 max errors, multiple small daemon.png display, infinite.png background, 
infinite.mp3 music, lose_infinite.mp3 on loss, multi-difficulty words.
No hints, no win screen (auto-restart on word found).
"""

import pygame
import sys
import os
import random
import subprocess
import string

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import game_engine
from utils import word_manager
from utils import language_manager
from UI import constants
from UI import pygame_utils

# Global variables
screen = None
img_bg = None
img_daemon = None
fonts = {}

# UI Rects
btn_pause_rect = pygame.Rect(20, 20, 120, 40)

def initialize_pygame():
    """Initialize pygame and load resources."""
    global screen, img_bg, img_daemon, fonts

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Pendu - Mode Infinite")

    fonts = pygame_utils.create_fonts()
    pygame_utils.load_sounds()

    try:
        # Background infinite.png
        bg_path = os.path.join("assets", "images", "infinite.png")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
            img_bg.fill((20, 20, 20))
        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
        
        # Daemon image - Taille réduite à 150x150
        daemon_path = os.path.join("assets", "images", "daemon.png")
        if os.path.exists(daemon_path):
            img_daemon = pygame.image.load(daemon_path).convert_alpha()
            img_daemon = pygame.transform.scale(img_daemon, (150, 150))
    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))

def initialize_game():
    """Initialize a new game with words from all difficulties."""
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    # Musique infinite.mp3
    music_path = os.path.join("assets", "audios", "infinite.mp3")
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        except:
            pass

    current_lang = language_manager.get_current_language()
    
    # Sélection aléatoire parmi les trois listes
    difficulties = ["facile", "moyen", "difficile"]
    chosen_diff = random.choice(difficulties)
    secret_word = word_manager.get_word(current_lang, chosen_diff)
    
    if not secret_word:
        secret_word = "INFINITE"

    # 5 erreurs max
    game_state = game_engine.create_game(secret_word, 5)
    
    return game_state, secret_word

def return_to_main_menu():
    """Quits and returns to main.py."""
    pygame.mixer.music.stop()
    pygame.quit()
    main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    subprocess.Popen([sys.executable, main_path if os.path.exists(main_path) else "main.py"])
    sys.exit()

def play_lose_sequence(secret_word):
    """Loss: Overlay noir transparent + lose_infinite.mp3."""
    pygame.mixer.music.stop()
    
    loss_audio = os.path.join("assets", "audios", "lose_infinite.mp3")
    if os.path.exists(loss_audio):
        pygame.mixer.music.load(loss_audio)
        pygame.mixer.music.play()

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    fade.set_alpha(200)
    
    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(img_bg, (0, 0))
        screen.blit(fade, (0, 0))

        t1 = fonts["word"].render("GAME OVER", True, constants.RED)
        t2 = fonts["info"].render(f"Le mot était : {secret_word}", True, constants.WHITE)
        tip = fonts["small"].render("L'infini vous a consumé...", True, constants.GOLD)

        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 20)))
        screen.blit(tip, tip.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 40)))

        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, "REESSAYER", fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_back, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, "MENU", fonts["button"])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos): return "restart"
                if rect_back.collidepoint(event.pos): return_to_main_menu()

def draw_interface(state, secret, mouse_pos):
    """Draw game UI."""
    screen.blit(img_bg, (0, 0))

    # Pause Button
    pygame_utils.draw_button_with_border(screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, "PAUSE", fonts["button"])

    # Affichage des Daemons : une copie apparaît par erreur de gauche à droite
    if img_daemon:
        spacing = 160 # Espace entre chaque daemon
        start_x = (constants.WIDTH - (state["errors"] * spacing)) // 2
        for i in range(state["errors"]):
            screen.blit(img_daemon, (start_x + (i * spacing), 150))

    # Word
    masked = game_engine.get_masked_word(state)
    surf_mot = fonts["word"].render(" ".join(masked), True, constants.WHITE)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 200))

    # Affichage des lettres utilisées
    used_letters = ", ".join(state["letters_played"]).upper()
    txt_used = fonts["small"].render(f"Utilisées: {used_letters}", True, constants.WHITE)
    screen.blit(txt_used, (20, constants.HEIGHT - 40))

def main():
    initialize_pygame()
    game_state, secret_word = initialize_game()
    clock = pygame.time.Clock()
    paused = False

    # Pause menu buttons
    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(constants.WIDTH // 2 - 280, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(constants.WIDTH // 2 - 90, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 100, constants.HEIGHT // 2 + 20, w_b, h_b)

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause_rect.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        paused = False
                    if rect_reset.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        game_state, secret_word = initialize_game()
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        return_to_main_menu()

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    game_engine.play_letter(game_state, letter)

        # Check Win/Loss
        if game_state["status"] == "won":
            game_state, secret_word = initialize_game()
            
        elif game_state["status"] == "loss" or game_state["errors"] >= 5:
            if play_lose_sequence(secret_word) == "restart":
                game_state, secret_word = initialize_game()

        # Render
        if not paused:
            draw_interface(game_state, secret_word, mouse_pos)
        else:
            overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            txt = fonts["word"].render("PAUSE", True, constants.GOLD)
            screen.blit(txt, txt.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40)))

            pygame_utils.draw_button_with_border(screen, rect_cont, constants.GREEN, constants.GREEN_HOVER, mouse_pos, "CONTINUER", fonts["button"])
            pygame_utils.draw_button_with_border(screen, rect_reset, constants.ORANGE, constants.ORANGE_HOVER, mouse_pos, "RECOMMENCER", fonts["button"])
            pygame_utils.draw_button_with_border(screen, rect_quit, constants.RED, constants.RED_HOVER, mouse_pos, "QUITTER", fonts["button"])

        pygame.display.flip()

if __name__ == "__main__":
    main()