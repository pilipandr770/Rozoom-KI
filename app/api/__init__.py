from flask import Blueprint, request, jsonify, current_app
import os
import requests
from ..models import ChatMessage
from .. import db
from ..agents.controller import route_and_respond

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})


@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    metadata = data.get('metadata', {})

    # Delegate routing + OpenAI call to agents.controller
    result = route_and_respond(message, metadata)
    if 'error' in result:
        return jsonify(result), 502

    agent = result.get('agent')
    answer = result.get('answer')

    # persist chat to DB (rozoom_ki_clients schema)
    try:
        user_msg = ChatMessage(role='user', content=message, meta=metadata)
        bot_msg = ChatMessage(role='assistant', content=answer, meta={'agent': agent})
        db.session.add(user_msg)
        db.session.add(bot_msg)
        db.session.commit()
    except Exception as e:
        current_app.logger.error('Failed to persist chat: %s', e)

    return jsonify({'agent': agent, 'answer': answer})
