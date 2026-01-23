"""
Easy mode view for the Hangman game.
Features: 7 max errors, 3 fake hints, Large BLACK Vector Hangman,
7s delay on victory audio before showing menu.
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
fonts = {}

# UI Rects
btn_pause_rect = pygame.Rect(20, 20, 120, 40)
HINT_CENTER = (constants.WIDTH - 80, constants.HEIGHT - 80)
HINT_RADIUS = 40

def draw_vector_hangman(surface, errors):
    """Draws a LARGE BLACK hangman using geometric shapes."""
    color = (0, 0, 0) # NOIR
    width = 8        # Épaisseur
    # Coordonnées pour une grande taille
    start_x, start_y = constants.WIDTH // 2 - 80, 400
    
    if errors >= 1:
        # Potence
        pygame.draw.line(surface, color, (start_x - 80, start_y), (start_x + 80, start_y), width) # Base
        pygame.draw.line(surface, color, (start_x, start_y), (start_x, start_y - 300), width)    # Poteau
        pygame.draw.line(surface, color, (start_x, start_y - 300), (start_x + 140, start_y - 300), width) # Barre haute
        pygame.draw.line(surface, color, (start_x + 140, start_y - 300), (start_x + 140, start_y - 260), width) # Corde

    if errors >= 2: # Tête
        pygame.draw.circle(surface, color, (start_x + 140, start_y - 235), 25, width)
    
    if errors >= 3: # Corps
        pygame.draw.line(surface, color, (start_x + 140, start_y - 210), (start_x + 140, start_y - 100), width)
        
    if errors >= 4: # Bras gauche
        pygame.draw.line(surface, color, (start_x + 140, start_y - 190), (start_x + 100, start_y - 140), width)
        
    if errors >= 5: # Bras droit
        pygame.draw.line(surface, color, (start_x + 140, start_y - 190), (start_x + 180, start_y - 140), width)
        
    if errors >= 6: # Jambe gauche
        pygame.draw.line(surface, color, (start_x + 140, start_y - 100), (start_x + 100, start_y - 30), width)
        
    if errors >= 7: # Jambe droite
        pygame.draw.line(surface, color, (start_x + 140, start_y - 100), (start_x + 180, start_y - 30), width)

def initialize_pygame():
    global screen, img_bg, fonts
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Pendu - Mode Facile")
    fonts = pygame_utils.create_fonts()
    pygame_utils.load_sounds()

    try:
        bg_path = os.path.join("assets", "images", "facile.jpg")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
            img_bg.fill((100, 149, 237))
        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
    except:
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))

def initialize_game():
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    music_path = os.path.join("assets", "audios", "facile.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "facile")
    if not secret_word: secret_word = "FACILE"

    game_state = game_engine.create_game(secret_word, 7)
    return game_state, secret_word, 3

def return_to_main_menu():
    pygame.mixer.music.stop()
    pygame.quit()
    main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    subprocess.Popen([sys.executable, main_path if os.path.exists(main_path) else "main.py"])
    sys.exit()

def use_fake_hint(state, secret):
    alphabet = list(string.ascii_lowercase)
    word_letters = set(secret.lower())
    played_letters = set(state["letters_played"])
    available_fakes = [l for l in alphabet if l not in word_letters and l not in played_letters]
    if available_fakes:
        letter = random.choice(available_fakes)
        game_engine.play_letter(state, letter)
        return True
    return False

def play_win_sequence(secret_word):
    pygame.mixer.music.stop()
    win_bg_path = os.path.join("assets", "images", "penduewin.jpg")
    current_bg = img_bg
    if os.path.exists(win_bg_path):
        current_bg = pygame.transform.scale(pygame.image.load(win_bg_path).convert(), (constants.WIDTH, constants.HEIGHT))

    audio_path = os.path.join("assets", "audios", "victoire.mp3")
    if os.path.exists(audio_path):
        pygame.mixer.music.load(audio_path); pygame.mixer.music.play()

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 180, 5): 
        screen.blit(current_bg, (0, 0))
        fade.set_alpha(alpha); screen.blit(fade, (0, 0))
        pygame.display.flip(); pygame.time.delay(10)

    pygame.time.delay(7000)
    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(current_bg, (0, 0)); screen.blit(fade, (0, 0))
        msg = fonts["word"].render("VICTOIRE !", True, constants.GREEN)
        msg2 = fonts["info"].render(f"Le mot était : {secret_word}", True, constants.WHITE)
        screen.blit(msg, msg.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40)))
        screen.blit(msg2, msg2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 20)))
        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, "REJOUER", fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_quit, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, "QUITTER", fonts["button"])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos): return "restart"
                if rect_quit.collidepoint(event.pos): return_to_main_menu()

def play_lose_sequence(secret_word):
    pygame.mixer.music.stop()
    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT)); fade.fill((0, 0, 0))
    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(img_bg, (0, 0)); fade.set_alpha(200); screen.blit(fade, (0, 0))
        t1 = fonts["word"].render("GAME OVER", True, constants.RED)
        t2 = fonts["info"].render(f"Le mot était : {secret_word}", True, constants.WHITE)
        tip = fonts["small"].render("Astuce : Au pendu, il ne faut jamais perdre la tête...", True, constants.GOLD)
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

def draw_interface(state, secret, hints, mouse_pos):
    screen.blit(img_bg, (0, 0))
    pygame_utils.draw_button_with_border(screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, "PAUSE", fonts["button"])
    
    # DESSIN DU PENDU NOIR
    draw_vector_hangman(screen, state["errors"])

    masked = game_engine.get_masked_word(state)
    surf_mot = fonts["word"].render(" ".join(masked), True, constants.WHITE)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 150))

    used_letters = ", ".join(state["letters_played"]).upper()
    txt_used = fonts["small"].render(f"Utilisées: {used_letters}", True, constants.WHITE)
    screen.blit(txt_used, (20, constants.HEIGHT - 40))

    dist = ((mouse_pos[0]-HINT_CENTER[0])**2 + (mouse_pos[1]-HINT_CENTER[1])**2)**0.5
    color = constants.GOLD if dist < HINT_RADIUS else constants.DARK_BLUE
    pygame.draw.circle(screen, color, HINT_CENTER, HINT_RADIUS)
    pygame.draw.circle(screen, constants.WHITE, HINT_CENTER, HINT_RADIUS, 2)
    txt_hint = fonts["small"].render(f"INDICE ({hints})", True, constants.WHITE)
    screen.blit(txt_hint, txt_hint.get_rect(center=HINT_CENTER))

def main():
    initialize_pygame()
    game_state, secret_word, hints = initialize_game()
    clock = pygame.time.Clock()
    paused = False

    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(constants.WIDTH // 2 - 280, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(constants.WIDTH // 2 - 90, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 100, constants.HEIGHT // 2 + 20, w_b, h_b)

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause_rect.collidepoint(event.pos):
                    pygame_utils.play_click_sound(); paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos): pygame_utils.play_click_sound(); paused = False
                    if rect_reset.collidepoint(event.pos):
                        pygame_utils.play_click_sound(); game_state, secret_word, hints = initialize_game(); paused = False
                    if rect_quit.collidepoint(event.pos): pygame_utils.play_click_sound(); return_to_main_menu()
                if not paused:
                    dist = ((event.pos[0]-HINT_CENTER[0])**2 + (event.pos[1]-HINT_CENTER[1])**2)**0.5
                    if dist < HINT_RADIUS and hints > 0 and game_state["status"] == "in_progress":
                        pygame_utils.play_click_sound()
                        if use_fake_hint(game_state, secret_word): hints -= 1

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    game_engine.play_letter(game_state, letter)

        if game_state["status"] == "won":
            if play_win_sequence(secret_word) == "restart": game_state, secret_word, hints = initialize_game()
        elif game_state["status"] == "loss" or game_state["errors"] >= 7:
            if play_lose_sequence(secret_word) == "restart": game_state, secret_word, hints = initialize_game()

        if not paused:
            draw_interface(game_state, secret_word, hints, mouse_pos)
        else:
            overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            txt_pause = fonts["word"].render("PAUSE", True, constants.GOLD)
            screen.blit(txt_pause, txt_pause.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 60)))
            for r, label in [(rect_cont, "CONTINUER"), (rect_reset, "RECOMMENCER"), (rect_quit, "QUITTER")]:
                pygame_utils.draw_button_with_border(screen, r, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, label, fonts["button"])

        pygame.display.flip()

if __name__ == "__main__":
    main()