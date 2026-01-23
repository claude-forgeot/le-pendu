import json
import os

SCORE_FILE = "highscores.json"

def calculate_score(state):
    """Calcule le score selon la formule : 20 * justes - 10 * fausses."""
    played = state.get("letters_played", [])
    secret = state.get("secret_word", "").lower()
    
    correct_count = sum(1 for letter in set(played) if letter.lower() in secret)
    wrong_count = sum(1 for letter in set(played) if letter.lower() not in secret)
    
    score = (20 * correct_count) - (10 * wrong_count)
    return max(0, score)

def check_if_highscore(score, category="normal"):
    """Vérifie si le score mérite d'entrer dans le top 10 d'une catégorie."""
    if score <= 0: return False
    
    all_scores = _load_scores()
    # Si la catégorie n'existe pas encore, c'est forcément un record
    if category not in all_scores: return True
    
    category_scores = all_scores.get(category, [])
    
    if len(category_scores) < 10: return True
    return score > category_scores[-1]["score"]

def save_score(name, score, category="normal"):
    """Enregistre le score sans effacer les autres catégories."""
    all_scores = _load_scores()
    
    # On initialise la catégorie si elle n'existe pas, sans toucher aux autres
    if category not in all_scores:
        all_scores[category] = []
        
    all_scores[category].append({"name": name[:5].upper(), "score": score})
    
    # Tri et limitation au top 10
    all_scores[category] = sorted(all_scores[category], key=lambda x: x["score"], reverse=True)[:10]
    
    # Sauvegarde sécurisée
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(all_scores, f, indent=4)
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier : {e}")

def _load_scores():
    """Charge les scores avec vérification de l'intégrité du JSON."""
    if not os.path.exists(SCORE_FILE):
        return {}
    
    try:
        with open(SCORE_FILE, "r") as f:
            # On vérifie que le fichier n'est pas vide
            content = f.read().strip()
            if not content:
                return {}
            
            data = json.loads(content)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erreur de lecture JSON (Fichier corrompu ?) : {e}")
        # IMPORTANT : Si le fichier est corrompu, on pourrait ici retourner une 
        # erreur fatale plutôt que de renvoyer {} pour éviter d'écraser le fichier.
        return {}