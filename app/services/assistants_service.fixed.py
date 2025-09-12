from flask import current_app
import os
import logging
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

from openai import OpenAI
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.chat_message import ChatMessage

logger = logging.getLogger(__name__)

# Use a constant to easily switch between different models
DEFAULT_MODEL = "gpt-4o-2024-05-13"  # More modern and powerful model
# Fallback model if the main one is unavailable
FALLBACK_MODEL = "gpt-3.5-turbo"

def _client() -> OpenAI:
    """
    Get the OpenAI client with the API key from config.
    """
    api_key = current_app.config.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=api_key)

def get_or_create_thread(conversation_id: str, user_id: str, language: str) -> str:
    """
    Creates a unique thread ID for conversation tracking.
    Returns the thread ID to use in message history.
    """
    import uuid
    thread_id = f"thread_{uuid.uuid4().hex}"
    
    # Store the conversation in the database
    try:
        # Create a new chat message to establish the conversation
        init_message = ChatMessage(
            conversation_id=conversation_id,
            thread_id=thread_id,
            role="system",
            content=f"New conversation started. Language: {language}, User ID: {user_id}"
        )
        db.session.add(init_message)
        db.session.commit()
        logger.info(f"Created new conversation with ID: {conversation_id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception(f"DB error while creating conversation: {e}")
    
    return thread_id

def _get_assistant_prompt(kind: str) -> str:
    """
    Returns the system prompt for a specific agent type.
    """
    prompts = {
        "greeter": """
You are a greeting AI assistant for Rozoom company. Your task is:
1. Understand the user's needs
2. Provide general information about the company's services
3. Determine if the user should be redirected to a more specialized agent

Rozoom specializes in:
- Web development and web applications
- Interface design (UI/UX)
- Creating technical specifications for projects
- Digital marketing and SEO

If the user needs help creating technical specifications, suggest switching to the 'spec' agent.
If the user wants to know about the status of their project, suggest switching to the 'pm' agent.

Be polite, professional, and informative.
""",
        
        "spec": """
You are an AI specialist in creating technical specifications for Rozoom company. Your task is:
1. Help users structure requirements for their projects
2. Ask clarifying questions about functionality
3. Suggest technical solutions based on needs
4. Help estimate the scope of work and approximate timelines

Follow this structure for technical specifications:
- Project goals and objectives
- Target audience
- Functional requirements
- Technical stack
- Development phases
- Approximate implementation timeline

Ask for specific details from the user to make the technical specification as complete as possible.
""",
        
        "pm": """
You are an AI project manager for Rozoom company. Your task is:
1. Provide information about the status of current projects
2. Explain development stages
3. Inform about approximate task completion dates

You have access to user project data (if they provided an identifier).
If the user has active projects, you can check their status.
If there is no information about the user's projects, suggest registering a project or contacting a manager.

Be accurate in providing information and help the user understand at what stage their project is.
"""
    }
    
    return prompts.get(kind, prompts["greeter"])

def _get_message_history(conversation_id: str, max_messages: int = 10) -> List[Dict[str, Any]]:
    """
    Gets the message history for a specific conversation from the database.
    
    Args:
        conversation_id: Conversation ID
        max_messages: Maximum number of messages for context
        
    Returns:
        List of messages in Chat Completion API format.
    """
    try:
        # Get the latest messages for this conversation
        messages = ChatMessage.query.filter_by(
            conversation_id=conversation_id
        ).filter(
            ChatMessage.role.in_(["user", "assistant"])  # Only include actual dialogue
        ).order_by(
            ChatMessage.created_at.asc()
        ).limit(max_messages).all()
        
        # Convert to API format
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    except Exception as e:
        logger.exception(f"Error retrieving message history: {e}")
        return []

def add_user_message(thread_id: str, text: str) -> None:
    """
    Adds a user message to the chat history.
    
    Args:
        thread_id: Thread ID
        text: User message text
    """
    try:
        # Find the conversation ID from the thread ID
        conversation_message = ChatMessage.query.filter_by(thread_id=thread_id).first()
        if not conversation_message:
            logger.warning(f"Thread {thread_id} not found in database")
            return
        
        # Create a new message record
        message = ChatMessage(
            conversation_id=conversation_message.conversation_id,
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
    Generates a response using the Chat Completion API.
    
    Args:
        thread_id: Thread identifier
        assistant_kind: Agent type ("greeter", "spec", "pm")
        language: Response language
        suppress_greeting: Flag to suppress greeting
        
    Returns:
        Text response from the model
    """
    client = _client()
    
    # Get the system prompt for the selected agent
    system_prompt = _get_assistant_prompt(assistant_kind)
    
    # Add language instruction
    language_map = {
        "uk": "Ukrainian",
        "ru": "Russian",
        "en": "English",
        "de": "German"
    }
    language_name = language_map.get(language, "Ukrainian")
    system_prompt += f"\nPlease respond in {language_name}."
    
    # Add instruction to suppress greeting
    if suppress_greeting:
        system_prompt += "\nDon't greet the user again, continue the dialogue without greetings."
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Get conversation ID from thread ID
    conversation_message = ChatMessage.query.filter_by(thread_id=thread_id).first()
    if not conversation_message:
        logger.warning(f"Thread {thread_id} not found in database")
        return "Error: Conversation not found."
    
    conversation_id = conversation_message.conversation_id
    
    # Get message history from database
    history = _get_message_history(conversation_id)
    if history:
        messages.extend(history)
    
    # If there's no history, add contextual message
    if len(messages) <= 1:
        if assistant_kind == "spec":
            messages.append({
                "role": "user", 
                "content": "I want to create technical specifications for my project"
            })
        elif assistant_kind == "pm":
            messages.append({
                "role": "user", 
                "content": "I want to know about the status of my project"
            })
        else:  # greeter
            messages.append({
                "role": "user",
                "content": "Hello! Tell me what you do?"
            })
    
    # Make API request
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            assistant_message = response.choices[0].message.content
            
            # Save assistant response to history
            try:
                # Create new message record
                message = ChatMessage(
                    conversation_id=conversation_id,
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
            return "(Empty response from API)"
    except Exception as e:
        logger.exception(f"Error with OpenAI API: {e}")
        
        # Try using fallback model
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
                return "(Empty response from fallback API)"
        except Exception as fallback_e:
            logger.exception(f"Error with fallback API: {fallback_e}")
            return f"(API error: {str(e)})"
