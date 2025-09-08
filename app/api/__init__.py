from flask import Blueprint, request, jsonify, current_app, session
import os
import requests
from ..models import ChatMessage
from .. import db, csrf
from ..agents.controller import route_and_respond

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})


@api_bp.route('/chat', methods=['POST'])
@csrf.exempt  # Освобождаем этот маршрут от CSRF проверки
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    metadata = data.get('metadata', {})
    
    # Assign a conversation ID if not present
    if not metadata.get('conversation_id'):
        import uuid
        metadata['conversation_id'] = str(uuid.uuid4())
    
    # Определение языка пользователя
    user_lang = metadata.get('language')
    if not user_lang:
        # Проверяем заголовок Accept-Language
        accept_language = request.headers.get('Accept-Language', 'de')
        if 'de' in accept_language:
            user_lang = 'de'
        elif 'ru' in accept_language:
            user_lang = 'ru'
        elif 'en' in accept_language:
            user_lang = 'en'
        else:
            # По умолчанию используем немецкий
            user_lang = 'de'
        
        metadata['language'] = user_lang
    
    # Store previous messages in metadata if available
    if not metadata.get('history'):
        # Try to fetch previous messages from DB
        try:
            conversation_id = metadata.get('conversation_id')
            if conversation_id:
                # Проверим, поддерживается ли conversation_id моделью
                if hasattr(ChatMessage, 'conversation_id'):
                    try:
                        # Используем conversation_id для фильтрации
                        prev_messages = ChatMessage.query.filter_by(
                            conversation_id=conversation_id
                        ).order_by(ChatMessage.timestamp).all()
                        
                        if prev_messages:
                            metadata['history'] = [
                                {'role': msg.role, 'content': msg.content}
                                for msg in prev_messages
                            ]
                    except Exception as e:
                        current_app.logger.warning(f"Error fetching messages with conversation_id: {e}")
                else:
                    # Если поле conversation_id не поддерживается, просто берем последние сообщения
                    current_app.logger.warning("conversation_id field not available in ChatMessage model")
                    
                    # Безопасное чтение последних сообщений для поддержания контекста
                    try:
                        # Используем временную метку для сортировки, получаем последние 10 сообщений
                        prev_messages = ChatMessage.query.order_by(
                            ChatMessage.created_at.desc()
                        ).limit(10).all()
                        
                        if prev_messages:
                            # Реверсируем, чтобы получить правильный порядок
                            metadata['history'] = [
                                {'role': msg.role, 'content': msg.content}
                                for msg in reversed(prev_messages)
                            ]
                    except Exception as e:
                        current_app.logger.warning(f"Error fetching recent messages: {e}")
        except Exception as e:
            current_app.logger.warning(f"Could not fetch message history: {e}")

    # Логируем метаданные для отладки
    current_app.logger.info(f"Metadata before calling API: {metadata}")

    # Delegate routing + OpenAI call to agents.controller
    result = route_and_respond(message, metadata)
    if 'error' in result:
        return jsonify(result), 502

    agent = result.get('agent')
    answer = result.get('answer')
    interactive = result.get('interactive', {})
    
    # Записываем conversation_id для отладки
    current_app.logger.info(f"conversation_id для сохранения в БД: {metadata.get('conversation_id')}")

    # persist chat to DB (rozoom_ki_clients schema)
    try:
        # Проверим сначала, есть ли сессия транзакции в ошибочном состоянии, и закроем её
        if db.session.is_active and hasattr(db.session, 'is_modified') and db.session.is_modified():
            try:
                db.session.rollback()
            except:
                current_app.logger.warning("Failed to rollback session")
        
        # Only add user message if there is one (not for initial greeter)
        if message:
            try:
                user_msg = ChatMessage(
                    role='user',
                    content=message,
                    meta=metadata
                )
                
                # Получаем или создаем conversation_id
                conversation_id = metadata.get('conversation_id')
                current_app.logger.info(f"Got conversation_id from request: {conversation_id}")
                
                # Пробуем добавить conversation_id только если он поддерживается моделью
                if hasattr(ChatMessage, 'conversation_id'):
                    user_msg.conversation_id = conversation_id
                    current_app.logger.info(f"Setting conversation_id: {conversation_id} for user message")
                
                db.session.add(user_msg)
                
                # Сразу делаем flush, чтобы проверить правильность сохранения
                db.session.flush()
                current_app.logger.info(f"User message created with ID {user_msg.id} and conversation_id {user_msg.conversation_id}")
                
            except Exception as e:
                current_app.logger.warning(f"Could not create user message: {e}")
                # Делаем rollback, чтобы не блокировать следующие операции
                db.session.rollback()
        
        # Always add bot response
        try:
            bot_meta = {'agent': agent}
            if interactive:
                bot_meta['interactive'] = interactive
                
            bot_msg = ChatMessage(
                role='assistant',
                content=answer,
                meta=bot_meta
            )
            
            # Получаем conversation_id из метаданных или создаем новый, если отсутствует
            conversation_id = metadata.get('conversation_id')
            current_app.logger.info(f"Using conversation_id: {conversation_id}")
            
            # Пробуем добавить conversation_id только если он поддерживается моделью
            if hasattr(ChatMessage, 'conversation_id'):
                bot_msg.conversation_id = conversation_id
            
            db.session.add(bot_msg)
            
            # Commit только если оба добавления прошли успешно
            db.session.commit()
            
            # Логируем успешное сохранение
            current_app.logger.info(f"Successfully saved message with conversation_id: {conversation_id}")
        except Exception as e:
            current_app.logger.error(f'Failed to persist bot message: {e}')
            db.session.rollback()
    except Exception as e:
        current_app.logger.error('Failed to persist chat: %s', e)
        # Всегда делаем rollback, чтобы не оставлять сессию в ошибочном состоянии
        try:
            db.session.rollback()
        except:
            pass

    # Return the full result including interactive elements
    response = {
        'agent': agent,
        'answer': answer,
        'conversation_id': metadata.get('conversation_id')
    }
    
    # Include interactive elements if present
    if interactive:
        response['interactive'] = interactive
    
    return jsonify(response)
