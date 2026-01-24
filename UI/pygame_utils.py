import pygame

from UI import constants


# Create and return dictionary of commonly used fonts
def create_fonts():
    return {
        "word": pygame.font.SysFont("Arial", 60, bold=True),
        "info": pygame.font.SysFont("Arial", 30, bold=True),
        "button": pygame.font.SysFont("Arial", 20, bold=True),
        "timer": pygame.font.SysFont("Consolas", 60, bold=True),
        "small": pygame.font.SysFont("Arial", 20, bold=True),
    }


# Load and scale hangman body part images
def load_hangman_images(size=None):
    if size is None:
        size = constants.HANGMAN_SPRITE_SIZE

    images = {}
    image_paths = {
        1: constants.IMG_HEAD,
        2: constants.IMG_RIGHT_ARM,
        3: constants.IMG_LEFT_ARM,
        4: constants.IMG_RIGHT_LEG,
        5: constants.IMG_LEFT_LEG,
    }

    for key, path in image_paths.items():
        try:
            img = pygame.image.load(path)
            images[key] = pygame.transform.scale(img, (size, size))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")

    return images


# Load sound effects (placeholder for future sounds)
def load_sounds():
    pass


# Play click sound (disabled - click.ogg file missing)
def play_click_sound():
    pass


# Draw a rounded button with centered text
def draw_rounded_button(surface, color, rect, text, font, text_color=None):
    if text_color is None:
        text_color = constants.WHITE

    pygame.draw.rect(surface, color, rect, border_radius=int(rect.height / 3))
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


# Draw a button with border and hover effect
def draw_button_with_border(surface, rect, color, hover_color, mouse_pos, label, font):
    is_hover = rect.collidepoint(mouse_pos)

    if is_hover:
        pygame.draw.rect(surface, constants.GOLD, rect.inflate(6, 6), border_radius=12)

    pygame.draw.rect(
        surface,
        hover_color if is_hover else color,
        rect,
        border_radius=10
    )
    pygame.draw.rect(surface, constants.WHITE, rect, 2, border_radius=10)

    text_surf = font.render(label, True, constants.WHITE)
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))

    return is_hover
