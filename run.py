# run.py
# ВАЖЛИВО: патчимо gevent ДО будь-яких інших імпортів (це вже не потрібно з gthread, але залишаємо для сумісності)
try:
    import gevent.monkey as _monkey
    _monkey.patch_all()
except Exception:
    # Якщо gevent не встановлено — просто ігноруємо
    pass

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Локальний запуск (не використовується на Render)
    app.run(host='0.0.0.0', port=5000)
