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


# Draw gallows and body parts progressively based on error count (0-7)
def draw_hangman(surface, errors, x, y, color=None):
    if color is None:
        color = constants.WHITE

    line_width = 4
    head_radius = 25
    body_length = 80
    arm_length = 50
    leg_length = 60

    # Gallows position
    base_x = x + 50
    base_y = y + 250
    pole_height = 200
    beam_length = 100
    rope_length = 30

    # Always draw the gallows (base, pole, beam)
    pygame.draw.line(surface, color, (base_x - 40, base_y), (base_x + 40, base_y), line_width)
    pygame.draw.line(surface, color, (base_x, base_y), (base_x, base_y - pole_height), line_width)
    pygame.draw.line(surface, color, (base_x, base_y - pole_height), (base_x + beam_length, base_y - pole_height), line_width)

    # Person position
    head_x = base_x + beam_length
    rope_top = base_y - pole_height
    head_y = rope_top + rope_length + head_radius
    body_top = head_y + head_radius
    body_bottom = body_top + body_length
    arm_y = body_top + 20

    # Error 1: Head
    if errors >= 1:
        pygame.draw.circle(surface, color, (head_x, head_y), head_radius, line_width)

    # Error 2: Body
    if errors >= 2:
        pygame.draw.line(surface, color, (head_x, body_top), (head_x, body_bottom), line_width)

    # Error 3: Left arm
    if errors >= 3:
        pygame.draw.line(surface, color, (head_x, arm_y), (head_x - arm_length, arm_y + 30), line_width)

    # Error 4: Right arm
    if errors >= 4:
        pygame.draw.line(surface, color, (head_x, arm_y), (head_x + arm_length, arm_y + 30), line_width)

    # Error 5: Left leg
    if errors >= 5:
        pygame.draw.line(surface, color, (head_x, body_bottom), (head_x - 30, body_bottom + leg_length), line_width)

    # Error 6: Right leg
    if errors >= 6:
        pygame.draw.line(surface, color, (head_x, body_bottom), (head_x + 30, body_bottom + leg_length), line_width)

    # Error 7: Rope (final - person is hanged)
    if errors >= 7:
        pygame.draw.line(surface, color, (head_x, rope_top), (head_x, head_y - head_radius), line_width)


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


# Render masked word with adaptive font size to fit screen width
def render_word_adaptive(masked_word, max_width, color=None):
    if color is None:
        color = constants.WHITE

    spaced_word = " ".join(masked_word)
    font_size = 60

    while font_size > 20:
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        surf = font.render(spaced_word, True, color)
        if surf.get_width() <= max_width:
            return surf
        font_size -= 5

    font = pygame.font.SysFont("Arial", 20, bold=True)
    return font.render(spaced_word, True, color)


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
