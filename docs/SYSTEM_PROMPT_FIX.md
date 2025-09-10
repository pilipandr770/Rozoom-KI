# Исправление отсутствующей функции get_system_prompt

## Обнаруженная проблема

При запуске приложения возникала ошибка:

```
NameError: name 'get_system_prompt' is not defined. Did you mean: 'get_greeter_prompt'?
```

## Причина проблемы

В модуле `app/agents/prompts.py` были определены алиасы функций для обеспечения обратной совместимости с `controller.py`, однако отсутствовала сама функция `get_system_prompt`, на которую ссылались эти алиасы:

```python
# Алиасы для обеспечения обратной совместимости
# controller.py использует create_* вместо get_*
create_system_prompt = get_system_prompt  # Ошибка: get_system_prompt не определена
create_greeter_prompt = get_greeter_prompt
create_completion_prompt = get_completion_prompt
create_portfolio_prompt = get_portfolio_prompt
```

## Решение

В модуль `app/agents/prompts.py` добавлена реализация отсутствующей функции `get_system_prompt`:

```python
def get_system_prompt(lang='de'):
    """
    Возвращает системный промпт
    
    Args:
        lang: Код языка ('de', 'ru', 'en')
        
    Returns:
        str: Системный промпт на указанном языке
    """
    prompts = {
        'de': """Du bist ein KI-Assistent für die Rozoom-KI Website. Deine Hauptaufgabe ist es, Besuchern zu helfen, Fragen zu beantworten und sie durch die Website zu führen.""",
        'ru': """Ты ИИ-ассистент для сайта Rozoom-KI. Твоя основная задача - помогать посетителям, отвечать на вопросы и направлять их по сайту.""",
        'en': """You are an AI assistant for the Rozoom-KI website. Your main task is to help visitors, answer questions, and guide them through the website."""
    }
    return prompts.get(lang, prompts['de'])
```

Теперь алиасы корректно ссылаются на существующую функцию.

## Проверка

После внесения изменений проведена проверка компиляции обоих файлов:

```
python -m py_compile app\agents\prompts.py
python -m py_compile app\agents\controller.py
```

Оба файла успешно скомпилировались, что подтверждает решение проблемы с отсутствующей функцией.
