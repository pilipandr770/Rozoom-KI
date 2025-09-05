import markdown
from flask import Markup

def init_app(app):
    """
    Регистрирует фильтры для шаблонов Jinja2
    
    Args:
        app: Flask application
    """
    # Фильтр для преобразования Markdown в HTML
    @app.template_filter('markdown')
    def render_markdown(text):
        if not text:
            return ''
        return Markup(markdown.markdown(text))
