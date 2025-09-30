from flask import request, g, current_app
from flask_babel import Babel
from .i18n_patch import domain_manager, payment_domain

babel = Babel()

def _configured_languages():
    languages = current_app.config.get('LANGUAGES', ['en', 'de', 'uk'])
    return [lang.lower() for lang in languages]

def _resolve_alias(value: str | None):
    if not value:
        return None
    value = value.lower()
    aliases = current_app.config.get('LANGUAGE_ALIASES', {})
    normalized = aliases.get(value, value)
    if normalized in _configured_languages():
        return normalized
    return None

def get_locale():
    """Determine the best matching locale for the current request."""
    languages = _configured_languages()

    # 1. Explicit ?lang= parameter
    from_query = _resolve_alias(request.args.get('lang'))
    if from_query:
        return from_query

    # 2. Cookie preference
    from_cookie = _resolve_alias(request.cookies.get('lang'))
    if from_cookie:
        return from_cookie

    # 3. Accept-Language header best match
    best_match = request.accept_languages.best_match(languages)
    normalized_best = _resolve_alias(best_match)
    if normalized_best:
        return normalized_best

    # 4. Fallback to configured default
    default_locale = current_app.config.get('BABEL_DEFAULT_LOCALE', languages[0] if languages else 'en')
    normalized_default = _resolve_alias(default_locale)
    if normalized_default:
        return normalized_default

    return languages[0] if languages else 'en'

def init_babel(app):
    """Initialise Flask-Babel with custom domains and locale handling."""
    babel.init_app(app, locale_selector=get_locale)
    domain_manager.init_domains(app)

    app.jinja_env.globals['payment_gettext'] = payment_domain.gettext
    app.jinja_env.globals['payment_ngettext'] = payment_domain.ngettext

    @app.before_request
    def before_request():
        g.locale = str(get_locale())
