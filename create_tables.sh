#!/bin/bash
# create_tables.sh - Create database tables using Flask-Migrate migrations

set -e

echo "=== CREATING DATABASE TABLES ==="

# Set Flask app environment
export FLASK_APP=run.py
export PYTHONPATH=.

# NUCLEAR OPTION: Drop entire schema and recreate from scratch
echo "🔥 NUCLEAR RESET: Dropping entire schema and recreating..."
if python nuclear_reset.py; then
    echo "✅ Schema dropped and recreated successfully"
else
    echo "❌ Nuclear reset failed, cannot continue"
    exit 1
fi

# Now create all tables fresh
echo "Creating tables from scratch..."

# Create tables using direct Python script (database is now clean)
python -c "
import os
os.environ['FLASK_APP'] = 'run.py'

from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    schema = os.environ.get('POSTGRES_SCHEMA', 'rozoom_ki_schema')
    
    # Database is clean, just create all tables
    try:
        db.create_all()
        print('✅ Tables created successfully')
        
        # Verify tables were created
        inspector = inspect(db.engine)
        tables = inspector.get_table_names(schema=schema)
        print(f'✅ Created {len(tables)} tables: {', '.join(tables)}')
        
        if not tables:
            print('❌ CRITICAL: No tables were created!')
            exit(1)
        
    except Exception as e:
        print(f'❌ Error creating tables: {e}')
        import traceback
        traceback.print_exc()
        exit(1)
"

echo "=== TABLE CREATION COMPLETE ==="
