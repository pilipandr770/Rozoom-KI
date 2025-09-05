"""
Модуль с задачами для планировщика
"""

import logging
from datetime import datetime
from app import db, create_app
from app.services.content_scheduler_service import ContentSchedulerService
from app.models import ContentStatus

# Настройка логирования
logger = logging.getLogger(__name__)

def generate_scheduled_content():
    """
    Задача для генерации запланированного контента
    Запускается через планировщик
    """
    app = create_app()
    with app.app_context():
        try:
            logger.info("Starting scheduled content generation job")
            
            # Получаем расписания, для которых пора генерировать контент
            schedules = ContentSchedulerService.get_schedules_due_for_generation()
            
            if not schedules:
                logger.info("No schedules due for content generation")
                return
            
            logger.info(f"Found {len(schedules)} schedules for content generation")
            
            # Для каждого расписания генерируем контент
            for schedule in schedules:
                try:
                    logger.info(f"Generating content for schedule {schedule.id}: {schedule.name}")
                    
                    # Генерируем контент
                    generated_content = ContentSchedulerService.generate_content(schedule)
                    
                    if generated_content and generated_content.status == ContentStatus.PUBLISHED:
                        # Публикуем сгенерированный контент
                        en_post, de_post = ContentSchedulerService.publish_content(generated_content)
                        
                        if en_post and de_post:
                            logger.info(f"Successfully generated and published content for schedule {schedule.id}")
                        else:
                            logger.error(f"Failed to publish content for schedule {schedule.id}")
                    else:
                        logger.error(f"Failed to generate content for schedule {schedule.id}")
                    
                except Exception as e:
                    logger.error(f"Error processing schedule {schedule.id}: {str(e)}")
                    continue
            
            logger.info("Finished scheduled content generation job")
            
        except Exception as e:
            logger.error(f"Error in scheduled content generation job: {str(e)}")
