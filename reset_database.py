#!/usr/bin/env python
"""
Reset database by dropping all tables and recreating them.
Use with caution - this will delete all data!
"""
import os
import sys
from sqlalchemy import text, create_engine, inspect

def reset_database():
    """Drop all tables and indexes, then recreate schema"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not set")
        return False
    
    schema = os.environ.get('POSTGRES_SCHEMA', 'rozoom_ki_schema')
    engine = create_engine(database_url)
    
    try:
        with engine.begin() as conn:
            # Get all tables in schema
            inspector = inspect(engine)
            tables = inspector.get_table_names(schema=schema)
            
            print(f"Found {len(tables)} tables to drop: {tables}")
            
            # Drop all tables with CASCADE to remove all dependencies
            for table in tables:
                try:
                    conn.execute(text(f'DROP TABLE IF EXISTS {schema}.{table} CASCADE'))
                    print(f"✅ Dropped table: {table}")
                except Exception as e:
                    print(f"⚠️ Could not drop {table}: {e}")
            
            # Drop any remaining indexes
            result = conn.execute(text(f"""
                SELECT indexname 
                FROM pg_indexes 
                WHERE schemaname = '{schema}'
            """))
            
            indexes = [row[0] for row in result]
            print(f"Found {len(indexes)} indexes to drop: {indexes}")
            
            for index in indexes:
                try:
                    conn.execute(text(f'DROP INDEX IF EXISTS {schema}.{index} CASCADE'))
                    print(f"✅ Dropped index: {index}")
                except Exception as e:
                    print(f"⚠️ Could not drop {index}: {e}")
            
            print(f"✅ Database schema '{schema}' cleaned successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        engine.dispose()

if __name__ == '__main__':
    success = reset_database()
    sys.exit(0 if success else 1)
