"""
Патч для инициализации дополнительных доменов Flask-Babel.

В некоторых версиях Flask-Babel домены не имеют метода init_app,
поэтому мы создаём собственный класс для инициализации доменов.
"""
from flask import Flask, g, request
from flask_babel import Domain
import os

class DomainManager:
    """Класс для управления доменами переводов Flask-Babel"""
    
    def __init__(self):
        """Инициализировать менеджер доменов"""
        self.domains = {}
    
    def register_domain(self, domain_name):
        """Зарегистрировать новый домен переводов"""
        domain = Domain(domain=domain_name)
        self.domains[domain_name] = domain
        return domain
    
    def get_domain(self, domain_name):
        """Получить домен по имени"""
        if domain_name not in self.domains:
            self.register_domain(domain_name)
        return self.domains[domain_name]
    
    def init_domains(self, app):
        """Инициализировать все домены в приложении"""
        # Добавляем пути доменов в настройки Flask-Babel
        babel_translation_directories = app.config.get('BABEL_TRANSLATION_DIRECTORIES', 'translations')
        
        # Убедиться, что путь к переводам существует в приложении
        translations_path = os.path.join(app.root_path, 'translations')
        app.logger.debug(f"Translations path: {translations_path}")
        
        # Загрузить функции перевода в глобальное пространство имён шаблонов
        for domain_name, domain in self.domains.items():
            app.logger.debug(f"Loading domain: {domain_name}")
            # Делаем функцию gettext доступной в шаблонах
            app.jinja_env.globals[f'gettext_{domain_name}'] = domain.gettext
            app.jinja_env.globals[f'ngettext_{domain_name}'] = domain.ngettext

# Создаем экземпляр менеджера доменов
domain_manager = DomainManager()

# Предварительно регистрируем домен для платежей
payment_domain = domain_manager.register_domain('payment_translations')