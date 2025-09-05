# PROJECT SPEC (ТЗ)  ROZOOM-KI

## 1) Мета і KPI
- Конверсія у заявку/оплату ≥ 2–5%.
- Stripe Checkout one-time для 3–4 пакетів годин (знижка за більший обсяг).
- LCP < 2.5s мобайл; Lighthouse (mobile) ≥ 90.
- DE/EN локалізація, hreflang, schema.org/Offer для пакетів.

## 2) Сторінки (Sitemap)
- / — Hero + пакети + довіра + CTA.
- /services  перелік послуг (Python/ML/Автоматизація/Веб).
- /pricing  пакети годин: START (10h), GROW (30h), SCALE (60h), CUSTOM.
- /faq  часті питання.
- /about  про виконавця.
- /blog  статті (категорії, теги, SEO).
- /contact  форма ліда (імя, email, опис задачі, бюджет), WhatsApp-лінк.
- /impressum, /privacy, /terms  юридичні.

## 3) Функціонал
- Оплата пакетів через Stripe Checkout  webhook  Order у БД.
- Ліди: форма  БД + email/Telegram; reCAPTCHA v3.
- Блог-CRUD (через адмінку або прості Markdown-файли на старті).
- Багатомовність: DE/EN; перемикач мови; hreflang.

- База даних: используем несколько схем в PostgreSQL для разделения подсистем (см. docs/ARCHITECTURE.md). Например: `rozoom_ki_schema`, `rozoom_ki_clients`, `rozoom_ki_shop`, `rozoom_ki_projects`.

- Чат-виджет / Multi-agent: интеграция фронтенд-виджета, backend API для проксирования запросов к OpenAI и серверный multi-agent controller для маршрутизации между агентами (Sales, Tech, Billing и т.д.).

## 4) Нефункціональні
- Безпека: HTTPS/HSTS, CSP, rate-limit форм, .env.
- Доступність: WCAG 2.1 AA; alt, контраст, клавіатурність.
- SEO: sitemap.xml, robots.txt, OpenGraph, schema.org.

## 5) Приймальні критерії (MVP)
- Всі сторінки доступні, меню/футер, перемикач мов.
- /pricing показує 34 пакети, кнопка Купити веде на Stripe Checkout (test).
- Webhook створює Order у БД (можна фейкову табличку на старті).
- Ліди записуються у БД і приходять email (локально  лог).
- Lighthouse мобайл  90; валідні hreflang та schema.org.

## 6) Дані/таблиці
- users, leads, packages, orders, payments, blog_posts, translations, settings.

## 7) Стек
- Flask, Jinja2, TailwindCSS (CLI), HTMX/Alpine, PostgreSQL (або SQLite локально), Stripe.

Дополнительно: backend service для Chat-widget (OpenAI), возможно Celery/RQ для фоновой обработки и асинхронных задач (streaming ответов, модерация).
