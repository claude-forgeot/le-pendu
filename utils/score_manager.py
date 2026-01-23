import os

SCORE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'highscores.txt')


def calculate_score(state, time_remaining=0, hints_used=0):
    """
    Calculate score with formula:
    (20 * correct_letters) - (10 * wrong_letters) - (20 * hints_used) + (time_remaining * 2)
    """
    played = state.get("letters_played", [])
    secret = state.get("secret_word", "").lower()

    correct_count = 0
    wrong_count = 0
    for letter in set(played):
        if letter.lower() in secret:
            correct_count = correct_count + 1
        else:
            wrong_count = wrong_count + 1

    base_score = (20 * correct_count) - (10 * wrong_count)
    hint_penalty = 20 * hints_used
    time_bonus = int(time_remaining * 2)

    score = base_score - hint_penalty + time_bonus
    if score < 0:
        score = 0
    return score


def check_if_highscore(score, category="normal"):
    """Check if score qualifies for top 10 in a category."""
    if score <= 0:
        return False

    all_scores = _load_scores()

    if category not in all_scores:
        return True

    category_scores = all_scores.get(category, [])

    if len(category_scores) < 10:
        return True

    lowest_score = category_scores[-1]["score"]
    return score > lowest_score


def save_score(name, score, category="normal"):
    """Save score to the TXT file."""
    all_scores = _load_scores()

    if category not in all_scores:
        all_scores[category] = []

    clean_name = name[:5].upper()
    all_scores[category].append({"name": clean_name, "score": score})

    # Sort by score descending and keep top 10
    sorted_scores = []
    for entry in all_scores[category]:
        sorted_scores.append(entry)

    # Simple bubble sort (beginner-friendly)
    for i in range(len(sorted_scores)):
        for j in range(len(sorted_scores) - 1):
            if sorted_scores[j]["score"] < sorted_scores[j + 1]["score"]:
                temp = sorted_scores[j]
                sorted_scores[j] = sorted_scores[j + 1]
                sorted_scores[j + 1] = temp

    all_scores[category] = sorted_scores[:10]

    _save_scores(all_scores)


def _load_scores():
    """Load scores from TXT file."""
    if not os.path.exists(SCORE_FILE):
        return {}

    all_scores = {}
    current_category = None

    try:
        file = open(SCORE_FILE, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Check for category header [category]
            if line.startswith('[') and line.endswith(']'):
                current_category = line[1:-1]
                all_scores[current_category] = []
                continue

            # Parse name=score pairs
            if current_category and '=' in line:
                pos = line.find('=')
                name = line[:pos]
                score_str = line[pos + 1:]
                try:
                    score_val = int(score_str)
                    all_scores[current_category].append({"name": name, "score": score_val})
                except:
                    pass

    except Exception as e:
        print(f"Error loading scores: {e}")
        return {}

    return all_scores


def _save_scores(all_scores):
    """Save scores to TXT file."""
    try:
        file = open(SCORE_FILE, 'w', encoding='utf-8')

        categories = list(all_scores.keys())
        for i in range(len(categories)):
            category = categories[i]
            file.write('[' + category + ']\n')

            for entry in all_scores[category]:
                file.write(entry["name"] + '=' + str(entry["score"]) + '\n')

            # Add blank line between categories (except last)
            if i < len(categories) - 1:
                file.write('\n')

        file.close()
    except Exception as e:
        print(f"Error saving scores: {e}")