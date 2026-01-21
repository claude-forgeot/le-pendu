"""
Module graphic_view - Interface graphique Pygame pour le jeu du Pendu
Contient toute la logique de l'interface utilisateur avec Pygame
"""
import pygame
import sys

def draw_rounded_button(surface, color, rect, text, font):
    """
    Dessine un bouton arrondi avec texte centré

    Args:
        surface: Surface Pygame où dessiner
        color: Couleur du bouton et du texte
        rect: Rectangle définissant la position et taille du bouton
        text: Texte à afficher sur le bouton
        font: Police Pygame pour le texte
    """
    pygame.draw.rect(surface, color, rect, border_radius=int(rect.height / 3))
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def main_gui():
    """
    Fonction principale de l'interface graphique Pygame
    Affiche le menu principal avec les modes de jeu et options de langue
    """
    # Initialisation de Pygame
    pygame.init()
    pygame.mixer.init()

    # Configuration initiale (Fenêtre redimensionnable - Taille réduite au lancement)
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Le Pendu - Interface Responsive")

    # Couleurs
    WHITE = (255, 255, 255)
    GREEN = (46, 204, 113)
    ORANGE = (230, 126, 34)
    RED = (231, 76, 60)
    DARK_BLUE = (44, 62, 80)
    PURPLE = (155, 89, 182)
    GOLD = (241, 196, 15)

    # Couleurs Hover
    GREEN_H = (82, 222, 139)
    ORANGE_H = (255, 159, 67)
    RED_H = (255, 107, 91)
    DARK_BLUE_H = (52, 73, 94)
    PURPLE_H = (187, 143, 206)
    GOLD_H = (244, 208, 63)

    # Chargement des ressources
    try:
        # Modification des chemins vers les images
        img_background = pygame.image.load("./assets/images/home.jpg")
        img_logo = pygame.image.load("./assets/images/logo.png")
        img_fr = pygame.image.load("./assets/images/france.png")
        img_us = pygame.image.load("./assets/images/usa.png")

        # Modification du chemin vers l'audio
        pygame.mixer.music.load("./assets/audios/main.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Erreur de chargement des ressources : {e}")
        pygame.quit()
        sys.exit()

    running = True
    while running:
        win_w, win_h = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()

        # Background
        bg_scaled = pygame.transform.scale(img_background, (win_w, win_h))
        screen.blit(bg_scaled, (0, 0))

        # Logo responsive (Taille diminuée)
        logo_w = int(win_w * 0.22)
        if logo_w < 180: logo_w = 180
        logo_ratio = logo_w / img_logo.get_width()
        logo_h = int(img_logo.get_height() * logo_ratio)
        logo_scaled = pygame.transform.scale(img_logo, (logo_w, logo_h))
        screen.blit(logo_scaled, (30, 30))

        # Drapeaux en haut à droite (Taille augmentée)
        flag_w = int(win_w * 0.08)
        if flag_w < 60: flag_w = 60
        flag_h = int(flag_w * 0.66)

        fr_scaled = pygame.transform.scale(img_fr, (flag_w, flag_h))
        us_scaled = pygame.transform.scale(img_us, (flag_w, flag_h))

        # Positionnement des drapeaux
        screen.blit(us_scaled, (win_w - flag_w - 30, 30))
        screen.blit(fr_scaled, (win_w - (flag_w * 2) - 60, 30))

        # Dimensions des boutons
        btn_w = int(win_w * 0.22)
        if btn_w < 220: btn_w = 220
        btn_h = int(win_h * 0.09)
        if btn_h < 60: btn_h = 60

        font_size = int(btn_h * 0.45)
        font = pygame.font.SysFont("Arial", font_size, bold=True)

        spacing = int(btn_h * 1.25)
        start_y = logo_h + 60

        # Rectangles des boutons
        rect_facile = pygame.Rect(40, start_y, btn_w, btn_h)
        rect_normal = pygame.Rect(40, start_y + spacing, btn_w, btn_h)
        rect_difficile = pygame.Rect(40, start_y + spacing * 2, btn_w, btn_h)
        rect_infini = pygame.Rect(40, start_y + spacing * 3, btn_w, btn_h)

        # Logique pour placer VERSUS et SCORES à droite si la fenêtre est étroite
        if win_w < 600: # Seuil "format téléphone"
            pos_x_bas = win_w - btn_w - 40
            rect_versus = pygame.Rect(pos_x_bas, win_h - (btn_h * 2) - 60, btn_w, btn_h)
            rect_scores = pygame.Rect(pos_x_bas, win_h - btn_h - 40, btn_w, btn_h)
        else:
            rect_versus = pygame.Rect(win_w // 2 - btn_w // 2, win_h - btn_h - 40, btn_w, btn_h)
            rect_scores = pygame.Rect(win_w - btn_w - 40, win_h - btn_h - 40, btn_w, btn_h)

        def get_color(rect, normal_c, hover_c):
            """Retourne la couleur hover si la souris est sur le bouton"""
            return hover_c if rect.collidepoint(mouse_pos) else normal_c

        # Dessin des boutons
        draw_rounded_button(screen, get_color(rect_facile, GREEN, GREEN_H), rect_facile, "FACILE", font)
        draw_rounded_button(screen, get_color(rect_normal, ORANGE, ORANGE_H), rect_normal, "NORMAL", font)
        draw_rounded_button(screen, get_color(rect_difficile, RED, RED_H), rect_difficile, "DIFFICILE", font)
        draw_rounded_button(screen, get_color(rect_infini, DARK_BLUE, DARK_BLUE_H), rect_infini, "INFINI", font)
        draw_rounded_button(screen, get_color(rect_versus, PURPLE, PURPLE_H), rect_versus, "VERSUS", font)
        draw_rounded_button(screen, get_color(rect_scores, GOLD, GOLD_H), rect_scores, "SCORES", font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_facile.collidepoint(event.pos): print("Mode Facile")
                # Détection clic drapeaux
                fr_rect = pygame.Rect(win_w - (flag_w * 2) - 60, 30, flag_w, flag_h)
                us_rect = pygame.Rect(win_w - flag_w - 30, 30, flag_w, flag_h)
                if fr_rect.collidepoint(event.pos): print("Langue : FR")
                if us_rect.collidepoint(event.pos): print("Language : US")

        pygame.display.flip()

    pygame.quit()
    sys.exit()
