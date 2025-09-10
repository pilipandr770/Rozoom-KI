# Исправление ошибки отсутствующего модуля schemas

## Обнаруженная проблема

После исправления синтаксических ошибок в `controller.py` была обнаружена новая ошибка в логах деплоя:

```
ModuleNotFoundError: No module named 'app.agents.schemas'
```

Файл `controller.py` содержал импорт:
```python
from app.agents.schemas import AgentMessage, QuizChoice
```

Но файл `schemas.py` не существовал в директории `app/agents/`.

## Созданное решение

Был создан файл `app/agents/schemas.py` с определением двух классов:

```python
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass


@dataclass
class AgentMessage:
    """Schema for agent messages"""
    text: str
    agent: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class QuizChoice:
    """Schema for quiz choices"""
    text: str
    value: str
    cost: float
    description: Optional[str] = None
```

## Реализация

Файл `schemas.py` был создан с минимальной функциональностью, необходимой для компиляции `controller.py`. Классы определены как датаклассы Python с необходимыми полями.

## Особенности реализации

1. Классы были реализованы как датаклассы, что позволяет легко сериализовать и десериализовать данные
2. Добавлены типизированные аннотации для лучшего анализа кода
3. Добавлены опциональные поля для гибкости использования
4. Добавлены документационные строки для улучшения читаемости кода

## Результат

После создания файла `schemas.py` компиляция `controller.py` проходит успешно, что должно устранить ошибку при развертывании на сервере Render.com.
