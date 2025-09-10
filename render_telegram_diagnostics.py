# Цей файл додати до вашого проекту в Render.com
# Розмістіть його в кореневій директорії проекту

import os
import requests
import socket
import time
import sys
import logging
from datetime import datetime
from urllib3.util import connection

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

# Зберегти оригінальну функцію створення з'єднання
original_create_connection = connection.create_connection

def patched_create_connection(address, *args, **kwargs):
    """Функція для покращення DNS резолвінгу"""
    host, port = address
    
    # Для Telegram API виконуємо спеціальну логіку
    if 'api.telegram.org' in host:
        logger.info(f"Patched connection attempt to {host}:{port}")
        
        # Додаємо додаткові спроби DNS резолвінгу
        for attempt in range(3):
            try:
                # Очищаємо DNS кеш (в Linux це могло б бути "systemd-resolve --flush-caches")
                socket.getaddrinfo(host, port)
                logger.info(f"Successfully resolved {host} on attempt {attempt+1}")
                break
            except socket.gaierror:
                logger.warning(f"DNS resolution failed for {host} on attempt {attempt+1}")
                time.sleep(1)
    
    # Викликаємо оригінальну функцію
    return original_create_connection(address, *args, **kwargs)

def check_render_environment():
    """Перевірка на середовище Render.com"""
    is_render = "RENDER" in os.environ
    logger.info(f"Running on Render.com: {is_render}")
    return is_render

def check_env_variables():
    """Перевірка змінних середовища"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    results = {
        'token_exists': bool(token),
        'chat_id_exists': bool(chat_id)
    }
    
    logger.info(f"Environment check: TELEGRAM_BOT_TOKEN exists: {results['token_exists']}")
    logger.info(f"Environment check: TELEGRAM_CHAT_ID exists: {results['chat_id_exists']}")
    
    return results

def test_dns_resolution():
    """Тестування DNS резолвінгу з декількома спробами"""
    host = "api.telegram.org"
    results = []
    
    for attempt in range(3):
        try:
            start_time = time.time()
            ip_address = socket.gethostbyname(host)
            duration = time.time() - start_time
            logger.info(f"DNS resolution attempt {attempt+1}: Success, resolved to {ip_address} in {duration:.3f}s")
            results.append({"success": True, "ip": ip_address, "time": duration})
            break
        except socket.gaierror as e:
            logger.error(f"DNS resolution attempt {attempt+1} failed: {e}")
            results.append({"success": False, "error": str(e)})
            time.sleep(1)
    
    return results

def test_telegram_api():
    """Тестування доступу до Telegram API"""
    # Встановлюємо патч для створення з'єднання з покращеним DNS резолвінгом
    connection.create_connection = patched_create_connection
    
    try:
        start_time = time.time()
        response = requests.get("https://api.telegram.org/", timeout=10)
        duration = time.time() - start_time
        
        logger.info(f"API connectivity test: Status code {response.status_code}, took {duration:.3f}s")
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "time": duration
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"API connectivity test failed: {e}")
        return {"success": False, "error": str(e)}
    finally:
        # Відновлюємо оригінальну функцію
        connection.create_connection = original_create_connection

def test_telegram_message(retries=3):
    """Тестування відправки повідомлення в Telegram з повторними спробами"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        logger.error("Cannot test message sending: missing environment variables")
        return {"success": False, "error": "Missing environment variables"}
    
    # Встановлюємо патч для створення з'єднання
    connection.create_connection = patched_create_connection
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔍 Render.com Diagnostic Test\nTimestamp: {timestamp}"
    
    for attempt in range(retries):
        try:
            logger.info(f"Sending test message, attempt {attempt+1}/{retries}")
            start_time = time.time()
            
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            response = requests.post(url, data={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }, timeout=15)
            
            duration = time.time() - start_time
            
            if response.status_code == 200:
                logger.info(f"Message sent successfully in {duration:.3f}s")
                return {"success": True, "time": duration}
            else:
                logger.error(f"Failed to send message, status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Експоненційний відступ
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Error sending message on attempt {attempt+1}: {e}")
            
            if attempt < retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
    
    return {"success": False, "error": "All retry attempts failed"}
    
def run_full_diagnostics():
    """Запуск повної діагностики"""
    logger.info("=" * 60)
    logger.info("TELEGRAM API DIAGNOSTIC TOOL FOR RENDER.COM")
    logger.info("=" * 60)
    
    # Перевірка середовища
    is_render = check_render_environment()
    
    # Перевірка змінних середовища
    env_check = check_env_variables()
    
    # Тестування DNS резолвінгу
    dns_results = test_dns_resolution()
    dns_success = any(result.get("success", False) for result in dns_results)
    
    # Тестування доступу до API
    api_result = test_telegram_api()
    
    # Тестування відправки повідомлення, якщо попередні перевірки успішні
    message_result = None
    if env_check["token_exists"] and env_check["chat_id_exists"] and dns_success and api_result.get("success"):
        message_result = test_telegram_message()
    
    # Виводимо підсумковий результат
    logger.info("=" * 60)
    logger.info("DIAGNOSTIC RESULTS")
    logger.info("=" * 60)
    logger.info(f"✅ Running on Render.com: {is_render}")
    logger.info(f"{'✅' if env_check['token_exists'] else '❌'} TELEGRAM_BOT_TOKEN: {'Present' if env_check['token_exists'] else 'Missing'}")
    logger.info(f"{'✅' if env_check['chat_id_exists'] else '❌'} TELEGRAM_CHAT_ID: {'Present' if env_check['chat_id_exists'] else 'Missing'}")
    logger.info(f"{'✅' if dns_success else '❌'} DNS Resolution: {'Successful' if dns_success else 'Failed'}")
    logger.info(f"{'✅' if api_result.get('success') else '❌'} API Connectivity: {'Successful' if api_result.get('success') else 'Failed'}")
    
    if message_result:
        logger.info(f"{'✅' if message_result.get('success') else '❌'} Message Sending: {'Successful' if message_result.get('success') else 'Failed'}")
    
    # Повертаємо повний звіт
    return {
        "timestamp": datetime.now().isoformat(),
        "is_render": is_render,
        "environment": env_check,
        "dns_resolution": dns_results,
        "api_connectivity": api_result,
        "message_sending": message_result
    }

if __name__ == "__main__":
    results = run_full_diagnostics()
    
    # Записуємо результати в файл для подальшого аналізу
    with open("telegram_diagnostic_results.txt", "w") as f:
        f.write(str(results))
    
    # Повертаємо код виходу 0 якщо всі критичні перевірки успішні
    critical_success = (
        results["environment"]["token_exists"] and 
        results["environment"]["chat_id_exists"] and
        any(r.get("success", False) for r in results["dns_resolution"]) and
        results["api_connectivity"].get("success", False)
    )
    
    sys.exit(0 if critical_success else 1)
