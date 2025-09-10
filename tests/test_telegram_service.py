import pytest
from unittest.mock import patch, MagicMock, call
from app.services.telegram_service import send_telegram_message, send_tech_spec_notification, send_contact_form_notification
import requests
import socket

@patch('app.services.telegram_service.get_telegram_config')
@patch('app.services.telegram_service.requests.Session')
def test_send_telegram_message_success(mock_session, mock_config):
    """Test successful message sending"""
    # Setup mocks
    mock_config.return_value = ('test_token', 'test_chat_id', True)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_session.return_value.post.return_value = mock_response
    
    # Call the function
    result = send_telegram_message("Test message")
    
    # Verify the result and function calls
    assert result is True
    mock_session.return_value.post.assert_called_once()
    url = mock_session.return_value.post.call_args[0][0]
    assert "bot" in url
    assert "test_token" in url
    assert "sendMessage" in url

@patch('app.services.telegram_service.get_telegram_config')
@patch('app.services.telegram_service.requests.Session')
def test_send_telegram_message_api_error(mock_session, mock_config):
    """Test handling of API errors"""
    # Setup mocks
    mock_config.return_value = ('test_token', 'test_chat_id', True)
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = '{"error":"Bad Request"}'
    mock_session.return_value.post.return_value = mock_response
    
    # Call the function
    result = send_telegram_message("Test message")
    
    # Verify the result
    assert result is False

@patch('app.services.telegram_service.get_telegram_config')
@patch('app.services.telegram_service.requests.Session')
def test_send_telegram_message_connection_error(mock_session, mock_config):
    """Test handling of connection errors"""
    # Setup mocks
    mock_config.return_value = ('test_token', 'test_chat_id', True)
    mock_session.return_value.post.side_effect = requests.exceptions.ConnectionError("Connection failed")
    
    # Call the function
    result = send_telegram_message("Test message")
    
    # Verify the result
    assert result is False

@patch('app.services.telegram_service.get_telegram_config')
def test_send_telegram_message_invalid_config(mock_config):
    """Test handling of invalid configuration"""
    # Setup mock
    mock_config.return_value = (None, None, False)
    
    # Call the function
    result = send_telegram_message("Test message")
    
    # Verify the result
    assert result is False

@patch('app.services.telegram_service.get_telegram_config')
@patch('app.services.telegram_service.requests.Session')
def test_send_telegram_message_dns_error_with_retry(mock_session, mock_config):
    """Test handling of DNS errors with retry"""
    # Setup mocks
    mock_config.return_value = ('test_token', 'test_chat_id', True)
    
    # First call raises DNS error, second call succeeds
    mock_post = MagicMock()
    mock_post.side_effect = [
        requests.exceptions.ConnectionError("getaddrinfo failed"),
        MagicMock(status_code=200)
    ]
    mock_session.return_value.post = mock_post
    
    # Call the function
    result = send_telegram_message("Test message")
    
    # Verify the result and retry behavior
    assert result is True
    assert mock_post.call_count == 2

@patch('app.services.telegram_service.send_telegram_message')
def test_send_tech_spec_notification(mock_send):
    """Test tech spec notification formatting and sending"""
    # Setup mock
    mock_send.return_value = True
    
    # Sample tech spec data
    tech_spec_data = {
        'language': 'en',
        'answers': [
            {'question': 'Section 1', 'answer': 'Answer 1\nAnswer 2\nAnswer 3'},
            {'question': 'Section 2', 'answer': 'Answer 4\nAnswer 5'}
        ]
    }
    
    contact_info = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '123456789'
    }
    
    # Call the function
    result = send_tech_spec_notification(tech_spec_data, contact_info)
    
    # Verify the result and message formatting
    assert result is True
    assert mock_send.called
    # Check that the message contains the contact information
    message = mock_send.call_args[0][0]
    assert 'Test User' in message
    assert 'test@example.com' in message
    assert '123456789' in message
    # Check that it contains section headers
    assert 'Section 1' in message
    assert 'Section 2' in message

@patch('app.services.telegram_service.send_telegram_message')
def test_send_contact_form_notification(mock_send):
    """Test contact form notification formatting and sending"""
    # Setup mock
    mock_send.return_value = True
    
    # Sample form data
    form_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'This is a test message'
    }
    
    # Call the function
    result = send_contact_form_notification(form_data)
    
    # Verify the result and message formatting
    assert result is True
    message = mock_send.call_args[0][0]
    assert 'Test User' in message
    assert 'test@example.com' in message
    assert 'This is a test message' in message
