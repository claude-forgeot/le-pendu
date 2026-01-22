import pygame
import sys
import os
import cv2
import random
import subprocess

# --- GESTION DE LA LANGUE VIA ARGUMENTS ---
# Par défaut FR, mais passe en US si l'argument est présent
langue_active = "FR"
if len(sys.argv) > 1 and sys.argv[1] == "US":
    langue_active = "US"

# Traductions de l'interface
interface_txt = {
    "FR": {
        "pause": "PAUSE", "cont": "CONTINUER", "reset": "RECOMMENCER", 
        "quit": "RETOUR", "win": "GAGNÉ !", "loss": "PERDU", 
        "retry": "REJOUER", "errors": "ERREURS :", "hint": "ESPACE pour rejouer"
    },
    "US": {
        "pause": "PAUSE", "cont": "CONTINUE", "reset": "RESTART", 
        "quit": "BACK", "win": "YOU WIN!", "loss": "GAME OVER", 
        "retry": "RETRY", "errors": "ERRORS :", "hint": "SPACE to restart"
    }
}
txt = interface_txt[langue_active]

# --- CONFIGURATION DES CHEMINS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = CURRENT_DIR # Puisque difficile.py est à la racine selon ton message

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "models"))
sys.path.insert(0, os.path.join(BASE_DIR, "utils"))

try:
    import game_engine
    import word_manager
except ImportError as e:
    print(f"Erreur d'importation : {e}")
    sys.exit()

# --- INITIALISATION ---
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Le Pendu - MODE DIFFICILE ({langue_active})")

# Couleurs et Polices
WHITE, RED, GOLD, GREEN = (255, 255, 255), (231, 76, 60), (241, 196, 15), (46, 204, 113)
DARK_BLUE, DARK_BLUE_H = (44, 62, 80), (52, 73, 94)
BLACK_OVERLAY = (0, 0, 0, 180)

font_mot = pygame.font.SysFont("Arial", 60, bold=True)
font_info = pygame.font.SysFont("Arial", 30, bold=True)
font_btn = pygame.font.SysFont("Arial", 20, bold=True)
font_timer = pygame.font.SysFont("Consolas", 60, bold=True)
font_fausses = pygame.font.SysFont("Arial", 20, bold=True)

# --- RESSOURCES ---
SIZE = 100 
try:
    path_bg = os.path.join(BASE_DIR, "assets", "images", "pendue.png")
    img_bg = pygame.image.load(path_bg).convert()
    img_bg = pygame.transform.scale(img_bg, (WIDTH, HEIGHT))
    
    imgs = {
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "tete.png")), (SIZE, SIZE)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "bras_droit.png")), (SIZE, SIZE)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "bras_gauche.png")), (SIZE, SIZE)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "jambe_droite.png")), (SIZE, SIZE)),
        5: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "jambe_gauche.png")), (SIZE, SIZE)),
    }
    
    music_game_path = os.path.join(BASE_DIR, "assets", "audios", "difficile.mp3")
    video_path = os.path.join(BASE_DIR, "assets", "vidéo", "losehard.mp4")
    audio_lose = os.path.join(BASE_DIR, "assets", "audios", "losehard.mp3")
    sound_click = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "audios", "click.mp3"))
except Exception as e:
    img_bg = pygame.Surface((WIDTH, HEIGHT))
    img_bg.fill((40,40,40))
    imgs = {}
    sound_click = None

btn_pause_rect = pygame.Rect(20, 20, 120, 40)

def jouer_son_clic():
    if sound_click: sound_click.play()

def retour_menu():
    jouer_son_clic()
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.quit()
    menu_path = os.path.join(BASE_DIR, "UI", "graphic_view.py")
    subprocess.Popen([sys.executable, menu_path])
    sys.exit()

def initialiser_partie():
    pygame.mixer.music.stop()
    pygame.mixer.stop() 
    if os.path.exists(music_game_path):
        pygame.mixer.music.load(music_game_path)
        pygame.mixer.music.play(-1)
    
    # Utilisation de langue_active pour le word_manager
    mot_secret = word_manager.get_word(langue_active, "difficile")
    if not mot_secret: mot_secret = "PYTHON"
    return game_engine.create_game(mot_secret, 5), mot_secret, 30.0

def play_lose_sequence(secret_word, state):
    dessiner_interface(state, secret_word, 0, pygame.mouse.get_pos())
    pygame.display.flip()
    pygame.time.delay(600)
    pygame.mixer.music.stop()
    
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 15):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)
        pygame.event.pump()

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    cap.set(cv2.CAP_PROP_POS_MSEC, 30000)
    if os.path.exists(audio_lose):
        pygame.mixer.music.load(audio_lose)
        pygame.mixer.music.play(start=30.0)

    clock = pygame.time.Clock()
    last_frame_surf = None
    while cap.isOpened():
        if cap.get(cv2.CAP_PROP_POS_MSEC) >= 44000: break
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        last_frame_surf = pygame.surfarray.make_surface(frame)
        screen.blit(last_frame_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
        pygame.event.pump()

    cap.release()
    pygame.mixer.music.stop()
    
    rect_retry = pygame.Rect(WIDTH//2 - 210, HEIGHT - 120, 200, 50)
    rect_back = pygame.Rect(WIDTH//2 + 10, HEIGHT - 120, 200, 50)

    while True:
        m_pos = pygame.mouse.get_pos()
        if last_frame_surf: screen.blit(last_frame_surf, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(BLACK_OVERLAY)
        screen.blit(overlay, (0, 0))
        
        t1 = font_mot.render(txt["loss"], True, RED)
        t2 = font_info.render(f"{secret_word}", True, WHITE)
        screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
        screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
        
        for rect, label in [(rect_retry, txt["retry"]), (rect_back, txt["quit"])]:
            over = rect.collidepoint(m_pos)
            if over: pygame.draw.rect(screen, GOLD, rect.inflate(6, 6), border_radius=12)
            pygame.draw.rect(screen, DARK_BLUE_H if over else DARK_BLUE, rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
            txt_surf = font_btn.render(label, True, WHITE)
            screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retry.collidepoint(event.pos): jouer_son_clic(); return "restart"
                if rect_back.collidepoint(event.pos): retour_menu()

def dessiner_interface(state, secret, timer, mouse_pos):
    screen.blit(img_bg, (0, 0))
    
    over_p = btn_pause_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, DARK_BLUE_H if over_p else DARK_BLUE, btn_pause_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, btn_pause_rect, 2, border_radius=10)
    txt_p = font_btn.render(txt["pause"], True, WHITE)
    screen.blit(txt_p, txt_p.get_rect(center=btn_pause_rect.center))

    timer_val = max(0, int(timer))
    timer_color = RED if timer < 10 else WHITE
    surf_timer = font_timer.render(f"{timer_val}s", True, timer_color)
    timer_rect = surf_timer.get_rect(center=(WIDTH//2, 50))
    if timer < 5 and timer > 0:
        timer_rect.x += random.randint(-3, 3)
        timer_rect.y += random.randint(-3, 3)
    screen.blit(surf_timer, timer_rect)

    tx, ty = WIDTH // 2 - SIZE // 2, 130 
    pos = {1: (tx, ty), 2: (tx - SIZE, ty + SIZE), 3: (tx + SIZE, ty + SIZE), 4: (tx - SIZE // 2, ty + 2 * SIZE), 5: (tx + SIZE // 2, ty + 2 * SIZE)}
    for i in range(1, state["errors"] + 1):
        if i in imgs: screen.blit(imgs[i], pos[i])

    masked = game_engine.get_masked_word(state)
    surf_mot = font_mot.render(" ".join(masked), True, WHITE)
    screen.blit(surf_mot, (WIDTH//2 - surf_mot.get_width()//2, HEIGHT - 180))

    lettres_fausses = [l for l in state["letters_played"] if l not in secret.lower()]
    screen.blit(font_fausses.render(txt["errors"], True, RED), (20, HEIGHT - 70))
    screen.blit(font_fausses.render(", ".join(lettres_fausses).upper(), True, WHITE), (20, HEIGHT - 40))

def main():
    game_state, secret_word, timer = initialiser_partie()
    clock = pygame.time.Clock()
    paused = False
    
    w_b, h_b = 180, 50
    rect_cont = pygame.Rect(WIDTH//2 - 280, HEIGHT//2 + 20, w_b, h_b)
    rect_reset = pygame.Rect(WIDTH//2 - 90, HEIGHT//2 + 20, w_b, h_b)
    rect_quit = pygame.Rect(WIDTH//2 + 100, HEIGHT//2 + 20, w_b, h_b)

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause_rect.collidepoint(event.pos): jouer_son_clic(); paused = not paused
                elif paused:
                    if rect_cont.collidepoint(event.pos): jouer_son_clic(); paused = False
                    if rect_reset.collidepoint(event.pos): jouer_son_clic(); game_state, secret_word, timer = initialiser_partie(); paused = False
                    if rect_quit.collidepoint(event.pos): retour_menu()
            
            if not paused and event.type == pygame.KEYDOWN and game_state["status"] == "in_progress":
                lettre = event.unicode.lower()
                if lettre.isalpha() and len(lettre) == 1 and lettre not in game_state["letters_played"]:
                    old_err = game_state["errors"]
                    game_engine.play_letter(game_state, lettre)
                    timer += 5 if game_state["errors"] == old_err else -5
                    if game_state["errors"] >= 5:
                        game_state["status"] = "loss"
                        if play_lose_sequence(secret_word, game_state) == "restart":
                            game_state, secret_word, timer = initialiser_partie(); continue

        if game_state["status"] == "in_progress" and not paused:
            timer -= dt
            if timer <= 0:
                game_state["status"] = "loss"
                if play_lose_sequence(secret_word, game_state) == "restart":
                    game_state, secret_word, timer = initialiser_partie()

        if game_state["status"] == "win":
            screen.fill((20, 40, 20))
            msg = font_info.render(f"{txt['win']} : {secret_word}", True, GREEN)
            msg2 = font_btn.render(txt["hint"], True, WHITE)
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
            screen.blit(msg2, msg2.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    jouer_son_clic(); game_state, secret_word, timer = initialiser_partie()
            continue

        dessiner_interface(game_state, secret_word, timer, mouse_pos)
        
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(BLACK_OVERLAY)
            screen.blit(overlay, (0,0))
            txt_pause = font_mot.render(txt["pause"], True, GOLD)
            screen.blit(txt_pause, txt_pause.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
            for r, label in [(rect_cont, txt["cont"]), (rect_reset, txt["reset"]), (rect_quit, txt["quit"])]:
                over = r.collidepoint(mouse_pos)
                if over: pygame.draw.rect(screen, GOLD, r.inflate(6,6), border_radius=12)
                pygame.draw.rect(screen, DARK_BLUE_H if over else DARK_BLUE, r, border_radius=10)
                pygame.draw.rect(screen, WHITE, r, 2, border_radius=10)
                t_surf = font_btn.render(label, True, WHITE)
                screen.blit(t_surf, t_surf.get_rect(center=r.center))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()