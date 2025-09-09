from flask import Blueprint, g, request, current_app, session, redirect, jsonify, url_for

lang_bp = Blueprint('lang', __name__)

@lang_bp.route('/set-language/<lang>', methods=['GET'])
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
    
    # Проверяем, был ли запрос AJAX (если добавлен заголовок X-Requested-With)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Устанавливаем cookie для языка (срок действия 365 дней)
    max_age = 365 * 24 * 60 * 60  # 1 год в секундах
    
    if is_ajax:
        # Для AJAX запросов возвращаем JSON
        response = jsonify({'success': True, 'language': lang})
        response.set_cookie('lang', lang, max_age=max_age, path='/')
        return response
    else:
        # Для обычных запросов создаем ответ с редиректом
        response = make_response(redirect(next_url))
        response.set_cookie('lang', lang, max_age=max_age, path='/')
        return response
