import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOCALES_FILE = os.path.join(DATA_DIR, 'locales.txt')

_locales_data = {}
_current_language = "fr"


# Load translations from locales.txt
def load_locales():
    data = {}
    current_lang = None

    try:
        file = open(LOCALES_FILE, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check for language section header [fr] or [en]
            if line.startswith('[') and line.endswith(']'):
                current_lang = line[1:-1]
                data[current_lang] = {}
                continue

            # Parse key=value pairs
            if current_lang and '=' in line:
                pos = line.find('=')
                key = line[:pos]
                value = line[pos + 1:]
                data[current_lang][key] = value

    except Exception as e:
        print(f"Error loading locales: {e}")
        return {}

    return data


# Load translations at startup
def initialize():
    global _locales_data
    _locales_data = load_locales()


# Change the active language
def set_language(language_code):
    global _current_language

    if language_code in _locales_data:
        _current_language = language_code
        return True
    else:
        return False


# Return the active language
def get_current_language():
    return _current_language


# Return the translated text for the given key
def get_text(key):
    global _locales_data, _current_language

    if _current_language not in _locales_data:
        return key

    translations = _locales_data[_current_language]

    if key in translations:
        return translations[key]
    else:
        return key


# Return the list of available languages
def get_available_languages():
    return list(_locales_data.keys())


initialize()
