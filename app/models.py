import os
from . import db
from .models.blog import BlogPost, BlogCategory, BlogTag

# In models we'll use no schema by default (let app/__init__.py handle it)
# This avoids any schema-qualified table names in the models
# For SQLite - this works as is
# For Postgres - __init__.py sets search_path to handle schemas


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))


class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    message = db.Column(db.Text)
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
    conversation_id = db.Column(db.String(36), index=True)  # UUID для группировки сообщений
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
