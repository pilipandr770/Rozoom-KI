"""
Скрипт для извлечения текста для перевода и создания/обновления файлов переводов
"""
import os
import subprocess
import click
from flask import current_app
from app import create_app

@click.group()
def translations():
    """Команды для управления переводами."""
    pass

@translations.command()
def extract():
    """Извлечь все строки для перевода из шаблонов и Python кода."""
    app = create_app()
    with app.app_context():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([
            'pybabel', 'extract', 
            '-F', 'babel.cfg', 
            '-k', '_', 
            '-o', 'app/translations/messages.pot', 
            '.'
        ])
        click.echo('Строки для перевода извлечены в messages.pot')

@translations.command()
@click.argument('lang')
def init(lang):
    """Инициализировать новый язык."""
    app = create_app()
    with app.app_context():
        if lang not in current_app.config['LANGUAGES']:
            click.echo(f'Язык {lang} не поддерживается. Поддерживаемые языки: {", ".join(current_app.config["LANGUAGES"])}')
            return
        
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        subprocess.run([
            'pybabel', 'init', 
            '-i', 'app/translations/messages.pot', 
            '-d', 'app/translations', 
            '-l', lang
        ])
        click.echo(f'Инициализирован язык {lang}')

@translations.command()
def update():
    """Обновить все файлы переводов на основе messages.pot."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([
        'pybabel', 'update', 
        '-i', 'app/translations/messages.pot', 
        '-d', 'app/translations'
    ])
    click.echo('Файлы переводов обновлены')

@translations.command()
def compile():
    """Скомпилировать все файлы переводов."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([
        'pybabel', 'compile', 
        '-d', 'app/translations'
    ])
    click.echo('Файлы переводов скомпилированы')

if __name__ == '__main__':
    translations()
