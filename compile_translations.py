"""
Скрипт для компиляции файлов перевода (.po -> .mo)
"""
import os
import subprocess

def compile_translations():
    """Компиляция всех файлов перевода"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_dir, 'app', 'translations')
    
    if os.path.exists(translations_dir):
        for lang in os.listdir(translations_dir):
            lang_dir = os.path.join(translations_dir, lang)
            if os.path.isdir(lang_dir) and lang != '__pycache__':
                messages_dir = os.path.join(lang_dir, 'LC_MESSAGES')
                po_file = os.path.join(messages_dir, 'messages.po')
                mo_file = os.path.join(messages_dir, 'messages.mo')
                
                if os.path.exists(po_file):
                    print(f"Компиляция перевода для языка: {lang}")
                    try:
                        # Используем msgfmt для компиляции .po в .mo
                        # На Windows вам может потребоваться установить gettext
                        # https://mlocati.github.io/articles/gettext-iconv-windows.html
                        subprocess.run(['msgfmt', po_file, '-o', mo_file])
                        print(f"Перевод для {lang} успешно скомпилирован")
                    except Exception as e:
                        print(f"Ошибка компиляции перевода для {lang}: {e}")
                        # Если msgfmt не установлен, используем Python-реализацию
                        try:
                            from babel.messages.mofile import write_mo
                            from babel.messages.pofile import read_po
                            
                            with open(po_file, 'rb') as f:
                                catalog = read_po(f)
                            
                            with open(mo_file, 'wb') as f:
                                write_mo(f, catalog)
                                
                            print(f"Перевод для {lang} успешно скомпилирован с помощью Babel")
                        except Exception as babel_error:
                            print(f"Ошибка компиляции с помощью Babel: {babel_error}")
    else:
        print(f"Директория переводов не найдена: {translations_dir}")

if __name__ == "__main__":
    compile_translations()
