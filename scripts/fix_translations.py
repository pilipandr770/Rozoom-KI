#!/usr/bin/env python3
"""
This script fixes duplicate message definitions in the German translation file.

It reads the messages.po file, identifies and removes duplicate message entries,
and saves a clean version of the file.
"""

import re
import os
import shutil
from collections import OrderedDict

def fix_duplicate_translations(file_path):
    """
    Remove duplicate message definitions from a PO file.
    
    Args:
        file_path (str): Path to the PO file to fix
        
    Returns:
        int: Number of duplicates removed
    """
    # Create a backup of the original file
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"✓ Created backup at {backup_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the file into header and entries
    header_pattern = r'^(msgid ""\s+msgstr "".*?)(?=\s*msgid)'
    header_match = re.search(header_pattern, content, re.DOTALL | re.MULTILINE)
    
    if not header_match:
        print("Error: Could not identify file header")
        return 0
        
    header = header_match.group(1)
    
    # Extract all message entries
    entry_pattern = r'(msgid ".*?"(?:\s+msgstr ".*?")+)'
    entries = re.findall(entry_pattern, content, re.DOTALL)
    
    # Process entries and remove duplicates
    unique_entries = OrderedDict()
    duplicates = 0
    
    for entry in entries:
        # Extract the msgid
        msgid_match = re.search(r'msgid "(.*?)"', entry, re.DOTALL)
        if not msgid_match:
            continue
            
        msgid = msgid_match.group(1)
        
        # Skip empty msgid (should only be in header)
        if not msgid:
            continue
            
        # If this is a duplicate, don't add it again
        if msgid in unique_entries:
            duplicates += 1
            continue
            
        # Add to our unique entries
        unique_entries[msgid] = entry
    
    # Reconstruct the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write('\n\n')
        f.write('\n\n'.join(unique_entries.values()))
    
    print(f"✓ Removed {duplicates} duplicate entries")
    print(f"✓ Original entries: {len(entries)}")
    print(f"✓ Cleaned entries: {len(unique_entries)}")
    
    return duplicates

def main():
    """
    Main function to fix duplicate translations
    """
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the translations directory
    translations_dir = os.path.join(script_dir, '..', 'app', 'translations')
    de_po_path = os.path.join(translations_dir, 'de', 'LC_MESSAGES', 'messages.po')
    
    # Ensure the file exists
    if not os.path.exists(de_po_path):
        print(f"Error: Could not find file at {de_po_path}")
        return 1
    
    # Fix duplicates
    duplicates = fix_duplicate_translations(de_po_path)
    
    if duplicates > 0:
        print(f"✓ Fixed {duplicates} duplicate entries in the German translation file")
    else:
        print("No duplicate entries found in the German translation file")
    
    # Compile the translations
    compile_command = f"cd {translations_dir} && pybabel compile -d ."
    print(f"\nTo compile the translations, run:\n{compile_command}")
    
    return 0

if __name__ == "__main__":
    main()
