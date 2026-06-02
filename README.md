# Andrii-IT — IT Business Card & Client Acquisition Platform

**Live:** https://andrii-it.onrender.com | **Custom domain:** https://www.andrii-it.de

Flask-based IT freelancer platform: landing page, blog CMS with AI-generated content, AI sales chatbot, Stripe payments, multilingual (EN/DE/UK).

---

## Architecture

```
run.py                  ← Gunicorn entry point (app factory)
scheduler.py            ← APScheduler for background content generation
gunicorn_config.py      ← Production server config
app/
├── __init__.py         ← create_app() factory, blueprint registration
├── auth.py             ← AdminUser model, Flask-Login, load_user()
├── babel.py            ← Flask-Babel i18n setup (EN/DE/UK)
├── config.py           ← Config from .env
├── database.py         ← DB init, schema management, auto-seeding
├── models/             ← 21 SQLAlchemy models
├── routes/
│   ├── admin.py        ← Admin panel (blog, users, projects, payments, tech-specs)
│   ├── blog.py         ← Public blog (listing, search, categories, tags)
│   ├── auto_content.py ← AI content scheduling & publishing
│   ├── client.py       ← Client dashboard (projects, submissions)
│   ├── payment/        ← Stripe checkout flow + webhook
│   └── seo.py          ← robots.txt, sitemap.xml, ai.txt, security.txt
├── api/                ← REST API (chat endpoint)
├── pages/              ← Static pages (home, services, contact)
├── services/
│   ├── openai_service.py           ← OpenAI chat + blog content generation
│   ├── content_scheduler_service.py ← Auto-publish pipeline
│   └── telegram_service.py         ← Telegram notifications
├── agents/             ← 9 AI chat agents (greeter, pm, sales, billing, etc.)
├── commands/           ← CLI: flask seed-pricing, flask reset-admin
├── templates/          ← 40+ Jinja2 templates
├── static/
│   ├── css/            ← theme-overrides.css (single source of truth)
│   └── js/             ← chat widget, particles, animations
└── translations/       ← .po/.mo (de, uk)
```

## Key Features

| Feature | Status | Details |
|---------|--------|---------|
| Landing page | ✅ | Home, services, pricing, contact |
| AI Chat (sales bot) | ✅ | 9 agents, OpenAI Assistants API, multi-turn |
| Blog CMS | ✅ | CRUD, categories, tags, image hosting, search |
| Auto-content generation | ✅ | APScheduler + OpenAI → blog posts (EN+DE) every 30 min |
| Stripe payments | ✅ | Checkout sessions, webhooks, package pricing |
| SEO | ✅ | sitemap.xml, robots.txt, ai.txt, JSON-LD, OG tags, hreflang |
| i18n (EN/DE/UK) | ✅ | Flask-Babel, compiled .mo files |
| Client dashboard | ✅ | Project tracking, submissions, invoices |
| Admin panel | ✅ | Full CRUD for all entities |
| Tech spec questionnaire | ✅ | 15 fields, Telegram + email notification |
| Security | ✅ | CSRF, password hashing, security headers |

## Quick Start (Local Dev)

```bash
python -m venv .venv
.\.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env              # fill in values
python run.py                     # http://localhost:5000
```

## Production (Render)

- **Start command:** `gunicorn -c gunicorn_config.py run:app`
- **Database:** PostgreSQL (auto-configured via `DATABASE_URL`)
- **Environment:** Set all `.env` variables in Render dashboard

## CLI Commands

```bash
flask seed-pricing      # Seed default pricing packages
flask reset-admin       # Create/reset admin user
flask db upgrade        # Apply database migrations
```

## Environment Variables

See `.env.example` for all variables. Key ones:
- `DATABASE_URL` — PostgreSQL connection string
- `OPENAI_API_KEY` — OpenAI API key
- `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` — Stripe keys
- `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — Telegram notifications
- `SECRET_KEY` — Flask session secret

