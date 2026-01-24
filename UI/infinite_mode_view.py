# Infinite mode: 5 errors, daemon sprites, cumulative score, auto-restart on win

import pygame
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import game_engine
from utils import word_manager
from utils import language_manager
from utils import score_manager
from UI import constants
from UI import pygame_utils

# Module-level variables
img_bg = None
img_daemon = None
current_total_score = 0

# UI Rects
btn_pause_rect = pygame.Rect(20, 20, 120, 40)


# Load infinite background and daemon sprite images
def load_resources():
    global img_bg, img_daemon

    try:
        bg_path = os.path.join("assets", "images", "infinite.png")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
            img_bg.fill((20, 20, 20))
        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))

        daemon_path = os.path.join("assets", "images", "daemon.png")
        if os.path.exists(daemon_path):
            img_daemon = pygame.image.load(daemon_path).convert_alpha()
            img_daemon = pygame.transform.scale(img_daemon, (150, 150))
    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))


# Reset game state with random difficulty word, optionally reset cumulative score
def initialize_game(reset_score=False):
    global current_total_score
    if reset_score:
        current_total_score = 0

    pygame.mixer.music.stop()
    pygame.mixer.stop()

    if os.path.exists(constants.AUDIO_INFINITE_MODE):
        try:
            pygame.mixer.music.load(constants.AUDIO_INFINITE_MODE)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error loading infinite mode music: {e}")

    current_lang = language_manager.get_current_language()

    difficulties = ["facile", "moyen", "difficile"]
    chosen_diff = random.choice(difficulties)
    secret_word = word_manager.get_word(current_lang, chosen_diff)

    if not secret_word:
        secret_word = "INFINITE"

    game_state = game_engine.create_game(secret_word, 5)

    return game_state, secret_word


# Capture 5-char player name for highscore entry, save to infinite category
def get_name_input(screen, fonts, final_score):
    name = ""
    while True:
        screen.fill((0, 0, 0))
        prompt = fonts["info"].render(language_manager.get_text("new_record"), True, constants.GOLD)
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        name_surf = fonts["word"].render(name + cursor, True, constants.WHITE)
        instr = fonts["small"].render(language_manager.get_text("press_enter"), True, constants.WHITE)

        screen.blit(prompt, prompt.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 50)))
        screen.blit(name_surf, name_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 20)))
        screen.blit(instr, instr.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 80)))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    score_manager.save_score(name, final_score, category="infinite")
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 5 and event.unicode.isalpha():
                    name += event.unicode.upper()


# Display game over with total score, check highscore, show retry/menu buttons
def play_lose_sequence(screen, fonts, secret_word):
    global current_total_score
    pygame.mixer.music.stop()

    if os.path.exists(constants.AUDIO_LOSE_INFINITE):
        pygame.mixer.music.load(constants.AUDIO_LOSE_INFINITE)
        pygame.mixer.music.play()

    if score_manager.check_if_highscore(current_total_score, category="infinite"):
        result = get_name_input(screen, fonts, current_total_score)
        if result is None:
            return "quit"

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    fade.set_alpha(200)

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(img_bg, (0, 0))
        screen.blit(fade, (0, 0))

        t1 = fonts["word"].render(language_manager.get_text("game_over"), True, constants.RED)
        score_text = language_manager.get_text("total_score") + " " + str(current_total_score)
        t_score = fonts["info"].render(score_text, True, constants.GOLD)
        word_was_text = language_manager.get_text("word_was") + " " + secret_word
        t2 = fonts["info"].render(word_was_text, True, constants.WHITE)
        tip = fonts["small"].render(language_manager.get_text("tip_infinite"), True, constants.GOLD)

        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 100)))
        screen.blit(t_score, t_score.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 10)))
        screen.blit(tip, tip.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 60)))

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


# Render background, score, daemon sprites for errors, masked word and letters
def draw_interface(screen, fonts, state, secret, mouse_pos):
    global current_total_score
    screen.blit(img_bg, (0, 0))

    pygame_utils.draw_button_with_border(screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, language_manager.get_text("pause"), fonts["button"])

    score_surf = fonts["info"].render("Score: " + str(current_total_score), True, constants.GOLD)
    screen.blit(score_surf, (constants.WIDTH - 200, 20))

    if img_daemon:
        spacing = 160
        start_x = (constants.WIDTH - (state["errors"] * spacing)) // 2
        for i in range(state["errors"]):
            screen.blit(img_daemon, (start_x + (i * spacing), 150))

    masked = game_engine.get_masked_word(state)
    surf_mot = pygame_utils.render_word_adaptive(masked, constants.WIDTH - 40)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 200))

    used_letters = ", ".join(state["letters_played"]).upper()
    used_label = language_manager.get_text("letters_used")
    txt_used = fonts["small"].render(used_label + " " + used_letters, True, constants.WHITE)
    screen.blit(txt_used, (20, constants.HEIGHT - 40))


# Main game loop with auto-restart on win, cumulative scoring
def run_view(screen, fonts, clock):
    global current_total_score
    load_resources()
    game_state, secret_word = initialize_game(reset_score=True)
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
                        game_state, secret_word = initialize_game(reset_score=True)
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        pygame.mixer.music.stop()
                        return "main_menu"

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    game_engine.play_letter(game_state, letter)

        if game_state["status"] == "won":
            word_score = score_manager.calculate_score(game_state)
            current_total_score += word_score
            game_state, secret_word = initialize_game()

        elif game_state["status"] == "lost" or game_state["errors"] >= 5:
            result = play_lose_sequence(screen, fonts, secret_word)
            if result == "restart":
                game_state, secret_word = initialize_game(reset_score=True)
            elif result == "main_menu":
                return "main_menu"
            elif result == "quit":
                return None

        if not paused:
            draw_interface(screen, fonts, game_state, secret_word, mouse_pos)
        else:
            draw_interface(screen, fonts, game_state, secret_word, mouse_pos)
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
