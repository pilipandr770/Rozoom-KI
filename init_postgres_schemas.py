#!/usr/bin/env python
"""
Initialize PostgreSQL schemas for Render deployment.
Creates the schema if it doesn't exist.
"""
import os
import sys
import psycopg2
from urllib.parse import urlparse

def create_schema():
    """Create PostgreSQL schema if it doesn't exist"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("⚠️ DATABASE_URL not set, skipping schema creation")
        return False
    
    # Parse database URL
    try:
        result = urlparse(database_url)
        connection_params = {
            'dbname': result.path[1:],
            'user': result.username,
            'password': result.password,
            'host': result.hostname,
            'port': result.port or 5432
        }
        
        schema_name = os.environ.get('POSTGRES_SCHEMA', 'rozoom_ki_schema')
        
        # Connect and create schema
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if schema exists
        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s",
            (schema_name,)
        )
        
        if cursor.fetchone():
            print(f"✅ Schema '{schema_name}' already exists")
        else:
            # Create schema
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
            print(f"✅ Schema '{schema_name}' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        return False

if __name__ == '__main__':
    success = create_schema()
    sys.exit(0 if success else 1)