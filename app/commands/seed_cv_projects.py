"""
CLI command: flask seed-cv-projects

Updates the CV projects in the database:
  - Replaces any trading-bot project URL with https://nis2.store/
  - Adds NIS2.store project if not present
  - Adds WhatsApp Bot Helfer project (https://whatsappbothelfer.de/) if not present
"""
import click
from flask.cli import with_appcontext
from app import db
from app.models.cv import CVProject


# ---------------------------------------------------------------------------
# Project definitions
# ---------------------------------------------------------------------------
NIS2_PROJECT = {
    'title': 'NIS2.store — Cybersecurity Compliance Platform',
    'description': (
        'Full-stack web platform for NIS2 directive compliance. '
        'Helps businesses assess, plan and document their cybersecurity obligations '
        'under the EU NIS2 regulation. Built with Python/Flask, PostgreSQL and Stripe payments.'
    ),
    'url': 'https://nis2.store/',
    'github_url': '',
    'technologies': 'Python, Flask, PostgreSQL, Stripe, SQLAlchemy, Jinja2',
    'year': '2025',
    'featured': True,
    'order_idx': 10,
}

WHATSAPP_PROJECT = {
    'title': 'WhatsApp Bot Helfer — AI Customer Service Bot',
    'description': (
        'Automated WhatsApp chatbot for German-speaking businesses. '
        'Handles customer inquiries 24/7 using AI, routes complex queries to human agents, '
        'and integrates with existing CRM workflows. No coding required for the end user.'
    ),
    'url': 'https://whatsappbothelfer.de/',
    'github_url': '',
    'technologies': 'Python, OpenAI API, WhatsApp Business API, Flask, PostgreSQL',
    'year': '2025',
    'featured': True,
    'order_idx': 20,
}


def _upsert_project(data: dict) -> str:
    """Insert or update a project by URL. Returns 'created' or 'updated'."""
    proj = CVProject.query.filter_by(url=data['url']).first()
    if proj:
        for key, value in data.items():
            setattr(proj, key, value)
        db.session.commit()
        return 'updated'
    else:
        proj = CVProject(**data)
        db.session.add(proj)
        db.session.commit()
        return 'created'


@click.command('seed-cv-projects')
@with_appcontext
def seed_cv_projects_command():
    """Seed / update CV portfolio projects (NIS2.store and WhatsApp Bot Helfer)."""

    # ── 1. Find and update any existing trading-bot project ──────────────────
    trading_keywords = ['trading', 'trade', 'bot', 'binance', 'crypto', 'arbitrage']
    old_projects = CVProject.query.all()
    replaced = []
    for proj in old_projects:
        text = f"{proj.title} {proj.description} {proj.url}".lower()
        if any(kw in text for kw in trading_keywords):
            click.echo(f"  Found old project: '{proj.title}' (url={proj.url})")
            proj.url = NIS2_PROJECT['url']
            click.echo(f"  → URL replaced with {NIS2_PROJECT['url']}")
            replaced.append(proj.id)
    if replaced:
        db.session.commit()

    # ── 2. Upsert NIS2 project ────────────────────────────────────────────────
    action = _upsert_project(NIS2_PROJECT)
    click.echo(f"NIS2.store project: {action}")

    # ── 3. Upsert WhatsApp Bot Helfer project ─────────────────────────────────
    action = _upsert_project(WHATSAPP_PROJECT)
    click.echo(f"WhatsApp Bot Helfer project: {action}")

    click.echo("✅ CV projects updated successfully.")
