import socket
import requests
import json
import os
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("telegram_connectivity_test")

def test_telegram_api_with_timeout(timeout_seconds=10):
    """
    Test connectivity to the Telegram API with a custom timeout
    
    Args:
        timeout_seconds (int): Timeout in seconds
        
    Returns:
        dict: Result of the test
    """
    start_time = time.time()
    try:
        # Create a session with retry capability
        session = requests.Session()
        retry_strategy = Retry(
            total=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        
        # Make request with timeout
        logger.info(f"Testing connection to api.telegram.org with {timeout_seconds}s timeout")
        response = session.get("https://api.telegram.org", timeout=timeout_seconds)
        
        duration = time.time() - start_time
        logger.info(f"Connection successful! Status code: {response.status_code}")
        logger.info(f"Response time: {duration:.2f} seconds")
        
        return {
            "success": True,
            "status_code": response.status_code,
            "duration": duration
        }
        
    except requests.exceptions.ConnectTimeout:
        logger.error(f"Connection timed out after {timeout_seconds} seconds")
        return {
            "success": False,
            "error_type": "timeout",
            "duration": time.time() - start_time
        }
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        return {
            "success": False,
            "error_type": "connection",
            "error_message": str(e),
            "duration": time.time() - start_time
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error_type": "other",
            "error_message": str(e),
            "duration": time.time() - start_time
        }

def test_dns_resolution():
    """
    Test DNS resolution for api.telegram.org
    
    Returns:
        dict: Result of the DNS resolution test
    """
    try:
        logger.info("Testing DNS resolution for api.telegram.org")
        start_time = time.time()
        ip_address = socket.gethostbyname("api.telegram.org")
        duration = time.time() - start_time
        
        logger.info(f"DNS resolution successful: {ip_address}")
        logger.info(f"Resolution time: {duration:.2f} seconds")
        
        return {
            "success": True,
            "ip_address": ip_address,
            "duration": duration
        }
    except socket.gaierror as e:
        logger.error(f"DNS resolution failed: {str(e)}")
        return {
            "success": False,
            "error_message": str(e),
            "duration": time.time() - start_time
        }

def test_telegram_bot_api():
    """
    Test the Telegram Bot API with the configured bot token
    
    Returns:
        dict: Result of the API test
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables")
        return {
            "success": False,
            "error_type": "configuration",
            "error_message": "Missing TELEGRAM_BOT_TOKEN environment variable"
        }
    
    try:
        logger.info("Testing Telegram Bot API with token")
        start_time = time.time()
        
        # Create a session with retry capability
        session = requests.Session()
        retry_strategy = Retry(
            total=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        
        # Make request
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = session.get(url, timeout=15)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            bot_info = response.json()
            logger.info(f"Bot API test successful! Bot name: {bot_info['result']['first_name']}")
            logger.info(f"Response time: {duration:.2f} seconds")
            return {
                "success": True,
                "bot_info": bot_info['result'],
                "duration": duration
            }
        else:
            logger.error(f"Bot API test failed with status code {response.status_code}")
            logger.error(f"Response: {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "response": response.text,
                "duration": duration
            }
    except Exception as e:
        logger.error(f"Error testing Bot API: {str(e)}")
        return {
            "success": False,
            "error_message": str(e),
            "duration": time.time() - start_time
        }

def run_all_tests():
    """
    Run all connectivity tests
    """
    results = {
        "timestamp": time.time(),
        "dns_resolution": test_dns_resolution(),
        "api_connectivity": test_telegram_api_with_timeout(),
        "bot_api": test_telegram_bot_api()
    }
    
    # Print summary
    logger.info("\n=== TEST RESULTS SUMMARY ===")
    logger.info(f"DNS Resolution: {'✓ Success' if results['dns_resolution']['success'] else '✗ Failed'}")
    logger.info(f"API Connectivity: {'✓ Success' if results['api_connectivity']['success'] else '✗ Failed'}")
    logger.info(f"Bot API: {'✓ Success' if results['bot_api']['success'] else '✗ Failed'}")
    
    return results

if __name__ == "__main__":
    results = run_all_tests()
    
    # Save results to file
    with open("telegram_connectivity_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info("Results saved to telegram_connectivity_results.json")
    
    # Exit with status code based on success
    overall_success = all([
        results["dns_resolution"]["success"],
        results["api_connectivity"]["success"],
        results["bot_api"]["success"]
    ])
    
    exit(0 if overall_success else 1)
