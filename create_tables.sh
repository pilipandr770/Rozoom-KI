#!/bin/bash
# create_tables.sh - Create database tables using Flask-Migrate migrations

set -e

echo "=== CREATING DATABASE TABLES ==="

# Set Flask app environment
export FLASK_APP=run.py
export PYTHONPATH=.

# Check if migrations directory exists
if [ ! -d "migrations" ]; then
    echo "⚠️  No migrations directory found, initializing migrations..."
    flask db init
fi

# Check if there are any migration files
if [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "No migration files found, creating initial migration..."
    flask db migrate -m "Initial migration with all models"
fi

# Run migrations to create tables
echo "Running database migrations..."
if flask db upgrade; then
    echo "✅ Database tables created successfully via migrations"
else
    echo "⚠️  Migration failed, attempting direct table creation..."
    
    # Fallback: Use Python to create tables directly with better error handling
    python -c "
import os
os.environ['FLASK_APP'] = 'run.py'

from app import create_app, db
from sqlalchemy import text, inspect

app = create_app()

with app.app_context():
    schema = os.environ.get('POSTGRES_SCHEMA', 'rozoom_ki_schema')
    
    # Drop ALL conflicting indexes before creating tables
    try:
        with db.engine.begin() as conn:
            # Get all indexes in the schema
            result = conn.execute(text(f'''
                SELECT indexname 
                FROM pg_indexes 
                WHERE schemaname = '{schema}'
            '''))
            
            existing_indexes = [row[0] for row in result]
            print(f'Found {len(existing_indexes)} existing indexes in schema')
            
            # Drop all indexes
            for index_name in existing_indexes:
                try:
                    conn.execute(text(f'DROP INDEX IF EXISTS {schema}.{index_name}'))
                    print(f'Dropped index: {index_name}')
                except Exception as e:
                    print(f'Could not drop {index_name}: {e}')
        
        print('✅ Cleaned up all existing indexes')
    except Exception as e:
        print(f'⚠️  Could not clean indexes: {e}')
    
    # Now create all tables
    try:
        db.create_all()
        print('✅ Tables created successfully')
        
        # Verify tables were created
        inspector = inspect(db.engine)
        tables = inspector.get_table_names(schema=schema)
        print(f'✅ Created {len(tables)} tables: {', '.join(tables)}')
        
    except Exception as e:
        print(f'❌ Error creating tables: {e}')
        import traceback
        traceback.print_exc()
"
fi

echo "=== TABLE CREATION COMPLETE ==="
