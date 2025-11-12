# app/models/chat_message.py
from app import db
from datetime import datetime

class ChatMessage(db.Model):
    """
    Модель для хранения истории сообщений в чатах
    """
    __tablename__ = "chat_messages"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(64), nullable=False)  # index=True removed - causing conflicts
    thread_id = db.Column(db.String(64), nullable=True)  # Make thread_id nullable for direct API, index removed
    role = db.Column(db.String(16), nullable=False)  # 'user' или 'assistant'
    content = db.Column(db.Text, nullable=False)
    meta = db.Column(db.JSON, nullable=True)  # JSON метаданные для сообщения
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ChatMessage {self.id} {self.role} in {self.conversation_id}>"
    
    @property
    def as_dict(self) -> dict:
        """Преобразует запись в словарь для API"""
        return {
            "role": self.role,
            "content": self.content
        }
