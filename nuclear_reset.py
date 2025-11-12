#!/usr/bin/env python
"""
Nuclear option: Drop EVERYTHING in the schema and recreate it from scratch.
This includes all tables, indexes, sequences, functions, views, etc.
"""
import os
import sys
from sqlalchemy import text, create_engine

def nuclear_reset():
    """Drop entire schema and recreate it"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not set")
        return False
    
    schema = os.environ.get('POSTGRES_SCHEMA', 'rozoom_ki_schema')
    engine = create_engine(database_url)
    
    try:
        with engine.begin() as conn:
            print(f"🔥 NUCLEAR RESET: Dropping entire schema '{schema}'...")
            
            # Drop the entire schema and everything in it
            conn.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
            print(f"✅ Dropped schema '{schema}' with all objects")
            
            # Recreate the empty schema
            conn.execute(text(f'CREATE SCHEMA {schema}'))
            print(f"✅ Recreated empty schema '{schema}'")
            
            # Grant necessary permissions
            conn.execute(text(f'GRANT ALL ON SCHEMA {schema} TO CURRENT_USER'))
            print(f"✅ Granted permissions on schema '{schema}'")
            
            print(f"🎉 Nuclear reset complete! Schema '{schema}' is now empty and ready.")
            return True
            
    except Exception as e:
        print(f"❌ Error during nuclear reset: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        engine.dispose()

if __name__ == '__main__':
    print("⚠️  WARNING: This will delete ALL data in the schema!")
    print("⚠️  This includes all tables, indexes, sequences, and other objects.")
    print()
    success = nuclear_reset()
    sys.exit(0 if success else 1)
