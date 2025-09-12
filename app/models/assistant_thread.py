# app/models/assistant_thread.py
from app import db
from datetime import datetime

class AssistantThread(db.Model):
    __tablename__ = "assistant_threads"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(64), index=True, unique=True, nullable=False)
    user_id = db.Column(db.String(64), index=True, nullable=False)
    language = db.Column(db.String(8), nullable=True)
    openai_thread_id = db.Column(db.String(64), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<AssistantThread conv={self.conversation_id} thread={self.openai_thread_id}>"
