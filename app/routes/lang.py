from flask import Blueprint, request, current_app, jsonify, make_response, redirect

lang_bp = Blueprint('lang', __name__)


def _resolve_language(requested: str | None):
    if not requested:
        return None, None
    requested = requested.lower()
    aliases = current_app.config.get('LANGUAGE_ALIASES', {})
    normalized = aliases.get(requested, requested)
    languages = [lang.lower() for lang in current_app.config.get('LANGUAGES', ['en', 'de', 'uk'])]
    if normalized in languages:
        return normalized, requested
    return None, None


def _default_language():
    languages = [lang.lower() for lang in current_app.config.get('LANGUAGES', ['en', 'de', 'uk'])]
    default_locale = current_app.config.get('BABEL_DEFAULT_LOCALE', languages[0] if languages else 'en')
    normalized, _ = _resolve_language(default_locale)
    if normalized:
        return normalized
    return languages[0] if languages else 'en'


@lang_bp.route('/set-language/<lang>', methods=['GET'])
def set_language(lang):
    """Persist preferred language via cookie or JSON response."""
    normalized, cookie_value = _resolve_language(lang)
    if not normalized:
        normalized = _default_language()
        cookie_value = normalized

    next_url = request.args.get('next') or request.referrer or '/'
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    max_age = 365 * 24 * 60 * 60

    if is_ajax:
        response = jsonify({'success': True, 'language': normalized})
        response.set_cookie('lang', cookie_value, max_age=max_age, path='/')
        return response

    response = make_response(redirect(next_url))
    response.set_cookie('lang', cookie_value, max_age=max_age, path='/')
    return response
