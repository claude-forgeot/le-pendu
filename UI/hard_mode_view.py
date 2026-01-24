# Hard mode: 30s timer, 5 errors, video on loss, difficile category scores

import pygame
import sys
import os
import cv2
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import game_engine
from utils import word_manager
from utils import language_manager
from utils import score_manager
from UI import constants
from UI import pygame_utils


# Module-level variables for resources
img_bg = None
imgs = {}

# Pause button rect
btn_pause_rect = pygame.Rect(20, 20, 120, 40)
HINT_CENTER = (constants.WIDTH - 80, constants.HEIGHT - 80)
HINT_RADIUS = 40


# Load background and hangman sprite images for hard mode
def load_resources():
    global img_bg, imgs

    try:
        img_bg = pygame.image.load(constants.IMG_BACKGROUND_GAME).convert()
        img_bg = pygame.transform.scale(img_bg, (constants.WIDTH, constants.HEIGHT))
        imgs = pygame_utils.load_hangman_images()
    except Exception as e:
        print(f"Error loading resources: {e}")
        img_bg = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        img_bg.fill((40, 40, 40))
        imgs = {}


# Reset game state with difficile word, 30s timer, 1 hint, 5 max errors
def initialize_game():
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    if os.path.exists(constants.AUDIO_HARD_MODE):
        pygame.mixer.music.load(constants.AUDIO_HARD_MODE)
        pygame.mixer.music.play(-1)

    current_lang = language_manager.get_current_language()
    secret_word = word_manager.get_word(current_lang, "difficile")
    if not secret_word:
        secret_word = "PYTHON"

    game_state = game_engine.create_game(secret_word, 5)
    timer = 30.0
    hints_left = 1
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


# Capture 5-char player name for highscore entry, save to difficile category
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
                    score_manager.save_score(name, final_score, category="difficile")
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 5 and event.unicode.isalpha():
                    name += event.unicode.upper()


# Display win screen with fade, winhard image/audio, check highscore
def play_win_sequence(screen, fonts, secret_word, state, time_remaining, hints_used):
    pygame.mixer.music.stop()
    final_score = score_manager.calculate_score(state, time_remaining, hints_used)

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        screen.blit(img_bg, (0, 0))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

    win_img_path = os.path.join("assets", "images", "winhard.png")

    win_img = None
    if os.path.exists(win_img_path):
        win_img = pygame.image.load(win_img_path).convert()
        win_img = pygame.transform.scale(win_img, (constants.WIDTH, constants.HEIGHT))
        screen.blit(win_img, (0, 0))
        pygame.display.flip()

    if os.path.exists(constants.AUDIO_WIN_HARD):
        pygame.mixer.music.load(constants.AUDIO_WIN_HARD)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
            pygame.time.delay(100)
    else:
        pygame.time.delay(2000)

    if score_manager.check_if_highscore(final_score, category="difficile"):
        result = get_name_input(screen, fonts, final_score)
        if result is None:
            return "quit"

    rect_retry_win = pygame.Rect(constants.WIDTH // 2 - 210, constants.HEIGHT - 120, 200, 50)
    rect_quit_win = pygame.Rect(constants.WIDTH // 2 + 10, constants.HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.blit(img_bg, (0, 0))
        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        overlay.fill(constants.BLACK_OVERLAY)
        screen.blit(overlay, (0, 0))

        win_text = language_manager.get_text("hard_win")
        msg = fonts["word"].render(win_text, True, constants.GREEN)
        msg_score = fonts["info"].render(f"SCORE: {final_score}", True, constants.GOLD)
        msg2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)

        screen.blit(msg, msg.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 80)))
        screen.blit(msg_score, msg_score.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 20)))
        screen.blit(msg2, msg2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 40)))

        retry_t = language_manager.get_text("hard_retry")
        quit_t = language_manager.get_text("hard_quit")

        pygame_utils.draw_button_with_border(screen, rect_retry_win, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, retry_t, fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_quit_win, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, quit_t, fonts["button"])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry_win.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return "restart"
                if rect_quit_win.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return "main_menu"


# Play losehard video (12s-43s) with audio, then show game over screen
def play_lose_sequence(screen, fonts, secret_word, state):
    pygame.mixer.music.stop()

    video_path = constants.VIDEO_LOSE_HARD

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Video file not found: {video_path}")
        cap = None
    else:
        cap.set(cv2.CAP_PROP_POS_MSEC, 12000)

    fps = 30
    if cap:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30

    if os.path.exists(constants.AUDIO_LOSE_HARD):
        pygame.mixer.music.load(constants.AUDIO_LOSE_HARD)
        pygame.mixer.music.play(start=12.0)

    clock_local = pygame.time.Clock()
    last_frame_surf = None

    fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    fade.fill((0, 0, 0))

    alpha = 255
    if cap:
        while cap.isOpened():
            current_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
            if current_msec >= 43000:
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (constants.WIDTH, constants.HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0, 1)
            last_frame_surf = pygame.surfarray.make_surface(frame)

            screen.blit(last_frame_surf, (0, 0))

            if alpha > 0:
                fade.set_alpha(alpha)
                screen.blit(fade, (0, 0))
                alpha -= 5

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

        loss_text = language_manager.get_text("hard_loss")
        t1 = fonts["word"].render(loss_text, True, constants.RED)
        t2 = fonts["info"].render(f"{secret_word}", True, constants.WHITE)
        screen.blit(t1, t1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 60)))
        screen.blit(t2, t2.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 20)))

        retry_text = language_manager.get_text("hard_retry")
        quit_text = language_manager.get_text("hard_quit")

        pygame_utils.draw_button_with_border(screen, rect_retry, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, retry_text, fonts["button"])
        pygame_utils.draw_button_with_border(screen, rect_back, constants.DARK_BLUE, constants.DARK_BLUE_HOVER, m_pos, quit_text, fonts["button"])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return "restart"
                if rect_back.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return "main_menu"


# Render background, timer with shake, score, sprites, masked word, errors
def draw_interface(screen, fonts, state, secret, timer, hints_left, hints_used, mouse_pos):
    screen.blit(img_bg, (0, 0))

    pygame_utils.draw_button_with_border(
        screen, btn_pause_rect, constants.DARK_BLUE, constants.DARK_BLUE_HOVER,
        mouse_pos, language_manager.get_text("hard_pause"), fonts["button"]
    )

    current_score = score_manager.calculate_score(state, timer, hints_used)
    surf_score = fonts["info"].render(f"SCORE: {current_score}", True, constants.WHITE)
    screen.blit(surf_score, (constants.WIDTH - 180, 20))

    timer_val = max(0, int(timer))
    timer_color = constants.RED if timer < 10 else constants.WHITE
    surf_timer = fonts["timer"].render(f"{timer_val}s", True, timer_color)
    timer_rect = surf_timer.get_rect(center=(constants.WIDTH // 2, 50))
    if timer < 5 and timer > 0:
        timer_rect.x += random.randint(-3, 3)
        timer_rect.y += random.randint(-3, 3)
    screen.blit(surf_timer, timer_rect)

    size = constants.HANGMAN_SPRITE_SIZE
    tx, ty = constants.WIDTH // 2 - size // 2, 130
    pos = {
        1: (tx, ty),
        2: (tx - size, ty + size),
        3: (tx + size, ty + size),
        4: (tx - size // 2, ty + 2 * size),
        5: (tx + size // 2, ty + 2 * size)
    }
    for i in range(1, state["errors"] + 1):
        if i in imgs:
            screen.blit(imgs[i], pos[i])

    masked = game_engine.get_masked_word(state)
    surf_mot = pygame_utils.render_word_adaptive(masked, constants.WIDTH - 40)
    screen.blit(surf_mot, (constants.WIDTH // 2 - surf_mot.get_width() // 2, constants.HEIGHT - 180))

    wrong_letters = []
    for l in state["letters_played"]:
        if l not in secret.lower():
            wrong_letters.append(l)

    errors_text = language_manager.get_text("hard_errors")
    screen.blit(fonts["small"].render(errors_text, True, constants.RED), (20, constants.HEIGHT - 70))
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
                    pygame_utils.play_click_sound()
                    paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        paused = False
                    if rect_reset.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        game_state, secret_word, timer, hints_left, hints_used = initialize_game()
                        paused = False
                    if rect_quit.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
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

                    if game_state["errors"] >= 5:
                        game_state["status"] = "loss"
                        result = play_lose_sequence(screen, fonts, secret_word, game_state)
                        if result == "restart":
                            game_state, secret_word, timer, hints_left, hints_used = initialize_game()
                        elif result == "main_menu":
                            return "main_menu"
                        elif result == "quit":
                            return None

        if game_state["status"] == "in_progress" and not paused:
            timer -= dt
            if timer <= 0:
                game_state["status"] = "loss"
                result = play_lose_sequence(screen, fonts, secret_word, game_state)
                if result == "restart":
                    game_state, secret_word, timer, hints_left, hints_used = initialize_game()
                elif result == "main_menu":
                    return "main_menu"
                elif result == "quit":
                    return None

        if game_state["status"] == "won":
            result = play_win_sequence(screen, fonts, secret_word, game_state, timer, hints_used)
            if result == "restart":
                game_state, secret_word, timer, hints_left, hints_used = initialize_game()
            elif result == "main_menu":
                return "main_menu"
            elif result == "quit":
                return None
            continue

        if game_state["status"] == "in_progress":
            draw_interface(screen, fonts, game_state, secret_word, timer, hints_left, hints_used, mouse_pos)

            if paused:
                overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
                overlay.fill(constants.BLACK_OVERLAY)
                screen.blit(overlay, (0, 0))

                pause_title = language_manager.get_text("hard_pause")
                txt_pause = fonts["word"].render(pause_title, True, constants.GOLD)
                screen.blit(txt_pause, txt_pause.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 60)))

                cont_text = language_manager.get_text("hard_continue")
                reset_text = language_manager.get_text("hard_reset")
                quit_text = language_manager.get_text("hard_quit")

                for r, label in [(rect_cont, cont_text), (rect_reset, reset_text), (rect_quit, quit_text)]:
                    pygame_utils.draw_button_with_border(
                        screen, r, constants.DARK_BLUE, constants.DARK_BLUE_HOVER,
                        mouse_pos, label, fonts["button"]
                    )

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
