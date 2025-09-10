#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

from app import create_app, db
from app.auth import AdminUser

def check_admin():
    app = create_app()
    with app.app_context():
        try:
            admin = AdminUser.query.filter_by(username='admin').first()
            if admin:
                print(f'Admin exists: {admin.username}, email: {admin.email}')
                if not admin.email:
                    admin.email = 'admin@rozoom-ki.com'
                    db.session.commit()
                    print('Admin email updated')
            else:
                print('Creating admin user...')
                admin = AdminUser(username='admin', email='admin@rozoom-ki.com')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print('Admin user created')
        except Exception as e:
            print(f'Error: {e}')
            # Try to create tables
            db.create_all()
            print('Database tables created')

if __name__ == "__main__":
    check_admin()
