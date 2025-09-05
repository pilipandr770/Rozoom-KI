from app import create_app, db
from app.models import BlogCategory

app = create_app()
with app.app_context():
    categories = BlogCategory.query.all()
    print('Существующие категории блога:')
    for c in categories:
        print(f'- {c.name} (id={c.id})')
    
    if not categories:
        # Создадим базовую категорию, если нет ни одной
        print('Создаем базовую категорию "Технологии"')
        category = BlogCategory(name='Технологии', slug='technology')
        db.session.add(category)
        db.session.commit()
        print(f'Категория создана с id={category.id}')
