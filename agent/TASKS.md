# TASKS (ітеративно для Copilot Agent)

## Task 01  Скелет Flask + сторінки (без Stripe)
**Goal:** каркас додатку, маршрути, базові шаблони, перемикач мов, статика.
**DoD:** запустити локально; всі сторінки відкриваються; навігація працює.
**Acceptance:** `flask run` дає 200 на /, /services, /pricing, /faq, /about, /blog, /contact, /impressum, /privacy, /terms.

## Task 02 — Контент і стилі (Tailwind)
**Goal:** базове оформлення: Hero, картки пакетів, футер/хедер, responsive.
**DoD:** Lighthouse мобайл ≥ 90, LCP < 2.5s.
**Acceptance:** семантичні теги, критичні стилі, lazy-load медіа.

## Task 03  Ліди (форма  БД + лог/емейл)
**Goal:** форма /contact пише у leads (SQLite локально), лог у консоль.
**DoD:** валідація, CSRF, reCAPTCHA v3 (поки вимкнено прапорцем).
**Acceptance:** успішний сабміт показує сторінку «дякуємо.

## Task 04  Stripe (Checkout + webhook)
**Goal:** купівля пакетів з /pricing; webhook створює Order.
**DoD:** тестові ключі, сторінка успіху/помилки, запис Order.
**Acceptance:** видно новий запис у БД після успішної оплати.

## Task 05 — SEO/Аналітика/Юридичні
**Goal:** sitemap.xml, robots.txt, schema.org, GA4/Meta Pixel, cookie banner.
**DoD:** hreflang коректний; валідація schema.org проходить.

## Task 06  Блог
**Goal:** або Markdown-дженерація, або CRUD; список, перегляд, теги.
**DoD:** meta title/description + OpenGraph на постах.
