import os
import re
import shutil

def extract_top_strings(input_file, output_file, count=50):
    """Извлечь наиболее важные строки из файла с пропущенными переводами и добавить их в .po файл"""
    # Читаем существующие переводы
    existing_translations = set()
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            pattern = re.compile(r'msgid "(.*?)"')
            existing_translations = set(pattern.findall(content))
    
    # Чтение всех строк из файла с пропущенными переводами
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Находим строки с msgid
    msgid_pattern = re.compile(r'msgid "(.*?)"')
    extracted_strings = []
    i = 0
    
    while i < len(lines):
        match = msgid_pattern.search(lines[i])
        if match and match.group(1) not in existing_translations:
            text = match.group(1)
            if len(text) > 2 and not text.startswith('{') and not text.startswith('%'):
                # Переводим строку на немецкий (здесь просто заглушка, в реальности нужен перевод)
                german_translation = suggest_german_translation(text)
                extracted_strings.append((text, german_translation))
                if len(extracted_strings) >= count:
                    break
        i += 1
    
    # Добавляем новые переводы в конец файла .po
    with open(output_file, 'a', encoding='utf-8') as f:
        for text, translation in extracted_strings:
            f.write(f'msgid "{text}"\nmsgstr "{translation}"\n\n')
    
    return len(extracted_strings)

def suggest_german_translation(text):
    """
    Простая функция для предложения немецкого перевода на основе часто используемых фраз.
    Для полноценного перевода нужно использовать API машинного перевода или словари.
    """
    # Словарь с некоторыми общими переводами
    translations = {
        # Основные приветствия и фразы
        "Welcome to": "Willkommen bei",
        "Hello": "Hallo",
        "Thank you": "Danke",
        "Please": "Bitte",
        "Yes": "Ja",
        "No": "Nein",
        
        # Бизнес термины
        "Services": "Dienstleistungen",
        "Contact": "Kontakt",
        "About": "Über",
        "Pricing": "Preise",
        "Blog": "Blog",
        "Login": "Anmelden",
        "Register": "Registrieren",
        "Password": "Passwort",
        "Email": "E-Mail",
        "Submit": "Absenden",
        "Send": "Senden",
        
        # Общие слова
        "and": "und",
        "or": "oder",
        "the": "die",
        "a": "ein",
        "an": "ein",
        "in": "in",
        "on": "auf",
        "for": "für",
        "with": "mit",
        "without": "ohne",
        "to": "zu",
        "from": "von",
        
        # Технические термины
        "AI": "KI",
        "Machine Learning": "Maschinelles Lernen",
        "Dashboard": "Dashboard",
        "Account": "Konto",
        "Profile": "Profil",
        "Settings": "Einstellungen",
        "Admin": "Administrator",
        "User": "Benutzer",
        
        # Специфические для сайта
        "Rozoom-KI": "Rozoom-KI",
        "All rights reserved": "Alle Rechte vorbehalten",
    }
    
    # Возвращаем пустую строку как заглушку, 
    # в реальности здесь должен быть машинный перевод
    return ""

if __name__ == "__main__":
    input_file = 'missing_translations.txt'
    output_file = 'app/translations/de/LC_MESSAGES/messages.po'
    
    # Создаем резервную копию файла перевода
    if os.path.exists(output_file):
        backup_file = output_file + '.bak'
        shutil.copy2(output_file, backup_file)
        print(f"Создана резервная копия файла перевода: {backup_file}")
    
    # Добавляем 50 наиболее важных строк для перевода
    count = extract_top_strings(input_file, output_file, 50)
    print(f"Добавлено {count} новых строк для перевода в {output_file}")
    print("Теперь вы можете вручную добавить переводы для этих строк.")
