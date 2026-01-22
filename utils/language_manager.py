import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOCALES_FILE = os.path.join(DATA_DIR, 'locales.json')

_locales_data = {}
_current_language = "fr"


# Load translations from locales.json
def load_locales():
    file = open(LOCALES_FILE, 'r', encoding='utf-8')
    data = json.load(file)
    file.close()
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

    translations = _locales_data[_current_language]

    if key in translations:
        return translations[key]
    else:
        return key


# Return the list of available languages
def get_available_languages():
    return list(_locales_data.keys())


initialize()
