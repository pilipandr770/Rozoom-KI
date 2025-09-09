"""
Скрипт для быстрой компиляции файлов перевода (.po -> .mo)
Для использования на сервере при деплое
"""
import os
import sys
import logging
from pathlib import Path
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def compile_mo_files():
    """
    Компилирует все .po файлы в .mo файлы
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_dir, 'app', 'translations')
    
    if not os.path.exists(translations_dir):
        logger.error(f"Директория переводов не существует: {translations_dir}")
        return False
    
    success_count = 0
    error_count = 0
    
    for lang in os.listdir(translations_dir):
        lang_dir = os.path.join(translations_dir, lang)
        
        if not os.path.isdir(lang_dir) or lang == '__pycache__':
            continue
            
        lc_messages_dir = os.path.join(lang_dir, 'LC_MESSAGES')
        
        if not os.path.isdir(lc_messages_dir):
            logger.warning(f"Директория LC_MESSAGES отсутствует для языка {lang}")
            continue
            
        for po_file in Path(lc_messages_dir).glob('*.po'):
            mo_file = po_file.with_suffix('.mo')
            try:
                with open(po_file, 'rb') as f:
                    catalog = read_po(f)
                    
                with open(mo_file, 'wb') as f:
                    write_mo(f, catalog)
                    
                logger.info(f"Успешно скомпилирован: {po_file} -> {mo_file}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"Ошибка при компиляции {po_file}: {e}")
                error_count += 1
    
    logger.info(f"Компиляция завершена: {success_count} успешно, {error_count} с ошибками")
    return success_count > 0 and error_count == 0

if __name__ == "__main__":
    success = compile_mo_files()
    sys.exit(0 if success else 1)
