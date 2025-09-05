from app import create_app, db
from app.models import ContentSchedule, GeneratedContent, BlogCategory, ContentStatus, PublishFrequency
from app.services.content_scheduler_service import ContentSchedulerService
from datetime import datetime

try:
    # Создаем приложение и получаем контекст
    app = create_app()
    with app.app_context():
        print("Проверяем систему автоматического контента")
        
        # Проверяем наличие расписаний
        schedules = ContentSchedule.query.all()
        print(f"Найдено расписаний: {len(schedules)}")
        
        if not schedules:
            # Создаем тестовое расписание
            print("Создаем тестовое расписание...")
            
            # Получаем категорию
            category = BlogCategory.query.first()
            if not category:
                print("Категория не найдена, создаем новую")
                category = BlogCategory(name="Технологии", slug="technology")
                db.session.add(category)
                db.session.commit()
            
            # Создаем расписание
            schedule = ContentSchedule(
                name="Тестовое расписание AI",
                topic_area="Искусственный интеллект и его применение в бизнесе",
                description="Автоматическая генерация статей про AI и его использование",
                keywords="AI, искусственный интеллект, машинное обучение, нейронные сети, бизнес",
                frequency=PublishFrequency.WEEKLY,
                category_id=category.id,
                author_id=1,  # ID администратора
                next_generation_date=datetime.utcnow()  # Сегодня
            )
            
            db.session.add(schedule)
            db.session.commit()
            print(f"Расписание создано с ID: {schedule.id}")
            
            # Генерируем контент для расписания
            print("Генерируем контент...")
            generated_content = ContentSchedulerService.generate_content(schedule)
            
            if generated_content:
                print(f"Контент успешно сгенерирован: {generated_content.id}")
                print(f"Статус: {generated_content.status.name}")
                print(f"Заголовок EN: {generated_content.title_en}")
                print(f"Заголовок DE: {generated_content.title_de}")
                
                # Публикуем контент
                if generated_content.status == ContentStatus.PUBLISHED:
                    print("Публикуем контент...")
                    en_post, de_post = ContentSchedulerService.publish_content(generated_content)
                    
                    if en_post and de_post:
                        print(f"Опубликовано два поста: EN({en_post.id}), DE({de_post.id})")
                    else:
                        print("Ошибка при публикации контента")
            else:
                print("Ошибка при генерации контента")
        else:
            # Используем существующее расписание
            schedule = schedules[0]
            print(f"Используем существующее расписание: {schedule.id} - {schedule.name}")
            
            # Генерируем контент для существующего расписания
            print("Генерируем контент...")
            generated_content = ContentSchedulerService.generate_content(schedule)
            
            if generated_content:
                print(f"Контент успешно сгенерирован: {generated_content.id}")
                print(f"Статус: {generated_content.status.name}")
                print(f"Заголовок EN: {generated_content.title_en}")
                print(f"Заголовок DE: {generated_content.title_de}")
                
                # Публикуем контент
                if generated_content.status == ContentStatus.PUBLISHED:
                    print("Публикуем контент...")
                    en_post, de_post = ContentSchedulerService.publish_content(generated_content)
                    
                    if en_post and de_post:
                        print(f"Опубликовано два поста: EN({en_post.id}), DE({de_post.id})")
                    else:
                        print("Ошибка при публикации контента")
            else:
                print("Ошибка при генерации контента")

except Exception as e:
    print(f"Произошла ошибка: {e}")
    import traceback
    traceback.print_exc()
