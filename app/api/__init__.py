from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user
import os
import requests
from .. import db, csrf
from ..agents.controller import route_and_respond
from ..babel import get_locale
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
@csrf.exempt  # РћСЃРІРѕР±РѕР¶РґР°РµРј СЌС‚РѕС‚ РјР°СЂС€СЂСѓС‚ РѕС‚ CSRF РїСЂРѕРІРµСЂРєРё
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
        languages = [lang.lower() for lang in current_app.config.get('LANGUAGES', ['en', 'de', 'uk'])]
        aliases = current_app.config.get('LANGUAGE_ALIASES', {})

        requested_lang = metadata.get('language')
        if requested_lang:
            requested_lang = requested_lang.lower()
            user_lang = aliases.get(requested_lang, requested_lang)
        else:
            user_lang = None

        if user_lang not in languages:
            user_lang = get_locale()

        metadata['language'] = user_lang
        current_app.logger.info(f"Chat request: lang={user_lang}, message={message[:50]}...")
    except Exception as e:
        current_app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e), 'answer': 'РџРѕРјРёР»РєР° РїСЂРё РѕР±СЂРѕР±С†С– Р·Р°РїРёС‚Сѓ.'}), 400

    # Clear any failed transactions
    try:
        db.session.rollback()
    except Exception as e:
        current_app.logger.warning(f"Rollback before processing failed: {e}")

    # If user is authenticated, bind metadata.user_id to the logged-in user's id
    try:
        if getattr(current_user, 'is_authenticated', False) and hasattr(current_user, 'id'):
            metadata['user_id'] = current_user.id
            # Optional: include user email for downstream context
            if hasattr(current_user, 'email'):
                metadata.setdefault('user_email', current_user.email)
    except Exception as e:
        current_app.logger.warning(f"Unable to bind session user to chat metadata: {e}")

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
        return jsonify({'error': 'Chat processing failed', 'answer': 'Р’РёР±Р°С‡С‚Рµ, СЃС‚Р°Р»Р°СЃСЏ РїРѕРјРёР»РєР° РїСЂРё РѕР±СЂРѕР±С†С– РїРѕРІС–РґРѕРјР»РµРЅРЅСЏ.'}), 200

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




