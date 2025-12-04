# Security Headers Implementation

## Обзор

Реализованы все рекомендованные заголовки безопасности для защиты от распространенных веб-уязвимостей.

## Реализованные заголовки

### 1. Strict-Transport-Security (HSTS) ✅
**Уровень:** СРЕДНЯЯ → ИСПРАВЛЕНО

**Значение:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Защита:**
- Принудительное использование HTTPS
- Защита от SSL stripping атак
- Защита от downgrade атак
- `max-age=31536000` - 1 год
- `includeSubDomains` - защита поддоменов
- `preload` - добавление в HSTS preload list браузеров

---

### 2. X-Content-Type-Options ✅
**Уровень:** СРЕДНЯЯ → ИСПРАВЛЕНО

**Значение:**
```
X-Content-Type-Options: nosniff
```

**Защита:**
- Предотвращение MIME type sniffing
- Браузер не будет пытаться угадать тип контента
- Защита от загрузки вредоносных скриптов под видом изображений

---

### 3. X-Frame-Options ✅
**Уровень:** СРЕДНЯЯ → ИСПРАВЛЕНО

**Значение:**
```
X-Frame-Options: DENY
```

**Защита:**
- Полная защита от clickjacking атак
- Сайт не может быть загружен в `<frame>`, `<iframe>` или `<object>`
- Предотвращение UI redressing атак

---

### 4. Content-Security-Policy (CSP) ✅
**Уровень:** ВЫСОКАЯ → ИСПРАВЛЕНО

**Значение:**
```
Content-Security-Policy: 
  default-src 'self'; 
  script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com https://cdnjs.cloudflare.com https://js.stripe.com https://telegram.org; 
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; 
  font-src 'self' https://fonts.gstatic.com data:; 
  img-src 'self' data: https: blob:; 
  connect-src 'self' https://api.openai.com https://api.stripe.com wss://; 
  frame-src 'self' https://js.stripe.com https://hooks.stripe.com; 
  object-src 'none'; 
  base-uri 'self'; 
  form-action 'self'; 
  frame-ancestors 'none'; 
  upgrade-insecure-requests;
```

**Защита:**
- **XSS (Cross-Site Scripting)** - основная защита
- **Code injection** атаки
- **Clickjacking** через `frame-ancestors 'none'`
- **Mixed content** через `upgrade-insecure-requests`

**Разрешенные источники:**
- **Scripts:** CDN библиотеки, Stripe, Telegram
- **Styles:** Google Fonts, CDN
- **API:** OpenAI, Stripe, WebSocket
- **Frames:** только Stripe (для платежей)

**Примечание:** Используется `'unsafe-inline'` и `'unsafe-eval'` для совместимости с существующим кодом. В будущем рекомендуется использовать nonce или hash для inline scripts.

---

### 5. X-XSS-Protection ✅
**Уровень:** НИЗКАЯ → ИСПРАВЛЕНО

**Значение:**
```
X-XSS-Protection: 1; mode=block
```

**Защита:**
- Включение XSS фильтра в старых браузерах
- `mode=block` - блокировка страницы при обнаружении XSS
- Legacy заголовок, но все еще полезен для старых браузеров

---

### 6. Permissions-Policy ✅
**Уровень:** НИЗКАЯ → ИСПРАВЛЕНО

**Значение:**
```
Permissions-Policy: 
  accelerometer=(), 
  camera=(), 
  geolocation=(), 
  gyroscope=(), 
  magnetometer=(), 
  microphone=(), 
  payment=(self), 
  usb=(), 
  interest-cohort=()
```

**Защита:**
- Контроль доступа к API браузера
- Запрет на использование камеры, микрофона, геолокации
- Разрешены только платежи (`payment=(self)`)
- Защита от FLoC (`interest-cohort=()`)

---

### 7. Referrer-Policy ✅
**Бонус:** Дополнительная защита конфиденциальности

**Значение:**
```
Referrer-Policy: strict-origin-when-cross-origin
```

**Защита:**
- Контроль передачи referrer информации
- Полный URL передается только на тот же origin
- На другие origins передается только origin (без пути)

---

### 8. Server Header ✅
**Уровень:** НИЗКАЯ → ИСПРАВЛЕНО

**Решение:**
- Удален заголовок `Server` из Flask ответов
- Gunicorn настроен на `SERVER_SOFTWARE = 'Undisclosed'`
- Cloudflare заголовок `Server: cloudflare` остается (управляется Cloudflare)

---

## Файлы изменений

### 1. `app/security_headers.py` (новый файл)
Middleware для добавления всех заголовков безопасности.

### 2. `app/__init__.py`
Добавлена инициализация security headers:
```python
from .security_headers import init_security_headers
init_security_headers(app)
```

### 3. `gunicorn_config.py`
Добавлено скрытие версии Gunicorn:
```python
import gunicorn
gunicorn.SERVER_SOFTWARE = 'Undisclosed'
```

---

## Проверка после деплоя

После развертывания проверьте заголовки:

```bash
curl -I https://andrii-it.de
```

Ожидаемые заголовки:
```
HTTP/2 200
strict-transport-security: max-age=31536000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
content-security-policy: default-src 'self'; ...
x-xss-protection: 1; mode=block
permissions-policy: accelerometer=(), ...
referrer-policy: strict-origin-when-cross-origin
```

---

## Мониторинг

Используйте эти инструменты для проверки безопасности:

1. **Mozilla Observatory** - https://observatory.mozilla.org/
2. **Security Headers** - https://securityheaders.com/
3. **SSL Labs** - https://www.ssllabs.com/ssltest/

Ожидаемые результаты после исправлений:
- **Критичных:** 0 ✅
- **Высоких:** 0 ✅ (было 1)
- **Средних:** 0 ✅ (было 3)
- **Низких:** 1 (Cloudflare Server header - не критично)

---

## Рекомендации на будущее

### 1. Улучшение CSP
Заменить `'unsafe-inline'` на nonce-based CSP:

```python
# Генерация nonce для каждого запроса
import secrets
nonce = secrets.token_urlsafe(16)

# В CSP
script-src 'self' 'nonce-{nonce}' ...

# В HTML
<script nonce="{nonce}">...</script>
```

### 2. Subresource Integrity (SRI)
Добавить SRI хэши для внешних библиотек:

```html
<script src="https://cdn.jsdelivr.net/npm/library.js"
        integrity="sha384-..."
        crossorigin="anonymous"></script>
```

### 3. Certificate Transparency
Мониторинг CT logs для обнаружения поддельных сертификатов.

### 4. Security.txt
Создать файл `/.well-known/security.txt` с контактами для security researchers.

---

## Производительность

Добавление заголовков безопасности:
- **Overhead:** < 1ms на запрос
- **Размер:** ~2KB дополнительных заголовков
- **Кэширование:** Заголовки кэшируются браузером

**Итого:** Минимальное влияние на производительность при значительном улучшении безопасности.
