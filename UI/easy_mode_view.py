"""
Easy mode view for the Hangman game.
Features: 7 max errors, 3 fake hints (letters NOT in word), letters used display,
7s delay on victory audio before showing menu.
"""

import pygame
import sys
import os
import random
import string

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import game_engine
from utils import word_manager
from utils import language_manager
from UI import constants
from UI import pygame_utils


# Module-level variables for resources
img_bg = None

# UI Rects
btn_pause_rect = pygame.Rect(20, 20, 120, 40)
HINT_CENTER = (constants.WIDTH - 80, constants.HEIGHT - 80)
HINT_RADIUS = 40


def load_resources():
    """Load resources for easy mode."""
    global img_bg

    try:
        bg_path = os.path.join("assets", "images", "facile.jpg")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
            img_bg.fill((100, 149, 237))

        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))


def initialize_game():
    """Initialize a new game."""
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    if os.path.exists(constants.AUDIO_EASY_MODE):
        try:
            pygame.mixer.music.load(constants.AUDIO_EASY_MODE)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error loading easy mode music: {e}")

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "facile")
    if not secret_word:
        secret_word = "FACILE"

    game_state = game_engine.create_game(secret_word, 7)
    hints_left = 3

    return game_state, secret_word, hints_left


def use_fake_hint(state, secret):
    """Reveals a letter that is NOT in the word (helps by elimination)."""
    alphabet = list(string.ascii_lowercase)
    word_letters = set(secret.lower())
    played_letters = set(state["letters_played"])

    available_fakes = []
    for l in alphabet:
        if l not in word_letters and l not in played_letters:
            available_fakes.append(l)

    if available_fakes:
        letter = random.choice(available_fakes)
        game_engine.play_letter(state, letter)
        return True
    return False


def draw_hangman(screen, errors):
    """Draws a larger and bolder hangman in black using pygame.draw."""
    color = (0, 0, 0) # Noir
    # Coordonnées ajustées pour un dessin plus grand
    bx = constants.WIDTH // 2 - 120
    by = constants.HEIGHT // 2 - 160

    # Épaisseurs augmentées
    thick_struct = 8
    thick_man = 5

    # 1. Socle
    if errors >= 1:
        pygame.draw.line(screen, color, (bx - 20, by + 250), (bx + 220, by + 250), thick_struct)
    # 2. Poteau vertical
    if errors >= 2:
        pygame.draw.line(screen, color, (bx + 40, by + 250), (bx + 40, by - 20), thick_struct)
    # 3. Traverse horizontale et renfort
    if errors >= 3:
        pygame.draw.line(screen, color, (bx + 40, by - 20), (bx + 160, by - 20), thick_struct)
        pygame.draw.line(screen, color, (bx + 40, by + 30), (bx + 90, by - 20), thick_struct)
    # 4. Corde et Tête
    if errors >= 4:
        pygame.draw.line(screen, color, (bx + 160, by - 20), (bx + 160, by + 20), thick_man)
        pygame.draw.circle(screen, color, (bx + 160, by + 45), 25, thick_man)
    # 5. Corps (Buste)
    if errors >= 5:
        pygame.draw.line(screen, color, (bx + 160, by + 70), (bx + 160, by + 150), thick_man)
    # 6. Bras
    if errors >= 6:
        pygame.draw.line(screen, color, (bx + 160, by + 90), (bx + 120, by + 130), thick_man)
        pygame.draw.line(screen, color, (bx + 160, by + 90), (bx + 200, by + 130), thick_man)
    # 7. Jambes
    if errors >= 7:
        pygame.draw.line(screen, color, (bx + 160, by + 150), (bx + 120, by + 210), thick_man)
        pygame.draw.line(screen, color, (bx + 160, by + 150), (bx + 200, by + 210), thick_man)


def play_win_sequence(screen, fonts, secret_word):
    """Win: Fade black, background penduewin.jpg, wait 7s of victoire.ogg."""
    pygame.mixer.music.stop()

    win_bg_path = os.path.join("assets", "images", "penduewin.jpg")
    current_bg = img_bg
    if os.path.exists(win_bg_path):
        current_bg = pygame.transform.scale(pygame.image.load(win_bg_path).convert(), (constants.WIDTH, constants.HEIGHT))

    if os.path.exists(constants.AUDIO_VICTORY):
        pygame.mixer.music.load(constants.AUDIO_VICTORY)
        pygame.mixer.music.play()

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 180, 5):
        screen.blit(current_bg, (0, 0))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

    pygame.time.delay(7000)

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(current_bg, (0, 0))
        screen.blit(fade, (0, 0))

        msg = fonts["word"].render(language_manager.get_text("victory"), True, constants.GREEN)
        word_was_text = language_manager.get_text("word_was") + " " + secret_word
        msg2 = fonts["info"].render(word_was_text, True, constants.WHITE)
        screen.blit(msg, msg.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40)))
        screen.blit(msg2, msg2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 20)))

        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("replay"), fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_quit, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("quit"), fonts["button"])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    return "restart"
                if rect_quit.collidepoint(event.pos):
                    return "main_menu"


def play_lose_sequence(screen, fonts, secret_word):
    """Loss: Black fade, original bg visible, Game Over + Tip."""
    pygame.mixer.music.stop()
    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(img_bg, (0, 0))
        fade.set_alpha(200)
        screen.blit(fade, (0, 0))

        t1 = fonts["word"].render(language_manager.get_text("game_over"), True, constants.RED)
        word_was_text = language_manager.get_text("word_was") + " " + secret_word
        t2 = fonts["info"].render(word_was_text, True, constants.WHITE)
        tip = fonts["small"].render(language_manager.get_text("tip_easy"), True, constants.GOLD)

        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 20)))
        screen.blit(tip, tip.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 40)))

        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("retry"), fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_back, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("menu"), fonts["button"])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    return "restart"
                if rect_back.collidepoint(event.pos):
                    return "main_menu"


def draw_interface(screen, fonts, state, secret, hints, mouse_pos):
    """Draw game UI."""
    screen.blit(img_bg, (0, 0))

    pygame_utils.draw_button_with_border(screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, language_manager.get_text("pause"), fonts["button"])

    # Remplacement des images par le dessin dynamique
    draw_hangman(screen, state["errors"])

    masked = game_engine.get_masked_word(state)
    surf_mot = fonts["word"].render(" ".join(masked), True, constants.WHITE)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 200))

    used_letters = ", ".join(state["letters_played"]).upper()
    used_label = language_manager.get_text("letters_used")
    txt_used = fonts["small"].render(used_label + " " + used_letters, True, constants.WHITE)
    screen.blit(txt_used, (20, constants.HEIGHT - 40))

    dist = ((mouse_pos[0] - HINT_CENTER[0]) ** 2 + (mouse_pos[1] - HINT_CENTER[1]) ** 2) ** 0.5
    color = constants.GOLD if dist < HINT_RADIUS else constants.DARK_BLUE
    pygame.draw.circle(screen, color, HINT_CENTER, HINT_RADIUS)
    pygame.draw.circle(screen, constants.WHITE, HINT_CENTER, HINT_RADIUS, 2)

    hint_label = language_manager.get_text("hint")
    txt_hint = fonts["small"].render(hint_label + " (" + str(hints) + ")", True, constants.WHITE)
    screen.blit(txt_hint, txt_hint.get_rect(center=HINT_CENTER))


def run_view(screen, fonts, clock):
    """
    Main entry point for easy mode view.
    """
    load_resources()
    game_state, secret_word, hints = initialize_game()
    paused = False

    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(constants.WIDTH // 2 - 280, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(constants.WIDTH // 2 - 90, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 100, constants.HEIGHT // 2 + 20, w_b, h_b)

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

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
                        game_state, secret_word, hints = initialize_game()
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        pygame.mixer.music.stop()
                        return "main_menu"

                dist = ((event.pos[0] - HINT_CENTER[0]) ** 2 + (event.pos[1] - HINT_CENTER[1]) ** 2) ** 0.5
                if dist < HINT_RADIUS and not paused and hints > 0 and game_state["status"] == "in_progress":
                    pygame_utils.play_click_sound()
                    if use_fake_hint(game_state, secret_word):
                        hints -= 1

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    game_engine.play_letter(game_state, letter)

        if game_state["status"] == "won":
            result = play_win_sequence(screen, fonts, secret_word)
            if result == "restart":
                game_state, secret_word, hints = initialize_game()
            elif result == "main_menu":
                return "main_menu"
            elif result == "quit":
                return None

        elif game_state["status"] == "lost" or game_state["errors"] >= 7:
            result = play_lose_sequence(screen, fonts, secret_word)
            if result == "restart":
                game_state, secret_word, hints = initialize_game()
            elif result == "main_menu":
                return "main_menu"
            elif result == "quit":
                return None

        if not paused:
            draw_interface(screen, fonts, game_state, secret_word, hints, mouse_pos)
        else:
            draw_interface(screen, fonts, game_state, secret_word, hints, mouse_pos)
            overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            txt = fonts["word"].render(language_manager.get_text("pause"), True, constants.GOLD)
            screen.blit(txt, txt.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40)))

            pygame_utils.draw_button_with_border(screen, rect_cont, constants.GREEN, constants.GREEN_HOVER, mouse_pos, language_manager.get_text("continue"), fonts["button"])
            pygame_utils.draw_button_with_border(screen, rect_reset, constants.ORANGE, constants.ORANGE_HOVER, mouse_pos, language_manager.get_text("restart"), fonts["button"])
            pygame_utils.draw_button_with_border(screen, rect_quit, constants.RED, constants.RED_HOVER, mouse_pos, language_manager.get_text("quit"), fonts["button"])

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    fonts = pygame_utils.create_fonts()
    pygame_utils.load_sounds()
    clock = pygame.time.Clock()
    run_view(screen, fonts, clock)
    pygame.quit()