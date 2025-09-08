"""
Скрипт для проверки статуса переводов в приложении
"""

import os
import sys
from pathlib import Path

def check_translations():
    """Проверяет доступные переводы и их статус"""
    base_dir = Path(__file__).parent.absolute()
    translations_dir = base_dir / 'app' / 'translations'
    
    if not translations_dir.exists():
        print(f"Директория переводов не найдена: {translations_dir}")
        return
    
    print("=== Статус переводов ===")
    print(f"Директория переводов: {translations_dir}")
    
    # Проверка доступных языков
    languages = [d for d in translations_dir.iterdir() if d.is_dir() and d.name != '__pycache__']
    print(f"Доступные языки: {[lang.name for lang in languages]}")
    
    # Детальная информация по каждому языку
    for lang_dir in languages:
        print(f"\nЯзык: {lang_dir.name}")
        
        # Проверка файлов LC_MESSAGES
        messages_dir = lang_dir / 'LC_MESSAGES'
        if not messages_dir.exists():
            print(f"  Директория LC_MESSAGES не найдена для {lang_dir.name}")
            continue
            
        # Проверка .po файлов
        po_files = list(messages_dir.glob('*.po'))
        print(f"  .po файлы: {[po.name for po in po_files]}")
        
        # Проверка .mo файлов
        mo_files = list(messages_dir.glob('*.mo'))
        print(f"  .mo файлы: {[mo.name for mo in mo_files]}")
        
        # Проверка основного файла перевода
        main_po = messages_dir / 'messages.po'
        main_mo = messages_dir / 'messages.mo'
        
        if main_po.exists():
            # Подсчет строк для перевода
            with open(main_po, 'r', encoding='utf-8') as f:
                content = f.read()
                msgid_count = content.count('\nmsgid "')
                msgstr_count = content.count('\nmsgstr "')
                
                print(f"  Файл messages.po:")
                print(f"    - Строк для перевода (msgid): {msgid_count}")
                print(f"    - Строк с переводами (msgstr): {msgstr_count}")
                
                # Проверка на наличие устаревших переводов
                obsolete_count = content.count('\n#~ msgid')
                if obsolete_count > 0:
                    print(f"    - Устаревших строк (#~ msgid): {obsolete_count} - ВНИМАНИЕ! Эти строки не используются!")
        
        if main_mo.exists():
            print(f"  Файл messages.mo: ПРИСУТСТВУЕТ")
            # Определим дату последней модификации .mo файла по сравнению с .po файлом
            if main_po.exists():
                po_mtime = os.path.getmtime(main_po)
                mo_mtime = os.path.getmtime(main_mo)
                if mo_mtime < po_mtime:
                    print(f"    - ВНИМАНИЕ! Файл .mo устарел (старше чем .po файл) - требуется компиляция")
        else:
            print(f"  Файл messages.mo: ОТСУТСТВУЕТ - требуется компиляция")

    print("\n=== Рекомендации ===")
    print("1. Убедитесь, что все строки перевода имеют соответствующие msgstr значения")
    print("2. Убедитесь, что все .po файлы скомпилированы в .mo файлы")
    print("3. Проверьте отсутствие устаревших строк (с #~ префиксом) в .po файлах")
    print("4. Проверьте config.py на наличие правильных настроек BABEL_DEFAULT_LOCALE и LANGUAGES")
    print("5. Проверьте, что все строки в шаблонах обернуты в функцию {{ _('строка') }}")

if __name__ == "__main__":
    check_translations()
