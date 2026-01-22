# UI/hard_mode_view.py

"""
Hard mode view for the Hangman game.
Features: 30s timer, 5 max errors, video on loss.
Run with: python -m UI.hard_mode_view [US]
"""

import pygame
import sys
import os
import cv2
import random
import subprocess

from models import game_engine
from utils import word_manager
from utils import language_manager


# Screen dimensions
WIDTH, HEIGHT = 900, 600

# Colors
WHITE = (255, 255, 255)
RED = (231, 76, 60)
GOLD = (241, 196, 15)
GREEN = (46, 204, 113)
DARK_BLUE = (44, 62, 80)
DARK_BLUE_H = (52, 73, 94)
BLACK_OVERLAY = (0, 0, 0, 180)

# Global variables for pygame objects
screen = None
img_bg = None
imgs = {}
sound_click = None
music_game_path = ""
video_path = ""
audio_lose = ""

# Fonts
font_mot = None
font_info = None
font_btn = None
font_timer = None
font_fausses = None

# Pause button rect
btn_pause_rect = pygame.Rect(20, 20, 120, 40)


def initialize_pygame():
    """Initialize pygame and load resources."""
    global screen, img_bg, imgs, sound_click, music_game_path, video_path, audio_lose
    global font_mot, font_info, font_btn, font_timer, font_fausses

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    title = language_manager.get_text("hard_mode_title")
    pygame.display.set_caption(title)

    # Fonts
    font_mot = pygame.font.SysFont("Arial", 60, bold=True)
    font_info = pygame.font.SysFont("Arial", 30, bold=True)
    font_btn = pygame.font.SysFont("Arial", 20, bold=True)
    font_timer = pygame.font.SysFont("Consolas", 60, bold=True)
    font_fausses = pygame.font.SysFont("Arial", 20, bold=True)

    # Resource paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")

    # Load resources
    SIZE = 100
    try:
        path_bg = os.path.join(assets_dir, "images", "pendue.png")
        img_bg = pygame.image.load(path_bg).convert()
        img_bg = pygame.transform.scale(img_bg, (WIDTH, HEIGHT))

        imgs = {
            1: pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "images", "tete.png")), (SIZE, SIZE)),
            2: pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "images", "bras_droit.png")), (SIZE, SIZE)),
            3: pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "images", "bras_gauche.png")), (SIZE, SIZE)),
            4: pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "images", "jambe_droite.png")), (SIZE, SIZE)),
            5: pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "images", "jambe_gauche.png")), (SIZE, SIZE)),
        }

        music_game_path = os.path.join(assets_dir, "audios", "difficile.mp3")
        video_path = os.path.join(assets_dir, "vidéo", "losehard.mp4")
        audio_lose = os.path.join(assets_dir, "audios", "losehard.mp3")
        sound_click = pygame.mixer.Sound(os.path.join(assets_dir, "audios", "click.mp3"))

    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((WIDTH, HEIGHT))
        img_bg.fill((40, 40, 40))
        imgs = {}
        sound_click = None


def play_click_sound():
    """Play click sound effect."""
    if sound_click:
        sound_click.play()


def return_to_menu():
    """Return to the main menu."""
    play_click_sound()
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.quit()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    menu_path = os.path.join(base_dir, "UI", "graphic_view.py")
    subprocess.Popen([sys.executable, menu_path])
    sys.exit()


def initialize_game():
    """Initialize a new game with a random word."""
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    if os.path.exists(music_game_path):
        pygame.mixer.music.load(music_game_path)
        pygame.mixer.music.play(-1)

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "difficile")
    if not secret_word:
        secret_word = "PYTHON"

    game_state = game_engine.create_game(secret_word, 5)
    timer = 30.0

    return game_state, secret_word, timer


def play_lose_sequence(secret_word, state):
    """Play the loss sequence with video."""
    draw_interface(state, secret_word, 0, pygame.mouse.get_pos())
    pygame.display.flip()
    pygame.time.delay(600)
    pygame.mixer.music.stop()

    # Fade to black
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 15):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)
        pygame.event.pump()

    # Play video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    cap.set(cv2.CAP_PROP_POS_MSEC, 30000)

    if os.path.exists(audio_lose):
        pygame.mixer.music.load(audio_lose)
        pygame.mixer.music.play(start=30.0)

    clock = pygame.time.Clock()
    last_frame_surf = None

    while cap.isOpened():
        if cap.get(cv2.CAP_PROP_POS_MSEC) >= 44000:
            break
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        last_frame_surf = pygame.surfarray.make_surface(frame)
        screen.blit(last_frame_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
        pygame.event.pump()

    cap.release()
    pygame.mixer.music.stop()

    # Show game over screen
    rect_retry = pygame.Rect(WIDTH // 2 - 210, HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(WIDTH // 2 + 10, HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()

        if last_frame_surf:
            screen.blit(last_frame_surf, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(BLACK_OVERLAY)
        screen.blit(overlay, (0, 0))

        # Loss text
        loss_text = language_manager.get_text("hard_loss")
        t1 = font_mot.render(loss_text, True, RED)
        t2 = font_info.render(f"{secret_word}", True, WHITE)
        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        # Buttons
        retry_text = language_manager.get_text("hard_retry")
        quit_text = language_manager.get_text("hard_quit")

        for rect, label in [(rect_retry, retry_text), (rect_back, quit_text)]:
            over = rect.collidepoint(m_pos)
            if over:
                pygame.draw.rect(screen, GOLD, rect.inflate(6, 6), border_radius=12)
            pygame.draw.rect(screen, DARK_BLUE_H if over else DARK_BLUE, rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
            txt_surf = font_btn.render(label, True, WHITE)
            screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    play_click_sound()
                    return "restart"
                if rect_back.collidepoint(event.pos):
                    return_to_menu()


def draw_interface(state, secret, timer, mouse_pos):
    """Draw the game interface."""
    screen.blit(img_bg, (0, 0))

    # Pause button
    over_p = btn_pause_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, DARK_BLUE_H if over_p else DARK_BLUE, btn_pause_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, btn_pause_rect, 2, border_radius=10)
    pause_text = language_manager.get_text("hard_pause")
    txt_p = font_btn.render(pause_text, True, WHITE)
    screen.blit(txt_p, txt_p.get_rect(center=btn_pause_rect.center))

    # Timer
    timer_val = max(0, int(timer))
    timer_color = RED if timer < 10 else WHITE
    surf_timer = font_timer.render(f"{timer_val}s", True, timer_color)
    timer_rect = surf_timer.get_rect(center=(WIDTH // 2, 50))
    if timer < 5 and timer > 0:
        timer_rect.x += random.randint(-3, 3)
        timer_rect.y += random.randint(-3, 3)
    screen.blit(surf_timer, timer_rect)

    # Hangman parts
    SIZE = 100
    tx, ty = WIDTH // 2 - SIZE // 2, 130
    pos = {
        1: (tx, ty),
        2: (tx - SIZE, ty + SIZE),
        3: (tx + SIZE, ty + SIZE),
        4: (tx - SIZE // 2, ty + 2 * SIZE),
        5: (tx + SIZE // 2, ty + 2 * SIZE)
    }
    for i in range(1, state["errors"] + 1):
        if i in imgs:
            screen.blit(imgs[i], pos[i])

    # Masked word
    masked = game_engine.get_masked_word(state)
    surf_mot = font_mot.render(" ".join(masked), True, WHITE)
    screen.blit(surf_mot, (WIDTH // 2 - surf_mot.get_width() // 2, HEIGHT - 180))

    # Wrong letters
    wrong_letters = [l for l in state["letters_played"] if l not in secret.lower()]
    errors_text = language_manager.get_text("hard_errors")
    screen.blit(font_fausses.render(errors_text, True, RED), (20, HEIGHT - 70))
    screen.blit(font_fausses.render(", ".join(wrong_letters).upper(), True, WHITE), (20, HEIGHT - 40))


def main():
    """Main game loop."""
    # Check for language argument
    if len(sys.argv) > 1 and sys.argv[1].upper() == "EN":
        language_manager.set_language("en")
    else:
        language_manager.set_language("fr")

    initialize_pygame()
    game_state, secret_word, timer = initialize_game()
    clock = pygame.time.Clock()
    paused = False

    # Pause menu buttons
    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(WIDTH // 2 - 280, HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 + 20, w_b, h_b)

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause_rect.collidepoint(event.pos):
                    play_click_sound()
                    paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos):
                        play_click_sound()
                        paused = False
                    if rect_reset.collidepoint(event.pos):
                        play_click_sound()
                        game_state, secret_word, timer = initialize_game()
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        return_to_menu()

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    old_err = game_state["errors"]
                    game_engine.play_letter(game_state, letter)
                    if game_state["errors"] == old_err:
                        timer += 5
                    else:
                        timer -= 5

                    if game_state["errors"] >= 5:
                        game_state["status"] = "loss"
                        if play_lose_sequence(secret_word, game_state) == "restart":
                            game_state, secret_word, timer = initialize_game()
                            continue

        # Timer countdown
        if game_state["status"] == "in_progress" and not paused:
            timer -= dt
            if timer <= 0:
                game_state["status"] = "loss"
                if play_lose_sequence(secret_word, game_state) == "restart":
                    game_state, secret_word, timer = initialize_game()

        # Win screen
        if game_state["status"] == "won":
            screen.fill((20, 40, 20))
            win_text = language_manager.get_text("hard_win")
            hint_text = language_manager.get_text("hard_hint")
            msg = font_info.render(f"{win_text} : {secret_word}", True, GREEN)
            msg2 = font_btn.render(hint_text, True, WHITE)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            screen.blit(msg2, msg2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    play_click_sound()
                    game_state, secret_word, timer = initialize_game()
            continue

        # Draw game interface
        draw_interface(game_state, secret_word, timer, mouse_pos)

        # Pause overlay
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(BLACK_OVERLAY)
            screen.blit(overlay, (0, 0))

            pause_title = language_manager.get_text("hard_pause")
            txt_pause = font_mot.render(pause_title, True, GOLD)
            screen.blit(txt_pause, txt_pause.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))

            cont_text = language_manager.get_text("hard_continue")
            reset_text = language_manager.get_text("hard_reset")
            quit_text = language_manager.get_text("hard_quit")

            for r, label in [(rect_cont, cont_text), (rect_reset, reset_text), (rect_quit, quit_text)]:
                over = r.collidepoint(mouse_pos)
                if over:
                    pygame.draw.rect(screen, GOLD, r.inflate(6, 6), border_radius=12)
                pygame.draw.rect(screen, DARK_BLUE_H if over else DARK_BLUE, r, border_radius=10)
                pygame.draw.rect(screen, WHITE, r, 2, border_radius=10)
                t_surf = font_btn.render(label, True, WHITE)
                screen.blit(t_surf, t_surf.get_rect(center=r.center))

        pygame.display.flip()


if __name__ == "__main__":
    main()
