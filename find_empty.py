with open('app/translations/uk/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')
    empty_translations = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == 'msgstr ""':
            # Check if the next lines are also empty or just quotes
            j = i + 1
            is_really_empty = True
            while j < len(lines) and lines[j].startswith('"'):
                if lines[j].strip() != '""':
                    is_really_empty = False
                    break
                j += 1
            if is_really_empty:
                # Find the msgid above
                msgid_start = i - 1
                msgid_lines = []
                while msgid_start >= 0 and not lines[msgid_start].startswith('msgid'):
                    msgid_start -= 1
                if msgid_start >= 0:
                    # Collect msgid content
                    k = msgid_start
                    while k < i and (lines[k].startswith('msgid') or lines[k].startswith('"')):
                        msgid_lines.append(lines[k])
                        k += 1
                    msgid_text = '\n'.join(msgid_lines)
                    empty_translations.append((i+1, msgid_text))
        i += 1

    print(f'Found {len(empty_translations)} truly empty translations:')
    for line_num, msgid in empty_translations[:20]:  # Show first 20
        print(f'Line {line_num}: {msgid[:100]}...')