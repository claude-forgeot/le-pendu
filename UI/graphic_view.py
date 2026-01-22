"""
Module graphic_view - Interface graphique Pygame pour le jeu du Pendu
Contient toute la logique de l'interface utilisateur avec Pygame
"""
import pygame
import sys
import os
import subprocess

from UI import constants
from UI import pygame_utils
from utils import language_manager


def main_gui():
    """
    Fonction principale de l'interface graphique Pygame
    Affiche le menu principal avec les modes de jeu et options de langue
    """
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(
        (constants.WIDTH, constants.HEIGHT),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("Le Pendu - Interface Responsive")

    try:
        img_background = pygame.image.load(constants.IMG_BACKGROUND_HOME)
        img_logo = pygame.image.load(constants.IMG_LOGO)
        img_fr = pygame.image.load(constants.IMG_FLAG_FR)
        img_us = pygame.image.load(constants.IMG_FLAG_US)

        pygame.mixer.music.load(constants.AUDIO_MAIN_MENU)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error loading resources: {e}")
        pygame.quit()
        sys.exit()

    running = True
    while running:
        win_w, win_h = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()

        bg_scaled = pygame.transform.scale(img_background, (win_w, win_h))
        screen.blit(bg_scaled, (0, 0))

        logo_w = int(win_w * 0.22)
        if logo_w < 180:
            logo_w = 180
        logo_ratio = logo_w / img_logo.get_width()
        logo_h = int(img_logo.get_height() * logo_ratio)
        logo_scaled = pygame.transform.scale(img_logo, (logo_w, logo_h))
        screen.blit(logo_scaled, (30, 30))

        flag_w = int(win_w * 0.08)
        if flag_w < 60:
            flag_w = 60
        flag_h = int(flag_w * 0.66)

        fr_scaled = pygame.transform.scale(img_fr, (flag_w, flag_h))
        us_scaled = pygame.transform.scale(img_us, (flag_w, flag_h))

        screen.blit(us_scaled, (win_w - flag_w - 30, 30))
        screen.blit(fr_scaled, (win_w - (flag_w * 2) - 60, 30))

        btn_w = int(win_w * 0.22)
        if btn_w < 220:
            btn_w = 220
        btn_h = int(win_h * 0.09)
        if btn_h < 60:
            btn_h = 60

        font_size = int(btn_h * 0.45)
        font = pygame.font.SysFont("Arial", font_size, bold=True)

        spacing = int(btn_h * 1.25)
        start_y = logo_h + 60

        rect_facile = pygame.Rect(40, start_y, btn_w, btn_h)
        rect_normal = pygame.Rect(40, start_y + spacing, btn_w, btn_h)
        rect_difficile = pygame.Rect(40, start_y + spacing * 2, btn_w, btn_h)
        rect_infini = pygame.Rect(40, start_y + spacing * 3, btn_w, btn_h)

        if win_w < 600:
            pos_x_bas = win_w - btn_w - 40
            rect_versus = pygame.Rect(pos_x_bas, win_h - (btn_h * 2) - 60, btn_w, btn_h)
            rect_scores = pygame.Rect(pos_x_bas, win_h - btn_h - 40, btn_w, btn_h)
        else:
            rect_versus = pygame.Rect(win_w // 2 - btn_w // 2, win_h - btn_h - 40, btn_w, btn_h)
            rect_scores = pygame.Rect(win_w - btn_w - 40, win_h - btn_h - 40, btn_w, btn_h)

        def get_color(rect, normal_c, hover_c):
            return hover_c if rect.collidepoint(mouse_pos) else normal_c

        pygame_utils.draw_rounded_button(
            screen,
            get_color(rect_facile, constants.GREEN, constants.GREEN_HOVER),
            rect_facile,
            language_manager.get_text("button_facile"),
            font
        )
        pygame_utils.draw_rounded_button(
            screen,
            get_color(rect_normal, constants.ORANGE, constants.ORANGE_HOVER),
            rect_normal,
            language_manager.get_text("button_normal"),
            font
        )
        pygame_utils.draw_rounded_button(
            screen,
            get_color(rect_difficile, constants.RED, constants.RED_HOVER),
            rect_difficile,
            language_manager.get_text("button_difficile"),
            font
        )
        pygame_utils.draw_rounded_button(
            screen,
            get_color(rect_infini, constants.DARK_BLUE, constants.DARK_BLUE_HOVER),
            rect_infini,
            language_manager.get_text("button_infini"),
            font
        )
        pygame_utils.draw_rounded_button(
            screen,
            get_color(rect_versus, constants.PURPLE, constants.PURPLE_HOVER),
            rect_versus,
            language_manager.get_text("button_versus"),
            font
        )
        pygame_utils.draw_rounded_button(
            screen,
            get_color(rect_scores, constants.GOLD, constants.GOLD_HOVER),
            rect_scores,
            language_manager.get_text("button_scores"),
            font
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_facile.collidepoint(event.pos):
                    print(language_manager.get_text("mode_easy"))

                # Lancement du Mode Normal
                if rect_normal.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    pygame.quit()
                    normal_mode_path = os.path.join(
                        constants.BASE_DIR, "UI", "normal_mode_view.py"
                    )
                    subprocess.Popen([sys.executable, normal_mode_path])
                    sys.exit()

                # Lancement du Mode Difficile
                if rect_difficile.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    pygame.quit()
                    hard_mode_path = os.path.join(
                        constants.BASE_DIR, "UI", "hard_mode_view.py"
                    )
                    subprocess.Popen([sys.executable, hard_mode_path])
                    sys.exit()

                fr_rect = pygame.Rect(win_w - (flag_w * 2) - 60, 30, flag_w, flag_h)
                us_rect = pygame.Rect(win_w - flag_w - 30, 30, flag_w, flag_h)
                if fr_rect.collidepoint(event.pos):
                    language_manager.set_language("fr")
                    print("Langue changee: Francais")
                if us_rect.collidepoint(event.pos):
                    language_manager.set_language("en")
                    print("Language changed: English")

        pygame.display.flip()

    pygame.quit()
    sys.exit()