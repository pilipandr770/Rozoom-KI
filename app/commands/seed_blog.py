import click
from flask.cli import with_appcontext
from app import db
from app.models import User, BlogPost, BlogCategory, BlogTag
from datetime import datetime, timedelta
import random


import click
from flask.cli import with_appcontext
from app import db
from app.models import User, BlogPost, BlogCategory, BlogTag
from datetime import datetime, timedelta
import random


@click.command('seed-blog')
@with_appcontext
def seed_blog_command():
    """Seed the database with sample blog data."""
    seed_blog()
    click.echo('Seeded blog with sample data.')


def _get_or_create(model, defaults=None, **kwargs):
    obj = model.query.filter_by(**kwargs).first()
    if obj:
        return obj
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    obj = model(**params)
    db.session.add(obj)
    return obj


def seed_blog():
    """Add minimal sample blog data to the database.

    This seeder is intentionally small to avoid large literals and
    complex quoting that previously caused parse errors.
    """
    # Create a test user
    user = User.query.filter_by(email='admin@rozoom-ki.com').first()
    if not user:
        user = User(email='admin@rozoom-ki.com', name='Admin User')
        db.session.add(user)

    # Minimal set of categories
    category_defs = [
        {'name': 'Web Development', 'slug': 'web-development'},
        {'name': 'AI & Machine Learning', 'slug': 'ai-machine-learning'},
    ]

    categories = []
    for c in category_defs:
        categories.append(_get_or_create(BlogCategory, name=c['name'], slug=c['slug']))

    # Minimal set of tags
    tag_defs = ['python', 'ai', 'web-design']
    tags = []
    for slug in tag_defs:
        t = BlogTag.query.filter_by(slug=slug).first()
        if not t:
            t = BlogTag(name=slug.title(), slug=slug)
            db.session.add(t)
        tags.append(t)

    db.session.commit()

    # Minimal posts
    posts = [
        {
            'title': 'How AI is Transforming Web Development',
            'slug': 'how-ai-is-transforming-web-development',
            'content': '<p>AI is changing web development.</p>',
            'excerpt': 'Discover how AI is changing web development.',
            'image_url': '/static/img/blog/ai-web-dev.jpg',
            'category_slug': 'ai-machine-learning',
            'tags': ['ai', 'web-design'],
        },
        {
            'title': 'Building Scalable Applications with Flask',
            'slug': 'building-scalable-applications-with-flask',
            'content': '<p>Flask can be scaled with proper architecture.</p>',
            'excerpt': 'Learn strategies for scaling Flask apps.',
            'image_url': '/static/img/blog/flask-scaling.jpg',
            'category_slug': 'web-development',
            'tags': ['python'],
        },
    ]

    for p in posts:
        if BlogPost.query.filter_by(slug=p['slug']).first():
            continue
        category = BlogCategory.query.filter_by(slug=p['category_slug']).first()
        post_tags = [BlogTag.query.filter_by(slug=s).first() for s in p['tags'] if BlogTag.query.filter_by(slug=s).first()]
        post = BlogPost(
            title=p['title'],
            slug=p['slug'],
            content=p['content'],
            excerpt=p['excerpt'],
            image_url=p['image_url'],
            published=True,
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            author=user,
            category=category,
            tags=post_tags,
        )
        db.session.add(post)

    db.session.commit()
    
