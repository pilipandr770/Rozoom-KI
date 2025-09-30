with open('app/translations/uk/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')
    empty_translations = []
    for i, line in enumerate(lines):
        if line.strip() == 'msgstr ""':
            # Check if this is not a header
            if i > 10:  # Skip header section
                empty_translations.append(i+1)
    if empty_translations:
        print(f'Found {len(empty_translations)} empty translations at lines: {empty_translations[:10]}')
    else:
        print('No empty translations found!')