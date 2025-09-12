# app/services/assistants_service.py
from __future__ import annotations
import os
import logging
import json
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime

from flask import current_app
from openai import OpenAI
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.assistant_thread import AssistantThread
from app.models.chat_message import ChatMessage

logger = logging.getLogger(__name__)

# Используем константу для выбора модели, чтобы легко переключать разные модели
DEFAULT_MODEL = "gpt-4o-2024-05-13"  # Более современная и мощная модель
# Запасная модель, если основная недоступна
FALLBACK_MODEL = "gpt-3.5-turbo"

def _client() -> OpenAI:
    api_key = current_app.config.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY не налаштований")
    return OpenAI(api_key=api_key)

def _get_cfg(name: str, default: Optional[str] = None) -> Optional[str]:
    return current_app.config.get(name) or os.getenv(name, default)

def get_or_create_thread(conversation_id: str, user_id: str, language: str) -> str:
    """
    Имитирует логику OpenAI Threads для обратной совместимости.
    Фактически только создаёт запись в БД, не создаёт реальный thread в OpenAI.
    """
    at = AssistantThread.query.filter_by(conversation_id=conversation_id).first()
    if at and at.openai_thread_id:
        return at.openai_thread_id

    # Генерируем уникальный ID для отслеживания беседы
    import uuid
    thread_id = f"thread_{uuid.uuid4().hex}"

    try:
        if not at:
            at = AssistantThread(
                conversation_id=conversation_id,
                user_id=user_id,
                language=language,
                openai_thread_id=thread_id
            )
            db.session.add(at)
        else:
            at.openai_thread_id = thread_id
            at.language = language or at.language
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("DB error while saving AssistantThread: %s", e)
        # Не валимо процес — просто повернемо thread_id
    return thread_id

def _get_assistant_prompt(kind: str) -> str:
    """
    Возвращает системный промпт для конкретного типа агента.
    """
    prompts = {
        "greeter": """
Ты - приветствующий AI-ассистент компании Rozoom. Твоя задача:
1. Понять потребности пользователя
2. Предоставить общую информацию об услугах компании
3. Определить, нужно ли перенаправить пользователя к более специализированному агенту

Компания Rozoom специализируется на:
- Разработке веб-сайтов и веб-приложений
- Дизайне интерфейсов (UI/UX)
- Создании технических спецификаций для проектов
- Цифровом маркетинге и SEO

Если пользователю нужна помощь с созданием ТЗ для проекта, предложи перейти к агенту 'spec'.
Если пользователь хочет узнать о статусе своего проекта, предложи перейти к агенту 'pm'.

Будь вежливым, профессиональным и информативным.
""",
        
        "spec": """
Ты - AI-специалист по созданию технических заданий компании Rozoom. Твоя задача:
1. Помочь пользователям структурировать требования для их проектов
2. Задавать уточняющие вопросы по функциональности
3. Предлагать технические решения на основе потребностей
4. Помогать оценить объем работ и примерные сроки

Придерживайся следующей структуры для технического задания:
- Цели и задачи проекта
- Целевая аудитория
- Функциональные требования
- Технический стек
- Этапы разработки
- Примерные сроки реализации

Спрашивай конкретные детали у пользователя, чтобы сделать ТЗ максимально полным.
""",
        
        "pm": """
Ты - AI-менеджер проектов компании Rozoom. Твоя задача:
1. Предоставлять информацию о статусе текущих проектов
2. Объяснять этапы разработки
3. Информировать о примерных сроках завершения задач

У тебя есть доступ к данным о проектах пользователя (если они предоставили идентификатор).
Если у пользователя есть активные проекты, ты можешь проверить их статус.
Если нет информации о проектах пользователя, предложи зарегистрировать проект или связаться с менеджером.

Будь точным в предоставлении информации и помогай пользователю понимать, на каком этапе находится их проект.
"""
    }
    
    return prompts.get(kind, prompts["greeter"])

def _get_message_history(thread_id: str, max_messages: int = 10) -> List[Dict[str, Any]]:
    """
    Получает историю сообщений для конкретного треда из базы данных.
    
    Args:
        thread_id: ID треда
        max_messages: Максимальное количество сообщений для контекста
        
    Returns:
        Список сообщений в формате для API Chat Completion.
    """
    try:
        # Находим запись треда чтобы получить conversation_id
        thread = AssistantThread.query.filter_by(openai_thread_id=thread_id).first()
        if not thread:
            logger.warning(f"Thread {thread_id} not found in database")
            return []
        
        # Получаем последние сообщения для этой беседы
        messages = ChatMessage.query.filter_by(
            thread_id=thread_id
        ).order_by(
            ChatMessage.created_at.asc()
        ).limit(max_messages).all()
        
        # Преобразуем в формат для API
        return [msg.as_dict for msg in messages]
    except Exception as e:
        logger.exception(f"Error retrieving message history: {e}")
        return []

def add_user_message(thread_id: str, text: str) -> None:
    """
    Добавляет сообщение пользователя в историю чата.
    
    Args:
        thread_id: ID треда
        text: Текст сообщения пользователя
    """
    try:
        # Находим запись треда чтобы получить conversation_id
        thread = AssistantThread.query.filter_by(openai_thread_id=thread_id).first()
        if not thread:
            logger.warning(f"Thread {thread_id} not found in database")
            return
        
        # Создаем новую запись сообщения
        message = ChatMessage(
            conversation_id=thread.conversation_id,
            thread_id=thread_id,
            role="user",
            content=text
        )
        
        db.session.add(message)
        db.session.commit()
    except Exception as e:
        logger.exception(f"Error adding user message: {e}")
        db.session.rollback()

def run_with_assistant(
    thread_id: str,
    assistant_kind: str,
    language: str,
    suppress_greeting: bool = False
) -> str:
    """
    Генерирует ответ с использованием Chat Completion API вместо Assistants API.
    
    Args:
        thread_id: Идентификатор треда (для совместимости)
        assistant_kind: Тип агента ("greeter", "spec", "pm")
        language: Язык ответа
        suppress_greeting: Флаг для подавления приветствия
        
    Returns:
        Текстовый ответ от модели
    """
    client = _client()
    
    # Получаем системный промпт для выбранного агента
    system_prompt = _get_assistant_prompt(assistant_kind)
    
    # Добавляем инструкцию по языку
    language_map = {
        "uk": "украинский",
        "ru": "русский",
        "en": "английский",
        "de": "немецкий"
    }
    language_name = language_map.get(language, "украинский")
    system_prompt += f"\nОтвечай на {language_name} языке."
    
    # Добавляем инструкцию по подавлению приветствия
    if suppress_greeting:
        system_prompt += "\nНе приветствуй пользователя снова, продолжи диалог без приветствий."
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Получаем историю сообщений из базы данных
    history = _get_message_history(thread_id)
    if history:
        messages.extend(history)
    
    # Если истории нет, добавляем контекстное сообщение
    if len(messages) <= 1:
        if assistant_kind == "spec":
            messages.append({
                "role": "user", 
                "content": "Хочу создать техническое задание для моего проекта"
            })
        elif assistant_kind == "pm":
            messages.append({
                "role": "user", 
                "content": "Хочу узнать о статусе моего проекта"
            })
        else:  # greeter
            messages.append({
                "role": "user",
                "content": "Привет! Расскажи, что вы делаете?"
            })
    
    # Выполняем запрос к API
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            assistant_message = response.choices[0].message.content
            
            # Сохраняем ответ ассистента в историю
            try:
                thread = AssistantThread.query.filter_by(openai_thread_id=thread_id).first()
                if thread:
                    # Создаем новую запись сообщения
                    message = ChatMessage(
                        conversation_id=thread.conversation_id,
                        thread_id=thread_id,
                        role="assistant",
                        content=assistant_message
                    )
                    db.session.add(message)
                    db.session.commit()
            except Exception as e:
                logger.exception(f"Error saving assistant message: {e}")
                db.session.rollback()
                
            return assistant_message
        else:
            return "(порожня відповідь від API)"
    except Exception as e:
        logger.exception(f"Error with OpenAI API: {e}")
        
        # Пробуем использовать запасную модель
        try:
            logger.info(f"Trying fallback model {FALLBACK_MODEL}")
            response = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "(порожня відповідь від запасної API)"
        except Exception as fallback_e:
            logger.exception(f"Error with fallback API: {fallback_e}")
            return f"(помилка API: {str(e)})"
