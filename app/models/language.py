"""
Модуль для работы с переводами и определения языка
"""
from flask import request, session
import re


def detect_language(text, default_lang='de'):
    """
    Определяет язык текста по паттернам символов
    
    Args:
        text: Строка для анализа
        default_lang: Язык по умолчанию, если не удалось определить
        
    Returns:
        str: Код языка ('de', 'ru', 'en')
    """
    if not text:
        # Если текст пустой, используем настройки сессии или язык по умолчанию
        return session.get('lang', default_lang)
    
    # Определение языка по характерным паттернам
    # Кириллические символы для русского
    if re.search('[а-яА-Я]', text):
        return 'ru'
    
    # Специфические немецкие символы
    if re.search('[äöüÄÖÜß]', text):
        return 'de'
    
    # Для английского проверяем, если больше латинских символов, чем специфических немецких
    latin_chars = len(re.findall('[a-zA-Z]', text))
    german_chars = len(re.findall('[äöüÄÖÜß]', text))
    
    if latin_chars > 0 and latin_chars > german_chars:
        return 'en'
    
    # По умолчанию используем язык сессии или немецкий
    return session.get('lang', default_lang)


def get_text_by_key(translations, key, lang='de'):
    """
    Получает перевод по ключу и языку
    
    Args:
        translations: Словарь с переводами
        key: Ключ для поиска
        lang: Код языка ('de', 'ru', 'en')
        
    Returns:
        str: Текст перевода или ключ, если перевод не найден
    """
    if key in translations:
        # Если для ключа есть словарь с переводами
        if isinstance(translations[key], dict):
            # Если есть перевод для запрошенного языка, возвращаем его
            if lang in translations[key]:
                return translations[key][lang]
            # Иначе возвращаем немецкий перевод как запасной вариант
            elif 'de' in translations[key]:
                return translations[key]['de']
    
    # Если ключ не найден или нет подходящего перевода, возвращаем сам ключ
    return key
