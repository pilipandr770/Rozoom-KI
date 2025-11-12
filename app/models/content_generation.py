from .. import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import enum


class ContentStatus(enum.Enum):
    PLANNED = "planned"
    GENERATING = "generating"
    PUBLISHED = "published"
    FAILED = "failed"


class PublishFrequency(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class ContentSchedule(db.Model):
    """
    Модель для хранения расписания автоматической генерации контента
    """
    __tablename__ = 'content_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    topic_area = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)  # Ключевые слова для SEO, разделенные запятыми
    frequency = db.Column(Enum(PublishFrequency, name='publishfrequency', native_enum=False), default=PublishFrequency.WEEKLY)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    next_generation_date = db.Column(db.DateTime)
    
    # Связи
    category_id = db.Column(db.Integer, db.ForeignKey('blog_categories.id'))
    category = relationship("BlogCategory")
    
    # Один автор может создать много расписаний
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User")
    
    # Связь с сгенерированными статьями
    generated_posts = relationship("GeneratedContent", back_populates="schedule")
    
    def __repr__(self):
        return f'<ContentSchedule {self.name}>'


class GeneratedContent(db.Model):
    """
    Модель для хранения сгенерированного контента
    """
    __tablename__ = 'generated_content'
    
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(255))
    title_de = db.Column(db.String(255))
    content_en = db.Column(db.Text)
    content_de = db.Column(db.Text)
    image_prompt = db.Column(db.Text)  # Промпт для генерации изображения
    image_url = db.Column(db.String(500))  # Локальный путь к сохраненному изображению
    original_image_url = db.Column(db.String(500))  # Оригинальный URL от OpenAI (временный)
    image_data = db.Column(db.LargeBinary)  # Бинарные данные изображения для хранения в БД
    meta_description_en = db.Column(db.Text)  # SEO-описание на английском
    meta_description_de = db.Column(db.Text)  # SEO-описание на немецком
    keywords = db.Column(db.Text)  # SEO-ключевые слова
    status = db.Column(Enum(ContentStatus, name='contentstatus', native_enum=False), default=ContentStatus.PLANNED)
    error_message = db.Column(db.Text)  # Для сохранения ошибок при генерации
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Связи
    schedule_id = db.Column(db.Integer, db.ForeignKey('content_schedules.id'))
    schedule = relationship("ContentSchedule", back_populates="generated_posts")
    
    # Связь с опубликованными постами (если статья была опубликована)
    en_post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=True)
    de_post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=True)
    en_post = relationship("BlogPost", foreign_keys=[en_post_id])
    de_post = relationship("BlogPost", foreign_keys=[de_post_id])
    
    def __repr__(self):
        return f'<GeneratedContent {self.id}>'
