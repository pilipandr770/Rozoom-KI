import pytest
from unittest.mock import patch
from app.utils.telegram_queue import TelegramQueue, queue_telegram_message, send_telegram_message_with_retry

def test_telegram_queue_initialization():
    """Test that TelegramQueue initializes properly"""
    queue = TelegramQueue()
    assert queue.queue == []
    assert queue.max_retries == 5
    assert queue.retry_interval == 60
    assert queue.last_attempt == 0

@patch('app.utils.telegram_queue.send_telegram_message')
def test_add_and_process_queue_success(mock_send):
    """Test adding a message to the queue and processing it successfully"""
    # Configure the mock to return True (success)
    mock_send.return_value = True
    
    queue = TelegramQueue()
    queue.add_message("Test message")
    
    # Verify the message was added and then processed successfully
    assert mock_send.called
    assert mock_send.call_count == 1
    assert mock_send.call_args[0][0] == "Test message"
    assert queue.queue == []  # Queue should be empty after successful processing

@patch('app.utils.telegram_queue.send_telegram_message')
def test_add_and_process_queue_failure(mock_send):
    """Test adding a message to the queue and handling failure"""
    # Configure the mock to return False (failure)
    mock_send.return_value = False
    
    queue = TelegramQueue()
    queue.add_message("Test message")
    
    # Verify the message was added and attempted
    assert mock_send.called
    assert mock_send.call_count == 1
    assert mock_send.call_args[0][0] == "Test message"
    
    # Verify the message is still in queue with incremented attempt count
    assert len(queue.queue) == 1
    assert queue.queue[0] == ("Test message", 1)

@patch('app.utils.telegram_queue.send_telegram_message')
def test_max_retries_exceeded(mock_send):
    """Test that messages are dropped after max retries"""
    # Configure the mock to return False (failure)
    mock_send.return_value = False
    
    queue = TelegramQueue(max_retries=3)
    queue.queue = [("Test message", 3)]  # Already at max retries
    queue.process_queue()
    
    # Verify the queue is empty after processing (message dropped)
    assert queue.queue == []

@patch('app.utils.telegram_queue.telegram_queue')
def test_queue_telegram_message(mock_queue):
    """Test the queue_telegram_message helper function"""
    queue_telegram_message("Test message")
    
    # Verify the message was added to the queue
    mock_queue.add_message.assert_called_once_with("Test message")

@patch('app.utils.telegram_queue.send_telegram_message')
@patch('app.utils.telegram_queue.queue_telegram_message')
def test_send_with_retry_success(mock_queue, mock_send):
    """Test send_telegram_message_with_retry with immediate success"""
    mock_send.return_value = True
    
    result = send_telegram_message_with_retry("Test message")
    
    # Verify the message was sent successfully and not queued
    assert result is True
    mock_send.assert_called_once_with("Test message")
    mock_queue.assert_not_called()

@patch('app.utils.telegram_queue.send_telegram_message')
@patch('app.utils.telegram_queue.queue_telegram_message')
def test_send_with_retry_fallback(mock_queue, mock_send):
    """Test send_telegram_message_with_retry with fallback to queue"""
    mock_send.return_value = False
    mock_queue.return_value = True
    
    result = send_telegram_message_with_retry("Test message")
    
    # Verify the message was queued after send failed
    assert result is True
    mock_send.assert_called_once_with("Test message")
    mock_queue.assert_called_once_with("Test message")

@patch('app.utils.telegram_queue.send_telegram_message')
@patch('app.utils.telegram_queue.queue_telegram_message')
def test_send_with_retry_exception(mock_queue, mock_send):
    """Test send_telegram_message_with_retry handling exceptions"""
    mock_send.side_effect = Exception("Test exception")
    mock_queue.return_value = True
    
    result = send_telegram_message_with_retry("Test message")
    
    # Verify the exception was caught and message was queued
    assert result is True
    mock_send.assert_called_once_with("Test message")
    mock_queue.assert_called_once_with("Test message")
