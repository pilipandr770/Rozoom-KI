#!/usr/bin/env python3
"""Create or update admin user in production database"""
import os
import sys
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin_user(email, password):
    """Create or update admin user"""
    app = create_app()
    
    with app.app_context():
        print(f"🔍 Searching for user: {email}")
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            print(f"✅ User found: {user.username}")
            # Update existing user
            user.is_admin = True
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            print(f"🎉 Updated {email} to admin with new password!")
        else:
            print(f"⚠️ User not found. Creating new admin user...")
            # Create new user
            username = email.split('@')[0]
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                is_admin=True
            )
            db.session.add(user)
            db.session.commit()
            print(f"🎉 Created admin user: {username} ({email})")
        
        # Verify
        admin_count = User.query.filter_by(is_admin=True).count()
        print(f"\n✅ Total admins in database: {admin_count}")
        
        return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin_user.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    create_admin_user(email, password)
