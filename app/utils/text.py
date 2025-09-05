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
