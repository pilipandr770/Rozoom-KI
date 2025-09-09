#!/usr/bin/env python3
"""
Расширенная диагностика OpenAI API с проверкой сетевых соединений
"""
import os
import sys
import logging
import socket
import ssl
import json
import time
import traceback
from urllib.parse import urlparse

# Настройка логирования
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dns_resolution(domain):
    """Проверяет DNS-резолвинг домена"""
    print(f"🔍 Проверка DNS для {domain}...")
    try:
        # Получаем все IPv4 и IPv6 адреса
        addrs_info = socket.getaddrinfo(domain, None)
        
        ipv4_addrs = []
        ipv6_addrs = []
        
        for addr_info in addrs_info:
            family, socktype, proto, canonname, sockaddr = addr_info
            if family == socket.AF_INET:  # IPv4
                ipv4_addrs.append(sockaddr[0])
            elif family == socket.AF_INET6:  # IPv6
                ipv6_addrs.append(sockaddr[0])
        
        print(f"✅ DNS резолвинг успешен:")
        print(f"  IPv4 адреса: {', '.join(ipv4_addrs) if ipv4_addrs else 'нет'}")
        print(f"  IPv6 адреса: {', '.join(ipv6_addrs) if ipv6_addrs else 'нет'}")
        
        return True, {"ipv4": ipv4_addrs, "ipv6": ipv6_addrs}
    except Exception as e:
        print(f"❌ Ошибка DNS резолвинга: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return False, {"error": str(e)}

def check_tls_connection(domain, port=443):
    """Проверяет TLS соединение с сервером"""
    print(f"🔒 Проверка TLS соединения с {domain}:{port}...")
    try:
        # Создаем SSL контекст
        context = ssl.create_default_context()
        
        # Подключаемся через SSL
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # Получаем информацию о сертификате
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                
                print(f"✅ TLS соединение установлено:")
                print(f"  Протокол: {ssock.version()}")
                print(f"  Шифр: {cipher[0]} ({cipher[2]} бит)")
                print(f"  Сертификат выдан: {dict(cert['subject'])[('commonName',)]}")
                print(f"  Действителен до: {cert['notAfter']}")
                
                return True, {
                    "protocol": ssock.version(),
                    "cipher": cipher[0],
                    "bits": cipher[2],
                    "issuer": dict(cert['issuer'])[('commonName',)],
                    "valid_until": cert['notAfter']
                }
    except Exception as e:
        print(f"❌ Ошибка TLS соединения: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return False, {"error": str(e)}

def test_http_request(url):
    """Тестирует HTTP запрос без использования библиотек"""
    print(f"🌐 Тестирование HTTP запроса к {url}...")
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path or "/"
        
        # Создаем SSL контекст
        context = ssl.create_default_context()
        
        # Подключаемся через SSL
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # Формируем HTTP запрос
                request = f"HEAD {path} HTTP/1.1\r\n"
                request += f"Host: {domain}\r\n"
                request += "Connection: close\r\n"
                request += "User-Agent: OpenAI-Diagnostics/1.0\r\n"
                request += "\r\n"
                
                # Отправляем запрос
                ssock.send(request.encode())
                
                # Получаем ответ
                response = b""
                while True:
                    data = ssock.recv(4096)
                    if not data:
                        break
                    response += data
                
                # Парсим ответ
                response_text = response.decode('utf-8', errors='ignore')
                lines = response_text.split('\r\n')
                status_line = lines[0]
                headers = {}
                
                for line in lines[1:]:
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        headers[key] = value
                
                print(f"✅ HTTP запрос выполнен:")
                print(f"  Статус: {status_line}")
                print(f"  Сервер: {headers.get('Server', 'не указан')}")
                
                return True, {
                    "status": status_line,
                    "server": headers.get('Server', 'не указан'),
                    "headers": headers
                }
    except Exception as e:
        print(f"❌ Ошибка HTTP запроса: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return False, {"error": str(e)}

def check_openai_api():
    """Выполняет комплексную проверку подключения к OpenAI API"""
    print("🔍 Диагностика подключения к OpenAI API...\n")
    
    # 1. Проверка наличия API ключа
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY не найден в переменных окружения")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ OPENAI_API_KEY имеет неверный формат (должен начинаться с 'sk-')")
        return False
    
    print(f"✅ API ключ найден и имеет правильный формат (длина: {len(api_key)})")
    
    # 2. Проверка DNS резолвинга
    domain = "api.openai.com"
    dns_ok, dns_info = check_dns_resolution(domain)
    if not dns_ok:
        print("❌ DNS резолвинг api.openai.com не работает")
        return False
    
    # 3. Проверка TLS соединения
    tls_ok, tls_info = check_tls_connection(domain)
    if not tls_ok:
        print("❌ TLS соединение с api.openai.com не работает")
        return False
    
    # 4. Тест HTTP запроса
    http_ok, http_info = test_http_request("https://api.openai.com/v1/models")
    if not http_ok:
        print("❌ HTTP запрос к api.openai.com не работает")
        return False
    
    # 5. Проверка переменных прокси
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")
    no_proxy = os.getenv("NO_PROXY")
    
    print("\n📡 Настройки прокси:")
    print(f"  HTTP_PROXY: {http_proxy or 'не установлен'}")
    print(f"  HTTPS_PROXY: {https_proxy or 'не установлен'}")
    print(f"  NO_PROXY: {no_proxy or 'не установлен'}")
    
    # 6. Проверка блокировки IPv6
    ipv4_only = os.getenv("OPENAI_FORCE_IPV4", "false").lower() in ("true", "1", "yes")
    print(f"\n🌐 Принудительное использование IPv4: {'включено' if ipv4_only else 'выключено'}")
    
    if 'ipv6' in dns_info and dns_info['ipv6'] and not ipv4_only:
        print("ℹ️ Обнаружены IPv6 адреса, но принудительный IPv4 не включен")
        print("   Если соединения не работают, попробуйте установить OPENAI_FORCE_IPV4=true")
    
    # Общий результат
    print("\n✅ Базовое соединение с OpenAI API работает!")
    print("   Если всё равно получаете ошибки при использовании API, проверьте настройки gunicorn и патчинг gevent.")
    
    return True

if __name__ == "__main__":
    try:
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            check_openai_api()
    except Exception as e:
        print(f"❌ Ошибка при инициализации приложения: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        print("\nВыполняем диагностику без контекста приложения:")
        check_openai_api()
