"""
Hard mode view for the Hangman game.
Features: 30s timer, 7 max errors, macron video (12s-17s) on loss.
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
from utils import word_manager
from utils import language_manager
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
        # Background normal.png
        bg_path = os.path.join("assets", "images", "normal.png")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.image.load(constants.IMG_BACKGROUND_GAME).convert()
            
        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
        
        # Chargement des images du pendu (étapes 1 à 7)
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

    # Lancement de la musique normal.mp3 avec un départ à 5 secondes
    normal_audio = os.path.join("assets", "audios", "normal.mp3")
    if os.path.exists(normal_audio):
        try:
            pygame.mixer.music.load(normal_audio)
            pygame.mixer.music.play(-1, start=5.0)
        except Exception as e:
            print(f"Erreur audio normal.mp3: {e}")

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "difficile")
    if not secret_word:
        secret_word = "PYTHON"

    # Le joueur possède 7 essais
    game_state = game_engine.create_game(secret_word, 7)
    timer = 30.0

    return game_state, secret_word, timer


def return_to_main_menu():
    """Relance le menu principal et ferme ce script."""
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.quit()
    
    main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    
    if os.path.exists(main_path):
        subprocess.Popen([sys.executable, main_path])
    else:
        subprocess.Popen([sys.executable, "main.py"])
        
    sys.exit()


def play_win_sequence():
    """Sequence for winning: black fade with bg visible, playing victoire.mp3."""
    pygame.mixer.music.stop()
    
    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 200, 5): 
        screen.blit(img_bg, (0, 0))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

    # Utilisation de victoire.mp3 dans le dossier audios
    win_audio_path = os.path.join("assets", "audios", "victoire.mp3")
    
    if os.path.exists(win_audio_path):
        try:
            pygame.mixer.music.load(win_audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.time.delay(100)
        except Exception as e:
            print(f"Erreur audio victoire: {e}")
            pygame.time.delay(2000)
    else:
        pygame.time.delay(2000)


def play_lose_sequence(secret_word, state):
    """Play the loss sequence with macron.mp4 and macron.mp3 (12s to 17s)."""
    pygame.mixer.music.stop()
    
    video_path = os.path.join("assets", "vidéo", "macron.mp4")
    audio_path = os.path.join("assets", "audios", "macron.mp3")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "restart"

    # Décalage à 12 secondes
    cap.set(cv2.CAP_PROP_POS_MSEC, 12000)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    if os.path.exists(audio_path):
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(start=12.0)
        except Exception as e:
            print(f"Erreur audio macron: {e}")

    clock = pygame.time.Clock()
    last_frame_surf = None
    
    while cap.isOpened():
        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        if current_time_ms >= 17000:
            break

        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.resize(frame, (constants.WIDTH, constants.HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        last_frame_surf = pygame.surfarray.make_surface(frame)
        
        screen.blit(last_frame_surf, (0, 0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
                
        clock.tick(fps)

    cap.release()
    pygame.mixer.music.stop()

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        if last_frame_surf:
            screen.blit(last_frame_surf, (0, 0))

        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        overlay.fill(constants.BLACK_OVERLAY)
        screen.blit(overlay, (0, 0))

        loss_text = language_manager.get_text("hard_loss")
        t1 = fonts["word"].render(loss_text, True, constants.RED)
        t2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)
        
        # Astuce
        tip_text = "Astuce : Au pendu, il ne faut jamais perdre la tête..."
        t_tip = fonts["small"].render(tip_text, True, constants.GOLD)

        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2)))
        screen.blit(t_tip, t_tip.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 50)))

        retry_text = language_manager.get_text("hard_retry")
        quit_text = language_manager.get_text("hard_quit")

        for rect, label in [(rect_retry, retry_text), (rect_back, quit_text)]:
            pygame_utils.draw_button_with_border(
                screen, rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER,
                m_pos, label, fonts["button"]
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return "restart"
                if rect_back.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return_to_main_menu()


def draw_interface(state, secret, timer, mouse_pos):
    """Draw the game interface."""
    screen.blit(img_bg, (0, 0))

    pygame_utils.draw_button_with_border(
        screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER,
        mouse_pos, language_manager.get_text("hard_pause"), fonts["button"]
    )

    timer_val = max(0, int(timer))
    timer_color = constants.RED if timer < 10 else constants.WHITE
    surf_timer = fonts["timer"].render(f"{timer_val}s", True, timer_color)
    timer_rect = surf_timer.get_rect(center=(constants.WIDTH // 2, 50))
    
    if timer < 5 and timer > 0:
        timer_rect.x += random.randint(-3, 3)
        timer_rect.y += random.randint(-3, 3)
    screen.blit(surf_timer, timer_rect)

    error_count = state["errors"]
    if error_count > 0:
        idx = min(error_count, 7)
        if idx in imgs:
            img_pendu = imgs[idx]
            screen.blit(img_pendu, (constants.WIDTH // 2 - img_pendu.get_width() // 2, 100))

    masked = game_engine.get_masked_word(state)
    surf_mot = fonts["word"].render(" ".join(masked), True, constants.WHITE)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 180))

    wrong_letters = [l for l in state["letters_played"] if l not in secret.lower()]
    errors_text = language_manager.get_text("hard_errors")
    screen.blit(fonts["small"].render(f"{errors_text} ({error_count}/7)", True, constants.RED), (20, constants.HEIGHT - 70))
    screen.blit(fonts["small"].render(", ".join(wrong_letters).upper(), True, constants.WHITE), (20, constants.HEIGHT - 40))


def main():
    """Main game loop."""
    if len(sys.argv) > 1 and sys.argv[1].upper() == "EN":
        language_manager.set_language("en")
    else:
        language_manager.set_language("fr")

    initialize_pygame()
    game_state, secret_word, timer = initialize_game()
    clock = pygame.time.Clock()
    paused = False

    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(constants.WIDTH // 2 - 280, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(constants.WIDTH // 2 - 90, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 100, constants.HEIGHT // 2 + 20, w_b, h_b)

    rect_retry_win = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_quit_win = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
                        game_state, secret_word, timer = initialize_game()
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        return_to_main_menu()

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    old_err = game_state["errors"]
                    game_engine.play_letter(game_state, letter)
                    if game_state["errors"] == old_err:
                        timer += 5
                    else:
                        timer -= 5

                    if game_state["errors"] >= 7:
                        game_state["status"] = "loss"
                        if play_lose_sequence(secret_word, game_state) == "restart":
                            game_state, secret_word, timer = initialize_game()
                            continue

        if game_state["status"] == "in_progress" and not paused:
            timer -= dt
            if timer <= 0:
                game_state["status"] = "loss"
                if play_lose_sequence(secret_word, game_state) == "restart":
                    game_state, secret_word, timer = initialize_game()
                    continue

        if game_state["status"] == "won":
            play_win_sequence()
            while game_state["status"] == "won":
                m_pos = pygame.mouse.get_pos()
                screen.blit(img_bg, (0, 0))
                overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
                overlay.fill(constants.BLACK_OVERLAY)
                screen.blit(overlay, (0, 0))

                win_text = language_manager.get_text("hard_win")
                msg = fonts["word"].render(win_text, True, constants.GREEN)
                msg2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)
                screen.blit(msg, msg.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 60)))
                screen.blit(msg2, msg2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 20)))

                retry_t = language_manager.get_text("hard_retry")
                quit_t = language_manager.get_text("hard_quit")

                for r, label in [(rect_retry_win, retry_t), (rect_quit_win, quit_t)]:
                    pygame_utils.draw_button_with_border(
                        screen, r, constants.DARK_BLUE, constants.DARK_BLUE_HOVER,
                        m_pos, label, fonts["button"]
                    )

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if rect_retry_win.collidepoint(event.pos):
                            pygame_utils.play_click_sound()
                            game_state, secret_word, timer = initialize_game()
                        if rect_quit_win.collidepoint(event.pos):
                            pygame_utils.play_click_sound()
                            return_to_main_menu()
            continue

        if game_state["status"] == "in_progress":
            draw_interface(game_state, secret_word, timer, mouse_pos)

            if paused:
                overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
                overlay.fill(constants.BLACK_OVERLAY)
                screen.blit(overlay, (0, 0))

                pause_title = language_manager.get_text("hard_pause")
                txt_pause = fonts["word"].render(pause_title, True, constants.GOLD)
                screen.blit(txt_pause, txt_pause.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 60)))

                for r, label in [(rect_cont, language_manager.get_text("hard_continue")), 
                                 (rect_reset, language_manager.get_text("hard_reset")), 
                                 (rect_quit, language_manager.get_text("hard_quit"))]:
                    pygame_utils.draw_button_with_border(
                        screen, r, constants.DARK_BLUE, constants.DARK_BLUE_HOVER,
                        mouse_pos, label, fonts["button"]
                    )

        pygame.display.flip()


if __name__ == "__main__":
    main()