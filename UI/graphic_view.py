import pygame
import sys
import os
import subprocess
import json

from UI import constants
from UI import pygame_utils
from utils import language_manager


# Main Pygame GUI function - displays main menu with game modes and language options
def main_gui():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(
        (constants.WIDTH, constants.HEIGHT),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("Le Pendu - Interface Responsive")

    # Chemins des images door et book
    path_door = os.path.join(constants.BASE_DIR, "assets", "images", "door.png")
    path_book = os.path.join(constants.BASE_DIR, "assets", "images", "book.png")
    path_scores = os.path.join(constants.BASE_DIR, "highscores.json")

    try:
        img_background = pygame.image.load(constants.IMG_BACKGROUND_HOME)
        img_logo = pygame.image.load(constants.IMG_LOGO)
        img_fr = pygame.image.load(constants.IMG_FLAG_FR)
        img_us = pygame.image.load(constants.IMG_FLAG_US)
        img_door = pygame.image.load(path_door)
        img_book = pygame.image.load(path_book)

        pygame.mixer.music.load(constants.AUDIO_MAIN_MENU)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error loading resources: {e}")
        pygame.quit()
        sys.exit()

    show_rules = False
    show_scores = False
    running = True

    while running:
        win_w, win_h = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()
        current_lang = language_manager.get_current_language()

        # Fond
        bg_scaled = pygame.transform.scale(img_background, (win_w, win_h))
        screen.blit(bg_scaled, (0, 0))

        # Logo and book (hidden if show_scores is True)
        logo_h = 0
        if not show_scores:
            logo_w = int(win_w * 0.22)
            if logo_w < 180: logo_w = 180
            logo_ratio = logo_w / img_logo.get_width()
            logo_h = int(img_logo.get_height() * logo_ratio)
            logo_scaled = pygame.transform.scale(img_logo, (logo_w, logo_h))
            screen.blit(logo_scaled, (30, 30))

            book_size = int(logo_h * 0.35)
            book_scaled = pygame.transform.scale(img_book, (book_size, book_size))
            rect_book = pygame.Rect(30 + logo_w + 20, 30 + (logo_h // 3), book_size, book_size)
            screen.blit(book_scaled, rect_book)
        else:
            logo_h = 100
            rect_book = pygame.Rect(-100, -100, 0, 0)

        # Flags and door
        flag_w = int(win_w * 0.08)
        if flag_w < 60: flag_w = 60
        flag_h = int(flag_w * 0.66)
        door_size = int(flag_h * 1.5)
        door_scaled = pygame.transform.scale(img_door, (door_size, door_size))

        pos_door_x = win_w - door_size - 30
        pos_us_x = pos_door_x - flag_w - 30
        pos_fr_x = pos_us_x - flag_w - 30

        rect_fr = pygame.Rect(pos_fr_x, 30, flag_w, flag_h)
        rect_us = pygame.Rect(pos_us_x, 30, flag_w, flag_h)
        rect_door = pygame.Rect(pos_door_x, 20, door_size, door_size)

        # Language indicator
        if current_lang == "fr":
            pygame.draw.rect(screen, (255, 235, 59), rect_fr.inflate(10, 10), width=4, border_radius=5)
        elif current_lang == "en":
            pygame.draw.rect(screen, (255, 235, 59), rect_us.inflate(10, 10), width=4, border_radius=5)

        fr_final = img_fr.copy()
        us_final = img_us.copy()
        if rect_fr.collidepoint(mouse_pos):
            fr_final.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_ADD)
        if rect_us.collidepoint(mouse_pos):
            us_final.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_ADD)

        screen.blit(pygame.transform.scale(fr_final, (flag_w, flag_h)), rect_fr)
        screen.blit(pygame.transform.scale(us_final, (flag_w, flag_h)), rect_us)
        screen.blit(door_scaled, rect_door)

        # Button parameters
        btn_w_base = int(win_w * 0.22)
        if btn_w_base < 220: btn_w_base = 220
        btn_h_base = int(win_h * 0.09)
        if btn_h_base < 60: btn_h_base = 60

        # Shift left if scores panel is shown
        target_x = -btn_w_base - 100 if show_scores else 40
        start_y = logo_h + 80
        spacing = int(btn_h_base * 1.25)

        rect_facile = pygame.Rect(target_x, start_y, btn_w_base, btn_h_base)
        rect_normal = pygame.Rect(target_x, start_y + spacing, btn_w_base, btn_h_base)
        rect_difficile = pygame.Rect(target_x, start_y + spacing * 2, btn_w_base, btn_h_base)
        rect_infini = pygame.Rect(target_x, start_y + spacing * 3, btn_w_base, btn_h_base)
        rect_add_word = pygame.Rect(target_x, start_y + spacing * 4, btn_w_base, btn_h_base)

        # Button configuration: (rect, key, color, hover_color, file_path)
        buttons_config = [
            (rect_facile, "button_facile", constants.GREEN, constants.GREEN_HOVER, "easy_mode_view.py"),
            (rect_normal, "button_normal", constants.ORANGE, constants.ORANGE_HOVER, "normal_mode_view.py"),
            (rect_difficile, "button_difficile", constants.RED, constants.RED_HOVER, "hard_mode_view.py"),
            (rect_infini, "button_infini", constants.DARK_BLUE, constants.DARK_BLUE_HOVER, "infinite_mode_view.py"),
            (rect_add_word, "button_add_word", constants.PURPLE, constants.PURPLE_HOVER, "add_word_view.py")
        ]

        # Draw game mode buttons
        for r, key, color, hover_c, file_path in buttons_config:
            is_hover = r.collidepoint(mouse_pos)
            draw_rect = r.inflate(24, 12) if is_hover else r
            font_size = int(btn_h_base * (0.52 if is_hover else 0.45))
            f = pygame.font.SysFont("Arial", font_size, bold=True)
            pygame_utils.draw_rounded_button(screen, hover_c if is_hover else color, draw_rect, language_manager.get_text(key), f)

        # Scores button
        rect_scores = pygame.Rect(win_w - btn_w_base - 40, win_h - btn_h_base - 40, btn_w_base, btn_h_base)
        is_h_scores = rect_scores.collidepoint(mouse_pos)
        d_r_scores = rect_scores.inflate(20, 10) if is_h_scores else rect_scores
        f_s_scores = int(btn_h_base * 0.52) if is_h_scores else int(btn_h_base * 0.45)
        score_btn_text = language_manager.get_text("button_scores") if not show_scores else ("RETOUR" if current_lang=="fr" else "BACK")
        pygame_utils.draw_rounded_button(screen, constants.GOLD_HOVER if is_h_scores else constants.GOLD, d_r_scores, score_btn_text, pygame.font.SysFont("Arial", f_s_scores, bold=True))

        # Scores panel
        if show_scores:
            # Taille réduite du titre pour éviter les collisions avec les drapeaux
            title_font = pygame.font.SysFont("Arial", int(win_h * 0.055), bold=True)
            title_text = "CLASSEMENT (TOP 5)" if current_lang == "fr" else "LEADERBOARD (TOP 5)"
            title_surf = title_font.render(title_text, True, (0, 0, 0))
            # Positionnement un peu plus bas pour laisser de l'air en haut
            screen.blit(title_surf, (win_w // 2 - title_surf.get_width() // 2, 55))

            # Chargement des scores
            all_data = {}
            if os.path.exists(path_scores):
                try:
                    with open(path_scores, "r") as f:
                        all_data = json.load(f)
                except: pass

            panel_margin = 40
            panel_area_w = win_w - (panel_margin * 2)
            panel_w = (panel_area_w // 4) - 20
            panel_h = win_h * 0.6
            panel_y = 130

            # Correspondance entre les clés JSON et les boutons
            cat_mapping = {
                "button_facile": "facile",
                "button_normal": "normal",
                "button_difficile": "difficile",
                "button_infini": "infinite"
            }
            difficulty_keys = ["button_facile", "button_normal", "button_difficile", "button_infini"]
            header_font = pygame.font.SysFont("Arial", int(panel_w * 0.10), bold=True)
            entry_font = pygame.font.SysFont("Arial", int(panel_w * 0.09), bold=False)
            name_label = "NOM" if current_lang == "fr" else "NAME"
            score_label = "SCORE" if current_lang == "fr" else "SCORE"

            for i, key in enumerate(difficulty_keys):
                x_pos = panel_margin + i * (panel_w + 20)
                s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
                s.fill((0, 80, 180, 175))
                screen.blit(s, (x_pos, panel_y))
                pygame.draw.rect(screen, (255, 255, 255), (x_pos, panel_y, panel_w, panel_h), 2, border_radius=8)

                diff_f = pygame.font.SysFont("Arial", int(panel_w * 0.15), bold=True)
                diff_t = diff_f.render(language_manager.get_text(key), True, (255, 255, 255))
                screen.blit(diff_t, (x_pos + (panel_w // 2 - diff_t.get_width() // 2), panel_y + 15))

                header_y = panel_y + 65
                name_surf = header_font.render(name_label, True, (255, 235, 59))
                score_surf = header_font.render(score_label, True, (255, 235, 59))
                screen.blit(name_surf, (x_pos + 15, header_y))
                screen.blit(score_surf, (x_pos + panel_w - score_surf.get_width() - 15, header_y))
                pygame.draw.line(screen, (255, 255, 255), (x_pos + 10, header_y + 25), (x_pos + panel_w - 10, header_y + 25), 1)

        # Rules popup
        if show_rules:
            overlay = pygame.Surface((win_w, win_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))
            p_w, p_h = int(win_w * 0.7), int(win_h * 0.55)
            p_rect = pygame.Rect((win_w - p_w) // 2, (win_h - p_h) // 2, p_w, p_h)
            pygame.draw.rect(screen, (255, 255, 255), p_rect, border_radius=15)
            title = "REGLES" if current_lang == "fr" else "RULES"
            intro = "Devinez le mot lettre par lettre avant que le dessin ne soit complet !" if current_lang == "fr" else "Guess the word letter by letter!"
            rules_text = [title, "", intro, "",
                          "- Facile & Normal : 7 vies" if current_lang == "fr" else "- Easy & Normal: 7 lives",
                          "- Difficile : 5 vies" if current_lang == "fr" else "- Hard: 5 lives",
                          "- Infini : Illimite" if current_lang == "fr" else "- Infinite: No limit",
                          "", "Cliquez pour fermer" if current_lang == "fr" else "Click to close"]
            for i, text in enumerate(rules_text):
                if i == 0:
                    color = (211, 47, 47)
                    size_factor = 0.08
                    is_bold = True
                elif i == 2:
                    color = (80, 80, 80)
                    size_factor = 0.05
                    is_bold = False
                else:
                    color = (60, 60, 60)
                    size_factor = 0.06
                    is_bold = False
                txt_surf = pygame.font.SysFont("Arial", int(p_h * size_factor), bold=is_bold).render(text, True, color)
                screen.blit(txt_surf, (p_rect.centerx - txt_surf.get_width() // 2, p_rect.y + 35 + (i * 32)))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_rules:
                    show_rules = False
                    continue
                if rect_door.collidepoint(event.pos):
                    running = False
                if not show_scores and rect_book.collidepoint(event.pos):
                    show_rules = True
                if rect_fr.collidepoint(event.pos):
                    language_manager.set_language("fr")
                if rect_us.collidepoint(event.pos):
                    language_manager.set_language("en")
                if rect_scores.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    show_scores = not show_scores

                # Game mode buttons click handling
                if not show_scores:
                    for r, key, color, hover_c, file_path in buttons_config:
                        if r.collidepoint(event.pos):
                            pygame_utils.play_click_sound()
                            pygame.mixer.music.stop()
                            pygame.quit()
                            subprocess.Popen([sys.executable, os.path.join(constants.BASE_DIR, "UI", file_path)])
                            sys.exit()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_gui()
