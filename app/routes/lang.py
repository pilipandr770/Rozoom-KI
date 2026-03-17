from urllib.parse import urlparse, urlunparse, urlencode, parse_qs, urljoin
from flask import Blueprint, request, current_app, jsonify, make_response, redirect, session

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

    # Restrict redirect to local paths only (prevent open-redirect).
    raw_next = request.args.get('next') or ''
    parsed = urlparse(raw_next)
    if not parsed.netloc and raw_next.startswith('/'):
        # Append ?lang=<normalized> so get_locale() reads it at step 1
        # even if the browser blocks the cookie.
        qs = parse_qs(parsed.query)
        qs['lang'] = [normalized]
        next_url = urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))
    else:
        next_url = f'/?lang={normalized}'
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    max_age = 365 * 24 * 60 * 60

    if is_ajax:
        response = jsonify({'success': True, 'language': normalized})
        response.set_cookie('lang', cookie_value, max_age=max_age, path='/')
        return response

    # Store in Flask session as a reliable cross-request backup
    session['lang'] = normalized
    session.permanent = True

    response = make_response(redirect(next_url))
    response.set_cookie(
        'lang', cookie_value,
        max_age=max_age,
        path='/',
        samesite='Lax',
    )
    # No-store so the redirect itself is never served from browser cache
    response.headers['Cache-Control'] = 'no-store'
    return response
