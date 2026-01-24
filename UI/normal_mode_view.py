# Normal mode: 30s timer, 7 errors, video on loss, score tracking

import pygame
import sys
import os
import cv2
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import game_engine
from utils import word_manager, language_manager, score_manager
from UI import constants
from UI import pygame_utils


# Module-level variables for resources
img_bg = None

# Pause button rect
btn_pause_rect = pygame.Rect(20, 20, 120, 40)
HINT_CENTER = (constants.WIDTH - 80, constants.HEIGHT - 80)
HINT_RADIUS = 40


# Load and scale background image for normal mode
def load_resources():
    global img_bg

    try:
        bg_path = os.path.join("assets", "images", "normal.png")
        if os.path.exists(bg_path):
            img_bg = pygame.image.load(bg_path).convert()
        else:
            img_bg = pygame.image.load(constants.IMG_BACKGROUND_GAME).convert()

        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        img_bg.fill((40, 40, 40))


# Reset game state with moyen word, 30s timer, 2 hints
def initialize_game():
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    if os.path.exists(constants.AUDIO_NORMAL_MODE):
        try:
            pygame.mixer.music.load(constants.AUDIO_NORMAL_MODE)
            pygame.mixer.music.play(-1, start=5.0)
        except Exception as e:
            print(f"Audio error normal.ogg: {e}")

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "moyen")
    if not secret_word:
        secret_word = "PYTHON"

    game_state = game_engine.create_game(secret_word, 7)
    timer = 30.0
    hints_left = 2
    hints_used = 0

    return game_state, secret_word, timer, hints_left, hints_used


# Play a random unguessed letter that IS in the word
def use_real_hint(state, secret):
    word_letters = set(secret.lower())
    played_letters = set(state["letters_played"])

    available_hints = []
    for letter in word_letters:
        if letter not in played_letters:
            available_hints.append(letter)

    if available_hints:
        letter = random.choice(available_hints)
        game_engine.play_letter(state, letter)
        return True
    return False


# Capture 5-char player name for highscore entry, save to normal category
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
                    score_manager.save_score(name, final_score, category="normal")
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 5 and event.unicode.isalpha():
                    name += event.unicode.upper()


# Display win screen, calculate score, check highscore, show retry/quit
def play_win_sequence(screen, fonts, secret_word, state, time_remaining, hints_used):
    pygame.mixer.music.stop()
    final_score = score_manager.calculate_score(state, time_remaining, hints_used)

    win_bg_path = os.path.join("assets", "images", "winnormal.png")
    current_win_bg = img_bg
    if os.path.exists(win_bg_path):
        current_win_bg = pygame.transform.scale(pygame.image.load(win_bg_path).convert(), (constants.WIDTH, constants.HEIGHT))

    if os.path.exists(constants.AUDIO_VICTORY):
        pygame.mixer.music.load(constants.AUDIO_VICTORY)
        pygame.mixer.music.play()

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 180, 5):
        screen.blit(current_win_bg, (0, 0))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

    pygame.time.delay(7000)

    if score_manager.check_if_highscore(final_score, category="normal"):
        result = get_name_input(screen, fonts, final_score)
        if result is None:
            return "quit"

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(current_win_bg, (0, 0))
        screen.blit(fade, (0, 0))

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
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    return "restart"
                if rect_quit.collidepoint(event.pos):
                    return "main_menu"


# Play macron video (12s-17s) with audio, then show game over screen
def play_lose_sequence(screen, fonts, secret_word, state):
    pygame.mixer.music.stop()
    video_path = constants.VIDEO_LOSE_NORMAL
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        cap = None
    else:
        cap.set(cv2.CAP_PROP_POS_MSEC, 12000)

    fps = 30
    if cap:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30

    if os.path.exists(constants.AUDIO_LOSE_NORMAL):
        pygame.mixer.music.load(constants.AUDIO_LOSE_NORMAL)
        pygame.mixer.music.play(start=12.0)

    clock_local = pygame.time.Clock()
    last_frame_surf = None

    if cap:
        while cap.isOpened():
            current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            if current_time_ms >= 17000:
                break
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (constants.WIDTH, constants.HEIGHT))
            frame = frame.swapaxes(0, 1)
            last_frame_surf = pygame.surfarray.make_surface(frame)
            screen.blit(last_frame_surf, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    return "quit"
            clock_local.tick(fps)
        cap.release()

    pygame.mixer.music.stop()

    rect_retry = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        if last_frame_surf:
            screen.blit(last_frame_surf, (0, 0))
        else:
            screen.blit(img_bg, (0, 0))

        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        overlay.fill(constants.BLACK_OVERLAY)
        screen.blit(overlay, (0, 0))

        t1 = fonts["word"].render(language_manager.get_text("hard_loss"), True, constants.RED)
        t2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)
        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2)))

        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("hard_retry"), fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_back, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, language_manager.get_text("hard_quit"), fonts["button"])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    return "restart"
                if rect_back.collidepoint(event.pos):
                    return "main_menu"


# Render background, timer, score, hangman, masked word, errors and hint button
def draw_interface(screen, fonts, state, secret, timer, hints_left, hints_used, mouse_pos):
    screen.blit(img_bg, (0, 0))
    pygame_utils.draw_button_with_border(screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, language_manager.get_text("hard_pause"), fonts["button"])

    curr_score = score_manager.calculate_score(state, timer, hints_used)
    surf_score = fonts["info"].render(f"SCORE: {curr_score}", True, constants.WHITE)
    screen.blit(surf_score, (constants.WIDTH - 180, 20))

    timer_val = max(0, int(timer))
    timer_color = constants.RED if timer < 10 else constants.WHITE
    surf_timer = fonts["timer"].render(f"{timer_val}s", True, timer_color)
    screen.blit(surf_timer, surf_timer.get_rect(center=(constants.WIDTH // 2, 50)))

    pygame_utils.draw_hangman(screen, state["errors"], constants.WIDTH // 2 - 100, 80)

    masked = game_engine.get_masked_word(state)
    surf_mot = pygame_utils.render_word_adaptive(masked, constants.WIDTH - 40)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 180))

    wrong_letters = []
    for l in state["letters_played"]:
        if l not in secret.lower():
            wrong_letters.append(l)

    errors_text = language_manager.get_text("hard_errors")
    screen.blit(fonts["small"].render(f"{errors_text} ({state['errors']}/7)", True, constants.RED), (20, constants.HEIGHT - 70))
    screen.blit(fonts["small"].render(", ".join(wrong_letters).upper(), True, constants.WHITE), (20, constants.HEIGHT - 40))

    # Hint button
    dist = ((mouse_pos[0] - HINT_CENTER[0]) ** 2 + (mouse_pos[1] - HINT_CENTER[1]) ** 2) ** 0.5
    color = constants.GOLD if dist < HINT_RADIUS else constants.DARK_BLUE
    pygame.draw.circle(screen, color, HINT_CENTER, HINT_RADIUS)
    pygame.draw.circle(screen, constants.WHITE, HINT_CENTER, HINT_RADIUS, 2)

    hint_label = language_manager.get_text("hint")
    txt_hint = fonts["small"].render(hint_label + " (" + str(hints_left) + ")", True, constants.WHITE)
    screen.blit(txt_hint, txt_hint.get_rect(center=HINT_CENTER))


# Main game loop with timer countdown, state updates and rendering
def run_view(screen, fonts, clock):
    load_resources()
    game_state, secret_word, timer, hints_left, hints_used = initialize_game()
    paused = False

    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(constants.WIDTH // 2 - 280, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(constants.WIDTH // 2 - 90, constants.HEIGHT // 2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(constants.WIDTH // 2 + 100, constants.HEIGHT // 2 + 20, w_b, h_b)

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause_rect.collidepoint(event.pos):
                    paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos):
                        paused = False
                    if rect_reset.collidepoint(event.pos):
                        game_state, secret_word, timer, hints_left, hints_used = initialize_game()
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        return "main_menu"

                # Hint button click
                dist = ((event.pos[0] - HINT_CENTER[0]) ** 2 + (event.pos[1] - HINT_CENTER[1]) ** 2) ** 0.5
                if dist < HINT_RADIUS and not paused and hints_left > 0 and game_state["status"] == "in_progress":
                    pygame_utils.play_click_sound()
                    if use_real_hint(game_state, secret_word):
                        hints_left = hints_left - 1
                        hints_used = hints_used + 1

            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in game_state["letters_played"]:
                    old_err = game_state["errors"]
                    game_engine.play_letter(game_state, letter)
                    if game_state["errors"] == old_err:
                        timer += 5
                    else:
                        timer -= 5

        # Timer countdown when in progress
        if game_state["status"] == "in_progress" and not paused:
            timer -= dt
            if timer <= 0 or game_state["errors"] >= 7:
                game_state["status"] = "loss"

        # Handle win
        if game_state["status"] == "won":
            result = play_win_sequence(screen, fonts, secret_word, game_state, timer, hints_used)
            if result == "restart":
                game_state, secret_word, timer, hints_left, hints_used = initialize_game()
            elif result == "main_menu":
                return "main_menu"
            elif result == "quit":
                return None

        # Handle loss
        elif game_state["status"] == "loss" or game_state["status"] == "lost":
            result = play_lose_sequence(screen, fonts, secret_word, game_state)
            if result == "restart":
                game_state, secret_word, timer, hints_left, hints_used = initialize_game()
            elif result == "main_menu":
                return "main_menu"
            elif result == "quit":
                return None

        # Draw interface
        if not paused:
            draw_interface(screen, fonts, game_state, secret_word, timer, hints_left, hints_used, mouse_pos)
        else:
            draw_interface(screen, fonts, game_state, secret_word, timer, hints_left, hints_used, mouse_pos)
            overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
            overlay.fill(constants.BLACK_OVERLAY)
            screen.blit(overlay, (0, 0))

            txt = fonts["word"].render(language_manager.get_text("hard_pause"), True, constants.GOLD)
            screen.blit(txt, txt.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40)))

            for r, lbl in [(rect_cont, "hard_continue"), (rect_reset, "hard_reset"), (rect_quit, "hard_quit")]:
                pygame_utils.draw_button_with_border(screen, r, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, mouse_pos, language_manager.get_text(lbl), fonts["button"])

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
