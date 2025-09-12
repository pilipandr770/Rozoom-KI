from flask import Blueprint, request, jsonify, current_app, session
import os
import requests
from .. import db, csrf
from ..agents.controller import route_and_respond
# Keep emergency fallback available but do not use it by default
try:
    from ..agents.chat_fix import simple_chat_response  # noqa: F401
except Exception:
    simple_chat_response = None  # type: ignore

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})


@api_bp.route('/chat', methods=['POST'])
@csrf.exempt  # Освобождаем этот маршрут от CSRF проверки
def chat():
    # Parse request
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        metadata = data.get('metadata', {})

        current_app.logger.info(f"Chat API received: message={message[:50]}..., metadata={metadata}")

        # Ensure conversation_id
        if not metadata.get('conversation_id'):
            import uuid
            metadata['conversation_id'] = str(uuid.uuid4())

        # Resolve language
        user_lang = metadata.get('language')
        if not user_lang:
            accept_language = request.headers.get('Accept-Language', 'uk')
            if 'uk' in accept_language or 'ua' in accept_language:
                user_lang = 'uk'
            elif 'ru' in accept_language:
                user_lang = 'ru'
            elif 'de' in accept_language:
                user_lang = 'de'
            elif 'en' in accept_language:
                user_lang = 'en'
            else:
                user_lang = 'uk'
        metadata['language'] = user_lang
        current_app.logger.info(f"Chat request: lang={user_lang}, message={message[:50]}...")
    except Exception as e:
        current_app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e), 'answer': 'Помилка при обробці запиту.'}), 400

    # Clear any failed transactions
    try:
        db.session.rollback()
    except Exception as e:
        current_app.logger.warning(f"Rollback before processing failed: {e}")

    # Main flow: use controller route_and_respond (Assistants/legacy pipeline)
    try:
        result = route_and_respond(message, metadata)
    except Exception as e:
        current_app.logger.exception(f"route_and_respond failed: {e}")
        # Fallback to emergency simple handler if available
        if simple_chat_response:
            try:
                fallback = simple_chat_response(message, metadata)
                return jsonify({
                    'agent': fallback.get('agent', 'fallback'),
                    'answer': fallback.get('answer', '...'),
                    'conversation_id': fallback.get('conversation_id', metadata.get('conversation_id'))
                }), 200
            except Exception as fe:
                current_app.logger.error(f"Fallback simple_chat_response failed: {fe}")
        return jsonify({'error': 'Chat processing failed', 'answer': 'Вибачте, сталася помилка при обробці повідомлення.'}), 200

    # Compose response
    agent = result.get('agent')
    answer = result.get('answer')
    response = {
        'agent': agent,
        'answer': answer,
        'conversation_id': result.get('conversation_id', metadata.get('conversation_id'))
    }
    if result.get('interactive'):
        response['interactive'] = result['interactive']

    current_app.logger.info(f"Sending chat response: agent={agent}, answer={str(answer)[:50]}...")
    return jsonify(response)
