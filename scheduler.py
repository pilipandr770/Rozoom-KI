"""
Скрипт для настройки и запуска планировщика задач.
Использует APScheduler для запуска задач по расписанию.
"""

import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.tasks.content_generation import generate_scheduled_content

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_scheduler():
    """
    Инициализация и запуск планировщика задач
    """
    try:
        scheduler = BackgroundScheduler()
        
        # Добавляем задачу для генерации контента
        # Запускаем каждый день в 3:00 утра
        scheduler.add_job(
            generate_scheduled_content,
            trigger=CronTrigger(hour=3, minute=0),
            id='content_generation_job',
            replace_existing=True,
            name='Generate scheduled blog content'
        )
        
        # Запускаем планировщик
        scheduler.start()
        logger.info("Scheduler started")
        
        return scheduler
    
    except Exception as e:
        logger.error(f"Error initializing scheduler: {str(e)}")
        return None

if __name__ == "__main__":
    # Запускаем планировщик напрямую для тестирования
    scheduler = init_scheduler()
    
    try:
        # Запускаем задачу один раз для проверки
        generate_scheduled_content()
        
        # Держим скрипт запущенным
        import time
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler shutdown")
