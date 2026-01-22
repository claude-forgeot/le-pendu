"""
Add Word view for the Hangman game.
Allows users to add new words to the game database with a graphical interface.
"""

import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from UI import constants
from UI import pygame_utils
from utils import language_manager
from utils import word_manager


def main():
    """Main function for the Add Word GUI."""
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Le Pendu - Ajouter un Mot")

    try:
        img_background = pygame.image.load(constants.IMG_BACKGROUND_HOME)
        img_background = pygame.transform.scale(img_background, (constants.WIDTH, constants.HEIGHT))
    except:
        img_background = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        img_background.fill((40, 40, 60))

    fonts = pygame_utils.create_fonts()
    pygame_utils.load_sounds()

    current_language = language_manager.get_current_language()
    selected_difficulty = "facile"
    input_text = ""
    message = ""
    message_color = constants.WHITE
    active = False

    input_rect = pygame.Rect(constants.WIDTH // 2 - 200, 200, 400, 50)

    btn_w, btn_h = 120, 50
    btn_facile = pygame.Rect(constants.WIDTH // 2 - 270, 300, btn_w, btn_h)
    btn_moyen = pygame.Rect(constants.WIDTH // 2 - 60, 300, btn_w, btn_h)
    btn_difficile = pygame.Rect(constants.WIDTH // 2 + 150, 300, btn_w, btn_h)

    btn_add = pygame.Rect(constants.WIDTH // 2 - 110, 400, 220, 60)
    btn_back = pygame.Rect(20, constants.HEIGHT - 70, 150, 50)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(img_background, (0, 0))

        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        title_text = language_manager.get_text("add_word_title") if "add_word_title" in language_manager._locales_data[current_language] else "Ajouter un Mot"
        title_surf = fonts["word"].render(title_text, True, constants.GOLD)
        screen.blit(title_surf, (constants.WIDTH // 2 - title_surf.get_width() // 2, 50))

        lang_text = "Langue: Francais (JSON)" if current_language == "fr" else "Language: English (TXT)"
        lang_surf = fonts["button"].render(lang_text, True, constants.WHITE)
        screen.blit(lang_surf, (constants.WIDTH // 2 - lang_surf.get_width() // 2, 120))

        word_label = fonts["info"].render("Mot:", True, constants.WHITE)
        screen.blit(word_label, (input_rect.x, input_rect.y - 35))

        color = constants.GOLD if active else constants.WHITE
        pygame.draw.rect(screen, color, input_rect, 3, border_radius=10)
        text_surface = fonts["info"].render(input_text, True, constants.WHITE)
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        diff_label = fonts["info"].render("Difficulte:", True, constants.WHITE)
        screen.blit(diff_label, (constants.WIDTH // 2 - diff_label.get_width() // 2, 270))

        for btn, diff, color_normal, color_hover in [
            (btn_facile, "facile", constants.GREEN, constants.GREEN_HOVER),
            (btn_moyen, "moyen", constants.ORANGE, constants.ORANGE_HOVER),
            (btn_difficile, "difficile", constants.RED, constants.RED_HOVER)
        ]:
            if diff == selected_difficulty:
                pygame.draw.rect(screen, constants.GOLD, btn.inflate(6, 6), border_radius=12)

            is_hover = btn.collidepoint(mouse_pos)
            btn_color = color_hover if is_hover else color_normal
            pygame.draw.rect(screen, btn_color, btn, border_radius=10)
            pygame.draw.rect(screen, constants.WHITE, btn, 2, border_radius=10)

            text = fonts["button"].render(diff.capitalize(), True, constants.WHITE)
            screen.blit(text, (btn.centerx - text.get_width() // 2, btn.centery - text.get_height() // 2))

        add_hover = btn_add.collidepoint(mouse_pos)
        add_color = constants.DARK_BLUE_HOVER if add_hover else constants.DARK_BLUE
        pygame.draw.rect(screen, add_color, btn_add, border_radius=15)
        pygame.draw.rect(screen, constants.WHITE, btn_add, 3, border_radius=15)
        add_text = fonts["info"].render("Ajouter", True, constants.WHITE)
        screen.blit(add_text, (btn_add.centerx - add_text.get_width() // 2, btn_add.centery - add_text.get_height() // 2))

        back_hover = btn_back.collidepoint(mouse_pos)
        back_color = constants.PURPLE_HOVER if back_hover else constants.PURPLE
        pygame.draw.rect(screen, back_color, btn_back, border_radius=10)
        pygame.draw.rect(screen, constants.WHITE, btn_back, 2, border_radius=10)
        back_text = fonts["button"].render("Retour", True, constants.WHITE)
        screen.blit(back_text, (btn_back.centerx - back_text.get_width() // 2, btn_back.centery - back_text.get_height() // 2))

        if message:
            msg_surf = fonts["button"].render(message, True, message_color)
            screen.blit(msg_surf, (constants.WIDTH // 2 - msg_surf.get_width() // 2, 480))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if btn_facile.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    selected_difficulty = "facile"
                    message = ""

                if btn_moyen.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    selected_difficulty = "moyen"
                    message = ""

                if btn_difficile.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    selected_difficulty = "difficile"
                    message = ""

                if btn_add.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    if input_text.strip():
                        success = word_manager.add_word(current_language, input_text.strip(), selected_difficulty)
                        if success:
                            message = f"Mot '{input_text}' ajoute avec succes!"
                            message_color = constants.GREEN
                            input_text = ""
                        else:
                            message = f"Erreur: Mot deja existant ou invalide"
                            message_color = constants.RED
                    else:
                        message = "Erreur: Le mot ne peut pas etre vide"
                        message_color = constants.RED

                if btn_back.collidepoint(event.pos):
                    pygame_utils.play_click_sound()
                    import subprocess
                    pygame.quit()
                    main_path = os.path.join(constants.BASE_DIR, "main.py")
                    subprocess.Popen([sys.executable, main_path])
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip():
                            success = word_manager.add_word(current_language, input_text.strip(), selected_difficulty)
                            if success:
                                message = f"Mot '{input_text}' ajoute avec succes!"
                                message_color = constants.GREEN
                                input_text = ""
                            else:
                                message = f"Erreur: Mot deja existant ou invalide"
                                message_color = constants.RED
                        else:
                            message = "Erreur: Le mot ne peut pas etre vide"
                            message_color = constants.RED
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        message = ""
                    else:
                        if event.unicode.isalpha() or event.unicode in [' ', '-']:
                            input_text += event.unicode
                            message = ""

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
