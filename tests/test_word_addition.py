#!/usr/bin/env python3

"""
Script to test word loading and addition functionality.
Run with: python3 controllers/test_word_addition.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import word_manager

print("WORD MANAGER TEST")
print("")

print("1. Testing word loading from TXT (English)")
en_words = word_manager.load_words('en')
print(f"   Loaded {len(en_words.get('facile', []))} easy English words")
print(f"   Loaded {len(en_words.get('moyen', []))} medium English words")
print(f"   Loaded {len(en_words.get('difficile', []))} hard English words")
print("")

print("2. Testing word loading from TXT (French)")
fr_words = word_manager.load_words('fr')
print(f"   Loaded {len(fr_words.get('facile', []))} easy French words")
print(f"   Loaded {len(fr_words.get('moyen', []))} medium French words")
print(f"   Loaded {len(fr_words.get('difficile', []))} hard French words")
print("")

print("3. Testing random word selection")
en_word = word_manager.get_word('en', 'facile')
fr_word = word_manager.get_word('fr', 'facile')
print(f"   Random English word (easy): {en_word}")
print(f"   Random French word (easy): {fr_word}")
print("")

print("4. Testing add_word() function")
print("   Example usage:")
print("   word_manager.add_word('en', 'python', 'moyen')")
print("   word_manager.add_word('fr', 'ordinateur', 'facile')")
print("")

print("5. Demonstrating word addition (commented out to avoid modifying files)")
print("   Uncomment the lines below to actually add words:")
print("")
print("   # Add English word to TXT")
print("   # word_manager.add_word('en', 'keyboard', 'moyen')")
print("")
print("   # Add French word to TXT")
print("   # word_manager.add_word('fr', 'clavier', 'moyen')")
print("")

print("TEST COMPLETED")
