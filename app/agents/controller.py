from typing import Optional, Dict
from . import get_agent, choose_agent_by_metadata
from flask import current_app
import requests


def route_and_respond(message: str, metadata: Dict) -> Dict:
    agent = choose_agent_by_metadata(metadata)
    if not agent:
        agent = get_agent('general')

    openai_key = current_app.config.get('OPENAI_API_KEY')
    model = current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini')
    if not openai_key:
        return {'error': 'OpenAI API key not configured'}

    # Greeter is a special agent: provide clickable domain options instead of calling OpenAI
    if agent.name == 'greeter':
        from . import list_domain_options
        return {'agent': 'greeter', 'options': list_domain_options(), 'message': agent.system_prompt}

    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': agent.system_prompt},
            {'role': 'user', 'content': message},
        ],
        'max_tokens': 500,
    }

    headers = {'Authorization': f'Bearer {openai_key}'}
    resp = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
    if resp.status_code != 200:
        # try fallback model if configured
        fallback = current_app.config.get('OPENAI_MODEL_FALLBACK')
        if fallback and fallback != model:
            payload['model'] = fallback
            resp = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
            if resp.status_code != 200:
                return {'error': 'OpenAI error', 'details': resp.text}
        else:
            return {'error': 'OpenAI error', 'details': resp.text}

    data = resp.json()
    try:
        answer = data['choices'][0]['message']['content']
    except Exception:
        answer = data

    return {'agent': agent.name, 'answer': answer}
