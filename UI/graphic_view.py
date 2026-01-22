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

    # Chemins des images door et book
    path_door = os.path.join(constants.BASE_DIR, "assets", "images", "door.png")
    path_book = os.path.join(constants.BASE_DIR, "assets", "images", "book.png")

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
    running = True
    while running:
        win_w, win_h = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()
        current_lang = language_manager.get_current_language()

        # Fond
        bg_scaled = pygame.transform.scale(img_background, (win_w, win_h))
        screen.blit(bg_scaled, (0, 0))

        # Logo
        logo_w = int(win_w * 0.22)
        if logo_w < 180: logo_w = 180
        logo_ratio = logo_w / img_logo.get_width()
        logo_h = int(img_logo.get_height() * logo_ratio)
        logo_scaled = pygame.transform.scale(img_logo, (logo_w, logo_h))
        screen.blit(logo_scaled, (30, 30))

        # Book (réduit à 35% de la hauteur du logo)
        book_size = int(logo_h * 0.35)
        book_scaled = pygame.transform.scale(img_book, (book_size, book_size))
        rect_book = pygame.Rect(30 + logo_w + 20, 30 + (logo_h // 3), book_size, book_size)
        screen.blit(book_scaled, rect_book)

        # Drapeaux et Porte
        flag_w = int(win_w * 0.08)
        if flag_w < 60: flag_w = 60
        flag_h = int(flag_w * 0.66)
        
        door_size = int(flag_h * 1.5)
        door_scaled = pygame.transform.scale(img_door, (door_size, door_size))

        # Positions à droite
        pos_door_x = win_w - door_size - 30
        pos_us_x = pos_door_x - flag_w - 30
        pos_fr_x = pos_us_x - flag_w - 30

        rect_fr = pygame.Rect(pos_fr_x, 30, flag_w, flag_h)
        rect_us = pygame.Rect(pos_us_x, 30, flag_w, flag_h)
        rect_door = pygame.Rect(pos_door_x, 20, door_size, door_size)

        # --- INDICATEUR DE LANGUE (Encadré jaune) ---
        if current_lang == "fr":
            pygame.draw.rect(screen, (255, 235, 59), rect_fr.inflate(10, 10), width=4, border_radius=5)
        elif current_lang == "en":
            pygame.draw.rect(screen, (255, 235, 59), rect_us.inflate(10, 10), width=4, border_radius=5)

        # Effet surbrillance drapeaux au survol
        fr_final = img_fr.copy()
        us_final = img_us.copy()
        if rect_fr.collidepoint(mouse_pos):
            fr_final.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_ADD)
        if rect_us.collidepoint(mouse_pos):
            us_final.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_ADD)

        screen.blit(pygame.transform.scale(fr_final, (flag_w, flag_h)), rect_fr)
        screen.blit(pygame.transform.scale(us_final, (flag_w, flag_h)), rect_us)
        screen.blit(door_scaled, rect_door)

        # Boutons avec grossissement
        btn_w_base = int(win_w * 0.22)
        if btn_w_base < 220: btn_w_base = 220
        btn_h_base = int(win_h * 0.09)
        if btn_h_base < 60: btn_h_base = 60

        start_y = logo_h + 80
        spacing = int(btn_h_base * 1.25)

        buttons_config = [
            (start_y, "button_facile", constants.GREEN, constants.GREEN_HOVER),
            (start_y + spacing, "button_normal", constants.ORANGE, constants.ORANGE_HOVER),
            (start_y + spacing * 2, "button_difficile", constants.RED, constants.RED_HOVER),
            (start_y + spacing * 3, "button_infini", constants.DARK_BLUE, constants.DARK_BLUE_HOVER)
        ]

        # Stockage des rects pour interaction
        rect_facile = pygame.Rect(40, start_y, btn_w_base, btn_h_base)
        rect_normal = pygame.Rect(40, start_y + spacing, btn_w_base, btn_h_base)
        rect_difficile = pygame.Rect(40, start_y + spacing * 2, btn_w_base, btn_h_base)
        rect_infini = pygame.Rect(40, start_y + spacing * 3, btn_w_base, btn_h_base)

        for y_pos, key, color, hover_c in buttons_config:
            b_rect = pygame.Rect(40, y_pos, btn_w_base, btn_h_base)
            is_hover = b_rect.collidepoint(mouse_pos)
            
            if is_hover:
                draw_rect = b_rect.inflate(24, 12)
                font_size = int(btn_h_base * 0.52)
                c = hover_c
            else:
                draw_rect = b_rect
                font_size = int(btn_h_base * 0.45)
                c = color
            
            f = pygame.font.SysFont("Arial", font_size, bold=True)
            pygame_utils.draw_rounded_button(screen, c, draw_rect, language_manager.get_text(key), f)

        # Versus et Scores
        if win_w < 600:
            rect_versus = pygame.Rect(win_w - btn_w_base - 40, win_h - (btn_h_base * 2) - 60, btn_w_base, btn_h_base)
            rect_scores = pygame.Rect(win_w - btn_w_base - 40, win_h - btn_h_base - 40, btn_w_base, btn_h_base)
        else:
            rect_versus = pygame.Rect(win_w // 2 - btn_w_base // 2, win_h - btn_h_base - 40, btn_w_base, btn_h_base)
            rect_scores = pygame.Rect(win_w - btn_w_base - 40, win_h - btn_h_base - 40, btn_w_base, btn_h_base)

        for r, key, c, hc in [(rect_versus, "button_versus", constants.PURPLE, constants.PURPLE_HOVER), (rect_scores, "button_scores", constants.GOLD, constants.GOLD_HOVER)]:
            is_h = r.collidepoint(mouse_pos)
            d_r = r.inflate(20, 10) if is_h else r
            f_s = int(btn_h_base * 0.52) if is_h else int(btn_h_base * 0.45)
            pygame_utils.draw_rounded_button(screen, hc if is_h else c, d_r, language_manager.get_text(key), pygame.font.SysFont("Arial", f_s, bold=True))

        # Pop-up des règles
        if show_rules:
            overlay = pygame.Surface((win_w, win_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))
            
            p_w, p_h = int(win_w * 0.7), int(win_h * 0.55)
            p_rect = pygame.Rect((win_w - p_w) // 2, (win_h - p_h) // 2, p_w, p_h)
            pygame.draw.rect(screen, (255, 255, 255), p_rect, border_radius=15)
            
            title = "RÈGLES" if current_lang == "fr" else "RULES"
            intro = "Devinez le mot lettre par lettre avant que le dessin ne soit complet !" if current_lang == "fr" else "Guess the word letter by letter before the drawing is complete!"
            
            rules_text = [
                title,
                "",
                intro,
                "",
                "- Facile & Normal : 7 vies" if current_lang == "fr" else "- Easy & Normal: 7 lives",
                "- Difficile : 5 vies" if current_lang == "fr" else "- Hard: 5 lives",
                "- Infini : Illimité" if current_lang == "fr" else "- Infinite: No limit",
                "",
                "Cliquez pour fermer" if current_lang == "fr" else "Click to close"
            ]
            for i, text in enumerate(rules_text):
                # Style différent pour le titre et l'intro
                if i == 0:
                    color, size_factor, is_bold = (211, 47, 47), 0.08, True
                elif i == 2:
                    color, size_factor, is_bold = (80, 80, 80), 0.05, False
                else:
                    color, size_factor, is_bold = (60, 60, 60), 0.06, False
                
                txt_surf = pygame.font.SysFont("Arial", int(p_h * size_factor), bold=is_bold).render(text, True, color)
                screen.blit(txt_surf, (p_rect.centerx - txt_surf.get_width() // 2, p_rect.y + 35 + (i * 32)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_rules:
                    show_rules = False
                    continue
                
                if rect_door.collidepoint(event.pos):
                    running = False
                
                if rect_book.collidepoint(event.pos):
                    show_rules = True

                if rect_fr.collidepoint(event.pos):
                    language_manager.set_language("fr")
                if rect_us.collidepoint(event.pos):
                    language_manager.set_language("en")

                # Lancement des scripts de jeu
                for r, m_path in [(rect_facile, "easy_mode_view.py"), (rect_normal, "normal_mode_view.py"), (rect_difficile, "hard_mode_view.py")]:
                    if r.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.Popen([sys.executable, os.path.join(constants.BASE_DIR, "UI", m_path)])
                        sys.exit()

        pygame.display.flip()

    pygame.quit()
    sys.exit()