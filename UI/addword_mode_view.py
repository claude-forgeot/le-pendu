"""
Add Word View - Gestionnaire pour ajouter des mots aux listes.
Background: addword.mp4 | Audio: addword.mp3 | Illustration: addword.png (Plein écran)
"""

import pygame
import sys
import os
import cv2
import subprocess

# Ajout du root au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import word_manager
from utils import language_manager
from UI import constants
from UI import pygame_utils

def return_to_main_menu():
    """Retourne au menu principal."""
    pygame.mixer.music.stop()
    pygame.quit()
    main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    subprocess.Popen([sys.executable, main_path if os.path.exists(main_path) else "main.py"])
    sys.exit()

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Ajouter des mots")
    
    fonts = pygame_utils.create_fonts()
    clock = pygame.time.Clock()

    # --- CHARGEMENT AUDIO ---
    audio_path = os.path.join("assets", "audios", "addword.mp3")
    if os.path.exists(audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)

    # --- CHARGEMENT VIDÉO (Background) ---
    video_path = os.path.join("assets", "images", "addword.mp4")
    video = None
    if os.path.exists(video_path):
        video = cv2.VideoCapture(video_path)

    # --- CHARGEMENT IMAGE ILLUSTRATION PLEIN ÉCRAN ---
    img_addword = None
    path_img_add = os.path.join("assets", "images", "addword.png")
    if os.path.exists(path_img_add):
        try:
            img_addword = pygame.image.load(path_img_add)
            # On redimensionne l'image pour qu'elle fasse exactement la taille de l'écran
            img_addword = pygame.transform.scale(img_addword, (constants.WIDTH, constants.HEIGHT))
        except Exception as e:
            print(f"Erreur image: {e}")

    # --- ÉTAT DE L'INTERFACE ---
    selected_category = "facile" # "facile", "normal", "difficile"
    input_text = ""
    status_msg = ""
    status_color = constants.WHITE
    
    # Rects
    btn_back_rect = pygame.Rect(20, 20, 120, 45)
    
    # Zones de clic pour catégories
    cat_rects = {
        "facile": pygame.Rect(100, 250, 200, 300),
        "normal": pygame.Rect(350, 250, 200, 300),
        "difficile": pygame.Rect(600, 250, 200, 300)
    }

    input_rect = pygame.Rect(constants.WIDTH // 2 - 200, 600, 400, 50)

    running = True
    while running:
        # 1. Dessin du fond (Vidéo ou couleur unie)
        if video:
            success, frame = video.read()
            if not success:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = video.read()
            
            if success:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                frame = cv2.flip(frame, 0)
                surf = pygame.surfarray.make_surface(frame)
                screen.blit(pygame.transform.scale(surf, (constants.WIDTH, constants.HEIGHT)), (0, 0))
        else:
            screen.fill((30, 30, 30))

        # 2. Dessin de l'image addword.png par-dessus en PLEIN ÉCRAN
        if img_addword:
            screen.blit(img_addword, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        lang = language_manager.get_current_language()

        # --- DESSIN DES 3 FENÊTRES ---
        for cat, rect in cat_rects.items():
            # Style
            is_hover = rect.collidepoint(mouse_pos)
            is_selected = (selected_category == cat)
            
            bg_color = (0, 80, 180, 180) if is_selected else (50, 50, 50, 150)
            border_color = constants.GOLD if (is_selected or is_hover) else constants.WHITE
            
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill(bg_color)
            screen.blit(s, (rect.x, rect.y))
            pygame.draw.rect(screen, border_color, rect, 3, border_radius=10)
            
            # Texte Catégorie
            cat_name = cat.upper()
            txt_cat = fonts["button"].render(cat_name, True, constants.WHITE)
            screen.blit(txt_cat, txt_cat.get_rect(center=(rect.centerx, rect.y + 40)))

        # --- CHAMP DE SAISIE ---
        pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=5)
        pygame.draw.rect(screen, constants.GOLD, input_rect, 2, border_radius=5)
        
        surf_input = fonts["info"].render(input_text + "|", True, (0, 0, 0))
        screen.blit(surf_input, (input_rect.x + 10, input_rect.y + 10))
        
        # Consignes
        label = "Tapez un mot et appuyez sur ENTRÉE :" if lang == "fr" else "Type a word and press ENTER:"
        surf_label = fonts["small"].render(label, True, constants.WHITE)
        screen.blit(surf_label, (input_rect.x, input_rect.y - 30))

        # Message de statut
        if status_msg:
            surf_status = fonts["small"].render(status_msg, True, status_color)
            screen.blit(surf_status, (input_rect.x, input_rect.y + 60))

        # --- BOUTON RETOUR ---
        pygame_utils.draw_button_with_border(screen, btn_back_rect, constants.RED, (200, 0, 0), mouse_pos, "RETOUR", fonts["button"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back_rect.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return_to_main_menu()
                
                for cat, rect in cat_rects.items():
                    if rect.collidepoint(event.pos):
                        pygame_utils.play_click_sound()
                        selected_category = cat
                        status_msg = ""

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(input_text.strip()) > 2:
                        # Ajout du mot via le manager
                        word_manager.add_word(lang, selected_category, input_text.strip().upper())
                        status_msg = f"Mot '{input_text.upper()}' ajouté à {selected_category} !"
                        status_color = constants.GREEN
                        input_text = ""
                    else:
                        status_msg = "Mot trop court !"
                        status_color = constants.RED
                else:
                    # On limite la saisie à des lettres
                    if event.unicode.isalpha() and len(input_text) < 15:
                        input_text += event.unicode.upper()

        pygame.display.flip()
        clock.tick(30)

    if video:
        video.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()