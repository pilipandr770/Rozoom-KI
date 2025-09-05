import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set SQLite mode
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models import User, BlogPost, BlogCategory, BlogTag
from datetime import datetime, timedelta
import random

def seed_blog():
    """Seed the blog with sample data."""
    app = create_app()
    with app.app_context():
        # Create SQLite tables if they don't exist
        db.create_all()
        
        # Create categories
        categories = [
            ('Web Development', 'web-development', 'Articles about web development and design'),
            ('AI & Machine Learning', 'ai-machine-learning', 'Insights into AI and machine learning technologies'),
            ('Business & Technology', 'business-technology', 'Where business meets technology'),
            ('Product Updates', 'product-updates', 'Latest updates on our products and services')
        ]
        
        category_objects = {}
        for name, slug, description in categories:
            category = BlogCategory.query.filter_by(slug=slug).first()
            if not category:
                category = BlogCategory(name=name, slug=slug, description=description)
                db.session.add(category)
            category_objects[name] = category
        
        db.session.commit()
        
        # Create tags
        tags = [
            ('Python', 'python'),
            ('JavaScript', 'javascript'),
            ('Flask', 'flask'),
            ('React', 'react'),
            ('AI', 'ai'),
            ('Machine Learning', 'machine-learning'),
            ('Web Design', 'web-design'),
            ('Business', 'business'),
            ('Technology', 'technology'),
            ('Security', 'security')
        ]
        
        tag_objects = {}
        for name, slug in tags:
            tag = BlogTag.query.filter_by(slug=slug).first()
            if not tag:
                tag = BlogTag(name=name, slug=slug)
                db.session.add(tag)
            tag_objects[name] = tag
        
        db.session.commit()
        
        # Find an admin user or create one
        user = None
        try:
            user = User.query.first()  # Just get any user
            if not user:
                # Try to create with email only
                user = User(email='admin@rozoom-ki.com')
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            print(f"Error finding/creating user: {e}")
            db.session.rollback()
            # Try creating a minimal User
            user = User()
            db.session.add(user)
            db.session.commit()
        
        if not user:
            print("Could not create or find a user. Exiting.")
            return
        
        # Create blog posts
        sample_posts = [
            {
                'title': 'How AI is Transforming Web Development',
                'slug': 'how-ai-is-transforming-web-development',
                'content': '<p>AI is revolutionizing web development in many ways.</p>',
                'excerpt': 'Discover how AI is changing web development',
                'image_url': '/static/img/blog/ai-web-dev.jpg',
                'category': 'AI & Machine Learning',
                'tags': ['AI', 'Web Design', 'Technology']
            },
            {
                'title': 'Building Scalable Applications with Flask',
                'slug': 'building-scalable-applications-with-flask',
                'content': '<p>Learn how to build scalable Flask applications.</p>',
                'excerpt': 'Best practices for Flask scalability',
                'image_url': '/static/img/blog/flask-scaling.jpg',
                'category': 'Web Development',
                'tags': ['Python', 'Flask', 'Web Design']
            },
            {
                'title': 'Securing Your Web Applications',
                'slug': 'securing-your-web-applications',
                'content': '<p>Important security considerations for web apps.</p>',
                'excerpt': 'Learn about web application security',
                'image_url': '/static/img/blog/web-security.jpg',
                'category': 'Web Development',
                'tags': ['Security', 'Web Design']
            }
        ]
        
        for post_data in sample_posts:
            post = BlogPost.query.filter_by(slug=post_data['slug']).first()
            if not post:
                # Get category
                category = category_objects.get(post_data['category'])
                
                # Get tags
                post_tags = []
                for tag_name in post_data['tags']:
                    tag = tag_objects.get(tag_name)
                    if tag:
                        post_tags.append(tag)
                
                # Create post
                post = BlogPost(
                    title=post_data['title'],
                    slug=post_data['slug'],
                    content=post_data['content'],
                    excerpt=post_data['excerpt'],
                    image_url=post_data['image_url'],
                    published=True,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                
                # Add relationships
                post.author = user
                post.category = category
                post.tags = post_tags
                
                db.session.add(post)
        
        db.session.commit()
        print("Blog data seeded successfully!")

if __name__ == "__main__":
    seed_blog()
