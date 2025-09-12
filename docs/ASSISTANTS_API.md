# OpenAI Assistants API Implementation

## Overview
This document explains the new chat architecture using OpenAI's Assistants API.

## Architecture

### Core Components

1. **Three Core Assistants:**
   - **ASST_GREETER:** Initial contact, understands needs, suggests next steps
   - **ASST_SPEC:** Helps create technical specifications for projects
   - **ASST_PM:** Reports project status with database access

2. **Conversation Thread System:**
   - Each conversation has one persistent OpenAI thread
   - Thread is maintained across assistant transitions
   - Thread ID is mapped to conversation ID in database

3. **Database Models:**
   - `AssistantThread`: Maps conversation_id to OpenAI thread_id

4. **Key Services:**
   - `assistants_service.py`: Core service for OpenAI Assistants API integration

## Implementation Details

### Thread Management
- Thread creation happens on first user message
- Thread persistence is managed in the `AssistantThread` model
- User messages are added to the same thread regardless of which assistant is active

### Assistant Switching
- The UI can request specific assistants via the `selected_agent` metadata field
- When switching assistants, the same thread is used to maintain conversation context
- `suppress_greeting` flag prevents assistants from repeating introductions

### Metadata Handling
- `user_id`: Stable identifier for the user (stored in localStorage)
- `language`: User's preferred language (detected or set)
- `conversation_id`: Unique identifier for the conversation
- `selected_agent`: The assistant requested by the user/UI
- `suppress_greeting`: Boolean to prevent repeated introductions

## Setup Instructions

1. **Create OpenAI Assistants:**
   - Create three assistants in the OpenAI console
   - Configure each with appropriate instructions and knowledge

2. **Environment Configuration:**
   - Add assistant IDs to the `.env` file:
     ```
     ASST_GREETER_ID=asst_...
     ASST_SPEC_ID=asst_...
     ASST_PM_ID=asst_...
     ```

3. **Database Migration:**
   - Run the migration to create the AssistantThread table:
     ```
     flask db upgrade
     ```

## Backward Compatibility
The implementation maintains backward compatibility with the existing specialist system:

- Legacy behavior is preserved if the new metadata fields aren't present
- The controller detects whether to use the new or old system based on metadata

## UI Integration
The chat widget has been updated to:
- Store a stable user_id in localStorage
- Detect the user's language from the browser
- Support assistant switching
- Maintain conversation history
