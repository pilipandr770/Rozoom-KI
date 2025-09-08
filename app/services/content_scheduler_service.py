import logging
from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from typing import List, Optional, Tuple
from flask import current_app

from app import db
from app.models import ContentSchedule, GeneratedContent, BlogPost, ContentStatus, PublishFrequency, BlogTag
from app.services.openai_service import OpenAIService
from app.utils.text import generate_slug, strip_html, clean_icons_from_content

# Настройка логирования
logger = logging.getLogger(__name__)

class ContentSchedulerService:
    """
    Сервис для управления расписанием публикаций и генерации контента
    """
    
    @staticmethod
    def get_schedules_due_for_generation() -> List[ContentSchedule]:
        """
        Получает все расписания, для которых пора генерировать новый контент
        
        Returns:
            List[ContentSchedule]: Список расписаний для генерации
        """
        now = datetime.utcnow()
        
        # Получаем расписания, у которых дата следующей генерации в прошлом или не задана
        # и которые включены
        schedules = ContentSchedule.query.filter(
            and_(
                ContentSchedule.enabled == True,
                or_(
                    ContentSchedule.next_generation_date <= now,
                    ContentSchedule.next_generation_date == None
                )
            )
        ).all()
        
        return schedules
    
    @staticmethod
    def update_next_generation_date(schedule: ContentSchedule) -> None:
        """
        Обновляет дату следующей генерации контента на основе частоты
        
        Args:
            schedule (ContentSchedule): Расписание для обновления
        """
        now = datetime.utcnow()
        
        if schedule.frequency == PublishFrequency.DAILY:
            next_date = now + timedelta(days=1)
        elif schedule.frequency == PublishFrequency.WEEKLY:
            next_date = now + timedelta(weeks=1)
        elif schedule.frequency == PublishFrequency.BIWEEKLY:
            next_date = now + timedelta(weeks=2)
        else:  # MONTHLY
            next_date = now + timedelta(days=30)
        
        schedule.next_generation_date = next_date
        db.session.commit()
    
    @staticmethod
    def generate_content(schedule: ContentSchedule) -> Optional[GeneratedContent]:
        """
        Генерирует контент для заданного расписания
        
        Args:
            schedule (ContentSchedule): Расписание для генерации контента
            
        Returns:
            Optional[GeneratedContent]: Сгенерированный контент или None при ошибке
        """
        try:
            # Создаем экземпляр сервиса OpenAI
            openai_service = OpenAIService()
            
            # Создаем запись для сгенерированного контента
            generated_content = GeneratedContent(
                schedule=schedule,
                status=ContentStatus.GENERATING
            )
            db.session.add(generated_content)
            db.session.commit()
            
            # Генерируем контент на английском
            en_content = openai_service.generate_blog_content(
                topic=schedule.topic_area,
                keywords=schedule.keywords,
                language='en'
            )
            
            # Генерируем контент на немецком
            de_content = openai_service.generate_blog_content(
                topic=schedule.topic_area,
                keywords=schedule.keywords,
                language='de'
            )
            
            # Создаем промпт для изображения на основе заголовка и темы
            image_prompt = openai_service.create_image_prompt(
                blog_title=en_content['title'],
                topic=schedule.topic_area
            )
            
            # Генерируем изображение
            image_url = openai_service.generate_image(image_prompt)
            
            # Обновляем запись сгенерированного контента
            generated_content.title_en = en_content['title']
            generated_content.title_de = de_content['title']
            # Очищаем контент от иконок и других нежелательных элементов
            generated_content.content_en = clean_icons_from_content(en_content['content'])
            generated_content.content_de = clean_icons_from_content(de_content['content'])
            generated_content.meta_description_en = clean_icons_from_content(en_content.get('meta_description', ''))
            generated_content.meta_description_de = clean_icons_from_content(de_content.get('meta_description', ''))
            generated_content.image_prompt = image_prompt
            generated_content.image_url = image_url
            generated_content.keywords = schedule.keywords
            generated_content.status = ContentStatus.PUBLISHED if image_url else ContentStatus.FAILED
            if not image_url:
                generated_content.error_message = "Failed to generate image"
            
            db.session.commit()
            
            # Обновляем дату следующей генерации в расписании
            ContentSchedulerService.update_next_generation_date(schedule)
            
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            
            # Обновляем статус контента в случае ошибки
            if 'generated_content' in locals():
                generated_content.status = ContentStatus.FAILED
                generated_content.error_message = str(e)
                db.session.commit()
            
            return None
    
    @staticmethod
    def publish_content(generated_content: GeneratedContent) -> Tuple[Optional[BlogPost], Optional[BlogPost]]:
        """
        Публикует сгенерированный контент как посты в блоге
        
        Args:
            generated_content (GeneratedContent): Сгенерированный контент
            
        Returns:
            Tuple[Optional[BlogPost], Optional[BlogPost]]: Кортеж из постов на английском и немецком,
                                                         None в случае ошибки
        """
        try:
            # Создаем пост на английском
            en_post = BlogPost(
                title=generated_content.title_en,
                slug=generate_slug(generated_content.title_en),
                content=clean_icons_from_content(generated_content.content_en),
                excerpt=strip_html(generated_content.meta_description_en),
                image_url=generated_content.image_url,
                published=True,
                author_id=generated_content.schedule.author_id,
                category_id=generated_content.schedule.category_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Создаем пост на немецком
            de_post = BlogPost(
                title=generated_content.title_de,
                slug=generate_slug(generated_content.title_de) + "-de",
                content=clean_icons_from_content(generated_content.content_de),
                excerpt=strip_html(generated_content.meta_description_de),
                image_url=generated_content.image_url,
                published=True,
                author_id=generated_content.schedule.author_id,
                category_id=generated_content.schedule.category_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Добавляем ключевые слова как теги
            if generated_content.keywords:
                keywords = [k.strip() for k in generated_content.keywords.split(',')]
                for keyword in keywords:
                    if not keyword:  # Пропускаем пустые ключевые слова
                        continue
                        
                    # Проверяем, существует ли тег
                    tag = BlogTag.query.filter_by(name=keyword).first()
                    if not tag:
                        # Создаем новый тег с непустым слагом
                        slug = generate_slug(keyword)
                        if not slug:  # Если слаг пустой, используем дефолтное значение
                            slug = f"tag-{keyword.replace(' ', '-')}"
                        
                        tag = BlogTag(name=keyword, slug=slug)
                        db.session.add(tag)
                        db.session.flush()  # Убедимся, что тег сохранен перед использованием
                    
                    # Добавляем тег к постам
                    en_post.tags.append(tag)
                    de_post.tags.append(tag)
            
            # Сохраняем посты
            db.session.add(en_post)
            db.session.add(de_post)
            db.session.commit()
            
            # Обновляем ссылки в сгенерированном контенте
            generated_content.en_post_id = en_post.id
            generated_content.de_post_id = de_post.id
            generated_content.published_at = datetime.utcnow()
            db.session.commit()
            
            return en_post, de_post
            
        except Exception as e:
            logger.error(f"Error publishing content: {str(e)}")
            db.session.rollback()
            return None, None
