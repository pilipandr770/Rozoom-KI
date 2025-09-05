"""
Script to append new translations to the messages.po file.
"""
import os

def append_translations():
    # Path to the new translations file
    new_translations_file = 'dashboard_translations.txt'
    # Path to the existing messages.po file
    messages_po_file = 'app/translations/de/LC_MESSAGES/messages.po'
    
    # Read the new translations
    with open(new_translations_file, 'r', encoding='utf-8') as f:
        new_translations = f.read()
    
    # Append the new translations to the messages.po file
    with open(messages_po_file, 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write(new_translations)
    
    print(f"Successfully appended translations to {messages_po_file}")

if __name__ == '__main__':
    append_translations()
