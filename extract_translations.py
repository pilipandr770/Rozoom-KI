import os
import re
import glob

def extract_text_from_html_files(directory):
    """
    Извлекает текстовые строки из HTML-файлов для потенциального перевода.
    Ищет только строки внутри тегов, игнорируя уже переведенные строки (с _()).
    """
    translations = set()
    pattern = re.compile(r'>([^<>{}/\n\r\t]+?)<')  # Находит текст между тегами
    translated_pattern = re.compile(r'\{\{\s*_\([\'"](.+?)[\'"]\)\s*\}\}')  # Уже переведенные строки
    
    # Получаем список всех HTML-файлов в директории
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    # Извлекаем текстовые строки из каждого файла
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Игнорируем уже переведенные строки
            translated = set(translated_pattern.findall(content))
            
            # Находим все текстовые строки между тегами
            matches = pattern.findall(content)
            for match in matches:
                # Очищаем и проверяем, что строка содержит полезный текст
                text = match.strip()
                if (text and len(text) > 1 and 
                    not text.startswith('{{') and 
                    not text.startswith('{%') and
                    not text.startswith('#') and
                    not text in translated):
                    translations.add(text)
    
    return sorted(translations)

def write_translations_to_file(translations, output_file):
    """Записывает строки для перевода в формате .po файла"""
    with open(output_file, 'w', encoding='utf-8') as file:
        for text in translations:
            file.write(f'msgid "{text}"\nmsgstr ""\n\n')

# Основной код
if __name__ == "__main__":
    templates_dir = 'app/templates'
    output_file = 'missing_translations.txt'
    
    print(f"Поиск текстов для перевода в {templates_dir}...")
    translations = extract_text_from_html_files(templates_dir)
    
    print(f"Найдено {len(translations)} потенциальных строк для перевода.")
    write_translations_to_file(translations, output_file)
    print(f"Результаты сохранены в {output_file}")
