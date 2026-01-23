"""
normal mode view for the Hangman game.
Features: 30s timer, 7 max errors, macron video (12s-17s) on loss.
Win: winnormal.png background, 7s delay on victory audio, Score & Highscore (Normal Category).
Run with: python -m UI.hard_mode_view [EN]
"""

import pygame
import sys
import os
import cv2
import random
import subprocess

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import game_engine
from utils import word_manager, language_manager, score_manager
from UI import constants
from UI import pygame_utils


# Global variables for pygame objects
screen = None
img_bg = None
imgs = {}
fonts = {}

# Pause button rect
btn_pause_rect = pygame.Rect(20, 20, 120, 40)


def initialize_pygame():
    """Initialize pygame and load resources."""
    global screen, img_bg, imgs, fonts

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    title = language_manager.get_text("hard_mode_title")
    pygame.display.set_caption(title)

    fonts = pygame_utils.create_fonts()
    pygame_utils.load_sounds()

    try:
        bg_path = os.path.join("assets", "images", "normal.png")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.image.load(constants.IMG_BACKGROUND_GAME).convert()
            
        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
        
        imgs = {}
        for i in range(1, 8):
            path = os.path.join("assets", "images", f"hangman_{i}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                imgs[i] = pygame.transform.scale(img, (300, 300))
    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        img_bg.fill((40, 40, 40))
        imgs = {}


def initialize_game():
    """Initialize a new game with a random word."""
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    normal_audio = os.path.join("assets", "audios", "normal.mp3")
    if os.path.exists(normal_audio):
        try:
            pygame.mixer.music.load(normal_audio)
            pygame.mixer.music.play(-1, start=5.0)
        except Exception as e:
            print(f"Erreur audio normal.mp3: {e}")

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "moyen")
    if not secret_word:
        secret_word = "PYTHON"

    game_state = game_engine.create_game(secret_word, 7)
    timer = 30.0

    return game_state, secret_word, timer


def return_to_main_menu():
    """Relance le menu principal et ferme ce script."""
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.quit()
    main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    subprocess.Popen([sys.executable, main_path if os.path.exists(main_path) else "main.py"])
    sys.exit()

def get_name_input(final_score):
    """Saisie du nom pour le Highscore (5 chars)."""
    name = ""
    while True:
        screen.fill((0, 0, 0))
        prompt = fonts["info"].render("NOUVEAU RECORD (NORMAL) ! Nom :", True, constants.GOLD)
        name_surf = fonts["word"].render(name + ("_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""), True, constants.WHITE)
        instr = fonts["small"].render("Appuie sur ENTREE pour valider", True, constants.WHITE)
        
        screen.blit(prompt, prompt.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 50)))
        screen.blit(name_surf, name_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 20)))
        screen.blit(instr, instr.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 80)))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    score_manager.save_score(name, final_score, category="normal")
                    return
                elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                elif len(name) < 5 and event.unicode.isalpha():
                    name += event.unicode.upper()


def play_win_sequence(secret_word, state):
    """Sequence for winning: winnormal.png, score check (Normal), and name input."""
    pygame.mixer.music.stop()
    final_score = score_manager.calculate_score(state)
    
    win_bg_path = os.path.join("assets", "images", "winnormal.png")
    current_win_bg = img_bg
    if os.path.exists(win_bg_path):
        current_win_bg = pygame.transform.scale(pygame.image.load(win_bg_path).convert(), (constants.WIDTH, constants.HEIGHT))

    win_audio_path = os.path.join("assets", "audios", "victoire.mp3")
    if os.path.exists(win_audio_path):
        pygame.mixer.music.load(win_audio_path); pygame.mixer.music.play()

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT)); fade.fill((0, 0, 0))
    for alpha in range(0, 180, 5): 
        screen.blit(current_win_bg, (0, 0))
        fade.set_alpha(alpha); screen.blit(fade, (0, 0))
        pygame.display.flip(); pygame.time.delay(10)

    start_wait = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_wait < 7000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        pygame.time.delay(100)

    # Vérification Record spécifique NORMAL
    if score_manager.check_if_highscore(final_score, category="normal"):
        get_name_input(final_score)

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(current_win_bg, (0, 0)); screen.blit(fade, (0, 0))

        win_text = language_manager.get_text("hard_win")
        msg = fonts["word"].render(win_text, True, constants.GREEN)
        msg_score = fonts["info"].render(f"SCORE: {final_score}", True, constants.GOLD)
        msg2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)
        
        screen.blit(msg, msg.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(msg_score, msg_score.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 20)))
        screen.blit(msg2, msg2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 40)))

        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("hard_retry"), fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_quit, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("hard_quit"), fonts["button"])
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos): return "restart"
                if rect_quit.collidepoint(event.pos): return_to_main_menu()


def play_lose_sequence(secret_word, state):
    """Play the loss sequence with macron.mp4 (12s to 17s)."""
    pygame.mixer.music.stop()
    video_path = os.path.join("assets", "vidéo", "macron.mp4")
    audio_path = os.path.join("assets", "audios", "macron.mp3")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened(): return "restart"

    cap.set(cv2.CAP_PROP_POS_MSEC, 12000)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    if os.path.exists(audio_path):
        pygame.mixer.music.load(audio_path); pygame.mixer.music.play(start=12.0)

    clock = pygame.time.Clock()
    last_frame_surf = None
    
    while cap.isOpened():
        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        if current_time_ms >= 17000: break
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (constants.WIDTH, constants.HEIGHT)).swapaxes(0, 1)
        last_frame_surf = pygame.surfarray.make_surface(frame)
        screen.blit(last_frame_surf, (0, 0)); pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: cap.release(); pygame.quit(); sys.exit()
        clock.tick(fps)

    cap.release(); pygame.mixer.music.stop()
    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        if last_frame_surf: screen.blit(last_frame_surf, (0, 0))
        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA); overlay.fill(constants.BLACK_OVERLAY); screen.blit(overlay, (0, 0))
        t1 = fonts["word"].render(language_manager.get_text("hard_loss"), True, constants.RED)
        t2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)
        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2)))
        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("hard_retry"), fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_back, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("hard_quit"), fonts["button"])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos): return "restart"
                if rect_back.collidepoint(event.pos): return_to_main_menu()


def draw_interface(state, secret, timer, mouse_pos):
    """Draw the game interface."""
    screen.blit(img_bg, (0, 0))
    pygame_utils.draw_button_with_border(screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, language_manager.get_text("hard_pause"), fonts["button"])
    
    curr_score = score_manager.calculate_score(state)
    surf_score = fonts["info"].render(f"SCORE: {curr_score}", True, constants.WHITE)
    screen.blit(surf_score, (constants.WIDTH - 180, 20))

    timer_val = max(0, int(timer))
    surf_timer = fonts["timer"].render(f"{timer_val}s", True, constants.RED if timer < 10 else constants.WHITE)
    screen.blit(surf_timer, surf_timer.get_rect(center=(constants.WIDTH // 2, 50)))

    error_count = state["errors"]
    if error_count > 0 and (idx := min(error_count, 7)) in imgs:
        screen.blit(imgs[idx], (constants.WIDTH // 2 - 150, 100))

    masked = game_engine.get_masked_word(state)
    surf_mot = fonts["word"].render(" ".join(masked), True, constants.WHITE)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 180))

    wrong = [l.upper() for l in state["letters_played"] if l not in secret.lower()]
    screen.blit(fonts["small"].render(f"{language_manager.get_text('hard_errors')} ({error_count}/7)", True, constants.RED), (20, constants.HEIGHT - 70))
    screen.blit(fonts["small"].render(", ".join(wrong), True, constants.WHITE), (20, constants.HEIGHT - 40))


def main():
    """Main game loop."""
    language_manager.set_language("en" if len(sys.argv) > 1 and sys.argv[1].upper() == "EN" else "fr")
    initialize_pygame()
    game_state, secret_word, timer = initialize_game()
    clock, paused = pygame.time.Clock(), False

    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(constants.WIDTH // 2 - 280, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(constants.WIDTH // 2 - 90, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 100, constants.HEIGHT // 2 + 20, w_b, h_b)

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause_rect.collidepoint(event.pos): paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos): paused = False
                    if rect_reset.collidepoint(event.pos): game_state, secret_word, timer = initialize_game(); paused = False
                    if rect_quit.collidepoint(event.pos): return_to_main_menu()
            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    old_err = game_state["errors"]
                    game_engine.play_letter(game_state, letter)
                    timer += 5 if game_state["errors"] == old_err else -5

        if game_state["status"] == "in_progress" and not paused:
            timer -= dt
            if timer <= 0 or game_state["errors"] >= 7:
                game_state["status"] = "loss"
                if play_lose_sequence(secret_word, game_state) == "restart": game_state, secret_word, timer = initialize_game()
        elif game_state["status"] == "won":
            draw_interface(game_state, secret_word, timer, mouse_pos); pygame.display.flip()
            if play_win_sequence(secret_word, game_state) == "restart": game_state, secret_word, timer = initialize_game()
        
        if not paused: draw_interface(game_state, secret_word, timer, mouse_pos)
        else:
            overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA); overlay.fill(constants.BLACK_OVERLAY); screen.blit(overlay, (0, 0))
            for r, lbl in [(rect_cont, "hard_continue"), (rect_reset, "hard_reset"), (rect_quit, "hard_quit")]:
                pygame_utils.draw_button_with_border(screen, r, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, language_manager.get_text(lbl), fonts["button"])
        pygame.display.flip()

if __name__ == "__main__":
    main()