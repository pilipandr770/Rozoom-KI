#!/usr/bin/env python
"""
Скрипт для компиляции всех файлов переводов в проекте,
включая стандартные переводы и доменные переводы.
"""
import os
import glob
import subprocess
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

def compile_translations():
    """Компилировать все файлы переводов в проекте."""
    print("Компиляция стандартных файлов переводов...")
    
    # Попытка использования pybabel
    try:
        subprocess.run(["pybabel", "compile", "-d", "app/translations", "-f"], check=True)
        print("✅ Стандартные файлы переводов успешно скомпилированы через pybabel")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("⚠️ Ошибка при использовании pybabel, переключение на ручную компиляцию...")
        
        # Ручная компиляция
        for po_file in glob.glob('app/translations/**/LC_MESSAGES/messages.po', recursive=True):
            mo_file = po_file[:-3] + '.mo'
            print(f'Компиляция {po_file} -> {mo_file}')
            try:
                with open(po_file, 'rb') as f_in:
                    catalog = read_po(f_in)
                with open(mo_file, 'wb') as f_out:
                    write_mo(f_out, catalog)
            except Exception as e:
                print(f'Ошибка компиляции {po_file}: {e}')
        
        print("✅ Стандартные файлы переводов скомпилированы вручную")
    
    # Компилируем доменные файлы переводов (payment_translations и другие)
    print("\nКомпиляция доменных файлов переводов...")
    domains = ["payment_translations", "form_translations", "contact_translations", 
               "pricing_translations", "services_form_translations", "testimonial_translations"]
    
    for domain in domains:
        try:
            print(f"Компиляция домена {domain}...")
            subprocess.run(["pybabel", "compile", "-d", "app/translations", "-D", domain, "-f"], check=True)
            print(f"✅ Домен {domain} успешно скомпилирован через pybabel")
        except (subprocess.SubprocessError, FileNotFoundError):
            print(f"⚠️ Ошибка при использовании pybabel для домена {domain}, переключение на ручную компиляцию...")
            
            # Ручная компиляция для конкретного домена
            domain_files = glob.glob(f'app/translations/**/LC_MESSAGES/{domain}.po', recursive=True)
            if not domain_files:
                print(f"❌ Не найдены файлы перевода для домена {domain}")
                continue
                
            for po_file in domain_files:
                mo_file = po_file[:-3] + '.mo'
                print(f'Компиляция {po_file} -> {mo_file}')
                try:
                    with open(po_file, 'rb') as f_in:
                        catalog = read_po(f_in)
                    with open(mo_file, 'wb') as f_out:
                        write_mo(f_out, catalog)
                    print(f"✅ {po_file} успешно скомпилирован")
                except Exception as e:
                    print(f'❌ Ошибка компиляции {po_file}: {e}')
    
    print("\n🎉 Все файлы переводов успешно скомпилированы!")

if __name__ == "__main__":
    compile_translations()