# Chat Widget Migration Implementation Plan

This document outlines the steps needed to migrate from OpenAI Assistants API to direct OpenAI API calls.

## Background

We are migrating from the deprecated OpenAI Assistants API to direct API calls. This change requires updates to both backend and frontend code.

## Implementation Steps

### 1. Update Backend Services

#### Replace assistants_service.py

```bash
# Backup original file
cp app/services/assistants_service.py app/services/assistants_service.py.bak

# Replace with fixed implementation
cp app/services/assistants_service.fixed.py app/services/assistants_service.py
```

This update:
- Removes dependencies on the deprecated Assistants API
- Implements direct OpenAI API calls with the Chat Completion API
- Ensures conversation history is properly maintained in the database

#### Add Database Migration Support

```bash
# Copy the database migration service
cp app/services/db_migrations.py app/services/db_migrations.py

# Copy the schema update script
cp app/services/update_chat_schema.py app/services/update_chat_schema.py
```

Add the following code to the app's `__init__.py` file right before the `return app` statement:

```python
# Initialize database schema for chat messages
from app.services.db_migrations import initialize_db_migrations
try:
    initialize_db_migrations()
except Exception as e:
    app.logger.error(f"Failed to initialize chat database schema: {e}")
```

### 2. Update Frontend Code

#### Fix Chat Widget JavaScript

```bash
# Backup original file
cp app/static/js/chat_widget.js app/static/js/chat_widget.js.bak

# Replace with fixed implementation
cp app/static/js/chat_widget.fixed.js app/static/js/chat_widget.js
```

The main fixes in the chat widget:
1. Fixed reference to `showTypingIndicator()` function instead of non-existent `showTyping()`
2. Made DOM element safety checks more robust
3. Improved error handling for API requests

### 3. Update Routes and Controllers (if needed)

The controller implementation seems adequate, as it already has a transition path from the Assistants API to direct API calls.

### 4. Test the Implementation

1. Start the Flask development server:
```bash
set FLASK_APP=app && set FLASK_ENV=development && flask run
```

2. Open the website in a browser and test the chat widget
3. Verify that conversations are properly stored and maintained in the database

### 5. Troubleshooting

If issues occur:
- Check browser console for JavaScript errors
- Check Flask server logs for backend errors
- Verify that the database schema was correctly updated
- Ensure the OpenAI API key is correctly set in the configuration
