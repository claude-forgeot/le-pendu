"""
Add Word View - Gestionnaire pour ajouter des mots aux listes.
Background: addword.mp4 | Audio: addword.mp3 | Illustration: addword.png (Plein écran)
Features: Language selection via flags (france.png, usa.png), input top, category selection via click.
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
            img_addword = pygame.transform.scale(img_addword, (constants.WIDTH, constants.HEIGHT))
        except Exception as e:
            print(f"Erreur image: {e}")

    # --- CHARGEMENT DRAPEAUX ---
    flags = {}
    flag_size = (60, 40)
    try:
        fr_flag = pygame.image.load(os.path.join("assets", "images", "france.png")).convert_alpha()
        en_flag = pygame.image.load(os.path.join("assets", "images", "usa.png")).convert_alpha()
        flags["fr"] = pygame.transform.scale(fr_flag, flag_size)
        flags["en"] = pygame.transform.scale(en_flag, flag_size)
    except:
        flags["fr"] = pygame.Surface(flag_size); flags["fr"].fill((0, 0, 255))
        flags["en"] = pygame.Surface(flag_size); flags["en"].fill((255, 0, 0))

    # --- TRADUCTIONS DES CATÉGORIES ---
    cat_labels = {
        "fr": {"facile": "FACILE", "normal": "NORMAL", "difficile": "DIFFICILE"},
        "en": {"facile": "EASY", "normal": "NORMAL", "difficile": "HARD"}
    }

    # --- ÉTAT DE L'INTERFACE ---
    input_text = ""
    status_msg = ""
    status_color = constants.WHITE
    
    btn_back_rect = pygame.Rect(20, 20, 120, 45)
    rect_fr = pygame.Rect(constants.WIDTH - 150, 25, flag_size[0], flag_size[1])
    rect_en = pygame.Rect(constants.WIDTH - 80, 25, flag_size[0], flag_size[1])
    input_rect = pygame.Rect(constants.WIDTH // 2 - 200, 150, 400, 50)
    
    cat_rects = {
        "facile": pygame.Rect(100, 300, 200, 300),
        "normal": pygame.Rect(350, 300, 200, 300),
        "difficile": pygame.Rect(600, 300, 200, 300)
    }

    running = True
    while running:
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

        if img_addword:
            screen.blit(img_addword, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        lang = language_manager.get_current_language()

        # --- DESSIN DRAPEAUX ---
        screen.blit(flags["fr"], rect_fr)
        screen.blit(flags["en"], rect_en)
        active_rect = rect_fr if lang == "fr" else rect_en
        pygame.draw.rect(screen, constants.GOLD, active_rect, 3, border_radius=2)

        # --- DESSIN DU CHAMP DE SAISIE ---
        pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=5)
        pygame.draw.rect(screen, constants.GOLD, input_rect, 2, border_radius=5)
        
        surf_input = fonts["info"].render(input_text + "|", True, (0, 0, 0))
        screen.blit(surf_input, (input_rect.x + 10, input_rect.y + 10))
        
        label_top = "1. Tapez le mot ici :" if lang == "fr" else "1. Type the word here:"
        surf_label_top = fonts["small"].render(label_top, True, constants.WHITE)
        screen.blit(surf_label_top, (input_rect.x, input_rect.y - 30))

        # --- DESSIN DES 3 FENÊTRES DE CATÉGORIE ---
        label_mid = "2. Cliquez sur une catégorie pour ajouter :" if lang == "fr" else "2. Click a category to add:"
        surf_label_mid = fonts["small"].render(label_mid, True, constants.GOLD)
        screen.blit(surf_label_mid, (constants.WIDTH // 2 - surf_label_mid.get_width() // 2, 260))

        for cat_id, rect in cat_rects.items():
            is_hover = rect.collidepoint(mouse_pos)
            bg_color = (0, 80, 180, 180) if is_hover else (50, 50, 50, 150)
            border_color = constants.GOLD if is_hover else constants.WHITE
            
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill(bg_color)
            screen.blit(s, (rect.x, rect.y))
            pygame.draw.rect(screen, border_color, rect, 3, border_radius=10)
            
            # Texte traduit
            display_name = cat_labels[lang][cat_id]
            txt_cat = fonts["button"].render(display_name, True, constants.WHITE)
            screen.blit(txt_cat, txt_cat.get_rect(center=(rect.centerx, rect.centery)))

        # Message de statut
        if status_msg:
            surf_status = fonts["small"].render(status_msg, True, status_color)
            screen.blit(surf_status, (constants.WIDTH // 2 - surf_status.get_width() // 2, 620))

        # --- BOUTON RETOUR ---
        back_text = "RETOUR" if lang == "fr" else "BACK"
        pygame_utils.draw_button_with_border(screen, btn_back_rect, constants.RED, (200, 0, 0), mouse_pos, back_text, fonts["button"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back_rect.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    return_to_main_menu()
                
                if rect_fr.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    language_manager.set_language("fr")
                    status_msg = ""
                if rect_en.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    language_manager.set_language("en")
                    status_msg = ""
                
                for cat_id, rect in cat_rects.items():
                    if rect.collidepoint(event.pos):
                        if len(input_text.strip()) > 2:
                            pygame_utils.play_click_sound()
                            word_to_add = input_text.strip().upper()
                            word_manager.add_word(lang, cat_id, word_to_add)
                            
                            if lang == "fr":
                                status_msg = f"'{word_to_add}' ajouté en {cat_labels['fr'][cat_id]} !"
                            else:
                                status_msg = f"'{word_to_add}' added to {cat_labels['en'][cat_id]} !"
                                
                            status_color = constants.GREEN
                            input_text = ""
                        else:
                            status_msg = "Mot trop court !" if lang == "fr" else "Word too short!"
                            status_color = constants.RED

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
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