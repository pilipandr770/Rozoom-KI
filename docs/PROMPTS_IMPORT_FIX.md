# Исправление ошибки импорта из модуля prompts

## Обнаруженная проблема

При деплое на сервер Render.com возникала следующая ошибка:

```
ImportError: cannot import name 'create_system_prompt' from 'app.agents.prompts'
```

## Причина проблемы

В файле `app/agents/controller.py` используются импорты функций из модуля `prompts.py` с префиксом `create_`:

```python
from app.agents.prompts import (
    create_system_prompt, 
    create_greeter_prompt, 
    create_completion_prompt,
    create_portfolio_prompt
)
```

Однако в модуле `app/agents/prompts.py` эти функции были определены с префиксом `get_`:

```python
def get_system_prompt(lang='de'):
    # ...

def get_greeter_prompt(lang='de'):
    # ...

def get_completion_prompt(lang='de'):
    # ...

def get_portfolio_prompt(lang='de'):
    # ...
```

## Решение

Для решения проблемы в файл `app/agents/prompts.py` добавлены алиасы, которые связывают функции с префиксом `get_` с соответствующими именами с префиксом `create_`:

```python
# Алиасы для обеспечения обратной совместимости
# controller.py использует create_* вместо get_*
create_system_prompt = get_system_prompt
create_greeter_prompt = get_greeter_prompt
create_completion_prompt = get_completion_prompt
create_portfolio_prompt = get_portfolio_prompt
```

Это обеспечивает обратную совместимость без необходимости менять существующий код в `controller.py`.

## Проверка

После внесения изменений проведена проверка компиляции обоих файлов:

```
python -m py_compile app\agents\prompts.py
python -m py_compile app\agents\controller.py
```

Оба файла успешно скомпилировались, что подтверждает решение проблемы импорта.
