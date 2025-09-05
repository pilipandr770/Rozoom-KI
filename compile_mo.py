from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

with open('app/translations/de/LC_MESSAGES/messages.po', 'rb') as f:
    catalog = read_po(f)

with open('app/translations/de/LC_MESSAGES/messages.mo', 'wb') as f:
    write_mo(f, catalog)

print("Файл messages.mo успешно скомпилирован.")
