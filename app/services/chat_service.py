from flask import current_app
import openai
import logging

logger = logging.getLogger(__name__)

def get_chat_response(messages, language='en'):
    """
    Get a response from the OpenAI chat API.
    
    Args:
        messages (list): List of message objects with role and content
        language (str): Language code (en, ru, de, uk)
    
    Returns:
        str: The generated response text
    """
    try:
        # Get API key from config
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            logger.error("OpenAI API key is not configured")
            return get_fallback_response(language)
        
        # Log key information (safely)
        logger.info(f"OpenAI API key configured: {'Yes' if api_key else 'No'}")
        logger.info(f"OpenAI API key length: {len(api_key) if api_key else 0}")
        logger.info(f"OpenAI API key starts with: {api_key[:4] + '...' if api_key else 'None'}")
        
        # Set up OpenAI client
        openai.api_key = api_key
        
        # Get preferred model from config
        model = current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini')
        fallback_model = current_app.config.get('OPENAI_MODEL_FALLBACK', 'gpt-3.5-turbo')
        
        logger.info(f"Using OpenAI model: {model} (fallback: {fallback_model})")
        
        # Make the API call
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
        except Exception as model_error:
            logger.warning(f"Error with primary model {model}: {str(model_error)}. Trying fallback model {fallback_model}")
            response = openai.chat.completions.create(
                model=fallback_model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
        
        # Extract and return the response text
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        return get_fallback_response(language)

def get_fallback_response(language='en'):
    """Return a fallback response when API calls fail"""
    responses = {
        'en': "I'm sorry, but I'm having trouble connecting to my knowledge database right now. Please try again in a moment.",
        'ru': "Извините, у меня возникли проблемы с подключением к моей базе знаний. Пожалуйста, попробуйте снова через минуту.",
        'de': "Es tut mir leid, aber ich habe derzeit Schwierigkeiten, eine Verbindung zu meiner Wissensdatenbank herzustellen. Bitte versuchen Sie es gleich noch einmal.",
        'uk': "Вибачте, у мене виникли проблеми з підключенням до моєї бази знань. Будь ласка, спробуйте знову через хвилину."
    }
    
    return responses.get(language, responses['en'])
