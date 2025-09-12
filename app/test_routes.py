"""
Test routes for the chat functionality
"""
from flask import Blueprint, render_template, current_app, redirect, url_for
from .agents.chat_fix import simple_chat_response

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/chat')
def chat_test():
    """
    Simple chat test page
    """
    return render_template('chat_test.html')

@test_bp.route('/simple_chat_test/<language>/<message>')
def test_simple_chat(language, message):
    """
    Test the simple_chat_response function directly
    """
    import uuid
    conversation_id = str(uuid.uuid4())
    
    metadata = {
        'language': language,
        'conversation_id': conversation_id,
        'page': '/test/chat'
    }
    
    try:
        result = simple_chat_response(message, metadata)
        answer_html = result.get('answer', '').replace('\n', '<br>')
        return f'''
        <h1>Chat Test</h1>
        <p><strong>Message:</strong> {message}</p>
        <p><strong>Language:</strong> {language}</p>
        <p><strong>Conversation ID:</strong> {conversation_id}</p>
        <hr>
        <h2>Response:</h2>
        <p><strong>Agent:</strong> {result.get('agent')}</p>
        <p><strong>Answer:</strong></p>
        <div style="border: 1px solid #ccc; padding: 10px; background-color: #f9f9f9;">
            {answer_html}
        </div>
        <hr>
        <a href="/test/chat">Back to chat test page</a>
        '''
    except Exception as e:
        import traceback
        return f'''
        <h1>Error</h1>
        <p>{str(e)}</p>
        <pre>{traceback.format_exc()}</pre>
        <hr>
        <a href="/test/chat">Back to chat test page</a>
        '''
