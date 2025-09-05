try:
    from app import create_app, db
    from app.models import User
    
    print("Импорт успешно выполнен")
    
    app = create_app()
    print("Приложение создано")
    
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        print(f'Учетная запись админа: {admin.email}, {admin.username}' if admin else 'Администратор не найден')
        
        # Выводим все учетные записи
        users = User.query.all()
        print(f"Всего пользователей: {len(users)}")
        for user in users:
            print(f"- {user.username} ({user.email}), admin={user.is_admin}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
