#!/usr/bin/env python3
"""
Скрипт для тестирования подключения к базе данных без SSL
Используется для диагностики проблем с SSL на Render.com
"""
import os
import sys
from sqlalchemy import create_engine, text

def test_database_connection():
    """Test database connection with different SSL settings"""
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return False

    # Convert postgres:// to postgresql:// if needed
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    print(f"Original DATABASE_URL: {database_url}")

    # Test 1: Try with SSL
    print("\n=== Test 1: Connection with SSL ===")
    try:
        if '?' in database_url:
            ssl_url = database_url + '&sslmode=require'
        else:
            ssl_url = database_url + '?sslmode=require'

        engine = create_engine(ssl_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("SUCCESS: SSL connection works")
            return True
    except Exception as e:
        print(f"FAILED: SSL connection error: {e}")

    # Test 2: Try without SSL
    print("\n=== Test 2: Connection without SSL ===")
    try:
        if '?' in database_url:
            base_url = database_url.split('?')[0]
            params = database_url.split('?')[1].split('&')
            non_ssl_params = [p for p in params if not p.startswith('ssl')]
            if non_ssl_params:
                no_ssl_url = base_url + '?' + '&'.join(non_ssl_params)
            else:
                no_ssl_url = base_url
        else:
            no_ssl_url = database_url

        print(f"Trying URL without SSL: {no_ssl_url}")
        engine = create_engine(no_ssl_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("SUCCESS: Non-SSL connection works")
            print(f"Working URL: {no_ssl_url}")
            return True
    except Exception as e:
        print(f"FAILED: Non-SSL connection error: {e}")

    # Test 3: Try with explicit SSL disable
    print("\n=== Test 3: Connection with SSL explicitly disabled ===")
    try:
        base_url = database_url.split('?')[0] if '?' in database_url else database_url
        no_ssl_url = base_url + '?sslmode=disable'

        print(f"Trying URL with SSL disabled: {no_ssl_url}")
        engine = create_engine(no_ssl_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("SUCCESS: Connection with SSL disabled works")
            print(f"Working URL: {no_ssl_url}")
            return True
    except Exception as e:
        print(f"FAILED: Connection with SSL disabled error: {e}")

    print("\n=== All connection tests failed ===")
    return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
