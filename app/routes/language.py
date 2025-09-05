from flask import Blueprint, request, redirect, make_response, url_for

language_bp = Blueprint('language', __name__, url_prefix='/language')

@language_bp.route('/set/<lang>')
def set_language(lang):
    """
    Устанавливает язык интерфейса и сохраняет его в cookie
    
    Args:
        lang: Код языка ('en' или 'de')
        
    Returns:
        Редирект на предыдущую страницу с установленным cookie
    """
    # Проверяем, что язык поддерживается
    if lang not in ['en', 'de']:
        lang = 'de'  # По умолчанию немецкий
    
    # Получаем URL страницы, с которой пришел запрос
    next_url = request.args.get('next') or request.referrer or '/'
    
    # Создаем ответ с редиректом
    response = make_response(redirect(next_url))
    
    # Устанавливаем cookie для языка (срок действия 365 дней)
    max_age = 365 * 24 * 60 * 60  # 1 год в секундах
    response.set_cookie('lang', lang, max_age=max_age, path='/')
    
    return response
