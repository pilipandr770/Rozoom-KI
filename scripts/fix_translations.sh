#!/bin/bash
# fix_translations.sh - Fix duplicate messages in German translation file

# Set text color variables
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔍 Starting German translation file cleanup...${NC}"

# Define paths
TRANSLATIONS_DIR="/opt/render/project/src/app/translations"
DE_PO_PATH="$TRANSLATIONS_DIR/de/LC_MESSAGES/messages.po"

# Check if the file exists
if [ ! -f "$DE_PO_PATH" ]; then
    echo -e "${RED}Error: Could not find German translation file at $DE_PO_PATH${NC}"
    exit 1
fi

# Create a backup of the file
BACKUP_PATH="${DE_PO_PATH}.bak"
cp "$DE_PO_PATH" "$BACKUP_PATH"
echo -e "${GREEN}✅ Created backup at $BACKUP_PATH${NC}"

# Fix duplicates using a temporary Python script
TMP_SCRIPT=$(mktemp)
cat > "$TMP_SCRIPT" << 'EOF'
#!/usr/bin/env python3
import re
import sys
from collections import OrderedDict

def fix_duplicate_translations(file_path):
    """
    Remove duplicate message definitions from a PO file.
    """
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
    
    print(f"✅ Removed {duplicates} duplicate entries")
    print(f"✅ Original entries: {len(entries)}")
    print(f"✅ Cleaned entries: {len(unique_entries)}")
    
    return duplicates

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <path-to-po-file>")
        sys.exit(1)
        
    fix_duplicate_translations(sys.argv[1])
EOF

# Make the script executable
chmod +x "$TMP_SCRIPT"

# Run the Python script
echo -e "${CYAN}Running cleanup script...${NC}"
python3 "$TMP_SCRIPT" "$DE_PO_PATH"

# Remove the temporary script
rm "$TMP_SCRIPT"

# Compile translations
echo -e "\n${CYAN}🔄 Compiling translations...${NC}"
cd "$TRANSLATIONS_DIR"
if pybabel compile -d .; then
    echo -e "${GREEN}✅ Translations successfully compiled${NC}"
else
    echo -e "${RED}❌ Failed to compile translations${NC}"
fi

echo -e "\n${CYAN}✨ Translation cleanup complete! ✨${NC}"
