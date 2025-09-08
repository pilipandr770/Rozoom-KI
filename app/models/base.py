import os
from datetime import datetime
from app import db
from sqlalchemy.orm import relationship


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)  # Added username field
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    password_hash = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    phone = db.Column(db.String(100))
    company = db.Column(db.String(255))
    
    # Project-related fields
    projects = relationship("Project", back_populates="client")
    
    # Blog relationships
    blog_posts = relationship("BlogPost", back_populates="author")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(255), nullable=True)
    message = db.Column(db.Text)
    data = db.Column(db.Text, nullable=True)  # JSON storage for questionnaire data
    source = db.Column(db.String(100), nullable=True)  # Where the lead came from
    status = db.Column(db.String(50), default='new')  # new, contacted, qualified, etc.
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    package = db.Column(db.String(128))
    amount = db.Column(db.Integer)
    stripe_session_id = db.Column(db.String(255))


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32))
    content = db.Column(db.Text)
    meta = db.Column(db.JSON)
    conversation_id = db.Column(db.String(36), index=True)  # UUID for grouping messages
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
