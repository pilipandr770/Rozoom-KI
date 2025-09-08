import re
import unicodedata
from typing import Optional

def generate_slug(text: str) -> str:
    """
    Генерирует SEO-дружественный URL-слаг из текста
    
    Args:
        text (str): Исходный текст
        
    Returns:
        str: URL-слаг
    """
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Удаляем диакритические знаки (ä -> a, ü -> u, etc.)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    
    # Заменяем все символы, кроме букв, цифр и пробелов, на пробелы
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # Заменяем последовательности пробелов на один дефис
    text = re.sub(r'\s+', '-', text)
    
    # Удаляем лишние дефисы в начале и конце
    text = text.strip('-')
    
    return text

def strip_html(text: Optional[str]) -> str:
    """
    Удаляет HTML-теги из текста
    
    Args:
        text (Optional[str]): Исходный текст
        
    Returns:
        str: Текст без HTML-тегов
    """
    if not text:
        return ""
    
    # Удаляем HTML-теги
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def clean_icons_from_content(content: Optional[str]) -> str:
    """
    Очищает контент от Font Awesome иконок и других нежелательных элементов
    
    Args:
        content (Optional[str]): Исходный HTML-контент
        
    Returns:
        str: Очищенный HTML-контент
    """
    if not content:
        return ""
    
    # Удаляем теги <i> с классами Font Awesome
    content = re.sub(r'<i[^>]*class=[\'"][^\'"]*(?:fa|fas|far|fab)[^\'"]*[\'"][^>]*><\/i>\s*', '', content)
    
    # Удаляем символы # в начале строк (заменяя их на двойные ##, чтобы сохранить заголовки Markdown)
    content = re.sub(r'(\n|^)#\s+', r'\1## ', content)
    
    # Удаляем символы @ перед именами пользователей
    content = re.sub(r'@User\d+', '', content)
    
    return content
