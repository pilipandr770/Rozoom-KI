import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create instance directory if it doesn't exist
instance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
    print(f"Created instance directory: {instance_dir}")

# Force SQLite for development with an absolute path
db_path = os.path.abspath(os.path.join(instance_dir, 'dev.db'))
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
print(f"Using database: {os.environ['DATABASE_URL']}")

from app import create_app, db
from app.models import User, BlogPost, BlogCategory, BlogTag
from datetime import datetime, timedelta
import random
from sqlalchemy.exc import SQLAlchemyError

def seed_blog():
    """Seed the blog with sample data."""
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
        
        # Create or get a user
        try:
            user = User.query.first()
            if not user:
                # Try to create with email only (flexible with or without name)
                try:
                    user = User(email='admin@example.com')
                    db.session.add(user)
                    db.session.commit()
                    print("Created admin user with email only.")
                except SQLAlchemyError as e:
                    print(f"Error creating user with email: {e}")
                    db.session.rollback()
                    # Last resort - create with minimal info
                    try:
                        user = User()
                        db.session.add(user)
                        db.session.commit()
                        print("Created user with minimal info.")
                    except SQLAlchemyError as e2:
                        print(f"Could not create any user: {e2}")
                        db.session.rollback()
                        return
        except Exception as e:
            print(f"Error with user operations: {e}")
            return
            
        # Create categories
        categories = [
            ('Web Development', 'web-development', 'Articles about web development and design'),
            ('AI & Machine Learning', 'ai-machine-learning', 'Insights into AI and machine learning technologies'),
            ('Business & Technology', 'business-technology', 'Where business meets technology'),
            ('Product Updates', 'product-updates', 'Latest updates on our products and services')
        ]
        
        category_objects = {}
        for name, slug, description in categories:
            try:
                category = BlogCategory.query.filter_by(slug=slug).first()
                if not category:
                    category = BlogCategory(name=name, slug=slug, description=description)
                    db.session.add(category)
                category_objects[name] = category
                print(f"Processed category: {name}")
            except Exception as e:
                print(f"Error creating category {name}: {e}")
        
        try:
            db.session.commit()
            print("Categories committed successfully.")
        except SQLAlchemyError as e:
            print(f"Error committing categories: {e}")
            db.session.rollback()
        
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
            try:
                tag = BlogTag.query.filter_by(slug=slug).first()
                if not tag:
                    tag = BlogTag(name=name, slug=slug)
                    db.session.add(tag)
                tag_objects[name] = tag
                print(f"Processed tag: {name}")
            except Exception as e:
                print(f"Error creating tag {name}: {e}")
        
        try:
            db.session.commit()
            print("Tags committed successfully.")
        except SQLAlchemyError as e:
            print(f"Error committing tags: {e}")
            db.session.rollback()
        
        # Create blog posts with simplified content
        sample_posts = [
            {
                'title': 'How AI is Transforming Web Development',
                'slug': 'how-ai-is-transforming-web-development',
                'content': '<p>AI is revolutionizing web development in many ways.</p><p>From automating repetitive tasks to improving user experiences, AI tools are becoming essential for modern web developers.</p>',
                'excerpt': 'Discover how AI is changing web development',
                'image_url': '/static/img/blog/ai-web-dev.jpg',
                'category': 'AI & Machine Learning',
                'tags': ['AI', 'Web Design', 'Technology']
            },
            {
                'title': 'Building Scalable Applications with Flask',
                'slug': 'building-scalable-applications-with-flask',
                'content': '<p>Learn how to build scalable Flask applications.</p><p>This post covers essential patterns and practices for creating Flask apps that can handle growth and increased traffic.</p>',
                'excerpt': 'Best practices for Flask scalability',
                'image_url': '/static/img/blog/flask-scaling.jpg',
                'category': 'Web Development',
                'tags': ['Python', 'Flask', 'Web Design']
            },
            {
                'title': 'Securing Your Web Applications',
                'slug': 'securing-your-web-applications',
                'content': '<p>Important security considerations for web apps.</p><p>Learn about common vulnerabilities and how to protect your web applications from security threats.</p>',
                'excerpt': 'Learn about web application security',
                'image_url': '/static/img/blog/web-security.jpg',
                'category': 'Web Development',
                'tags': ['Security', 'Web Design']
            }
        ]
        
        for post_data in sample_posts:
            try:
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
                    print(f"Created post: {post_data['title']}")
            except Exception as e:
                print(f"Error creating post {post_data['title']}: {e}")
        
        try:
            db.session.commit()
            print("Blog posts committed successfully!")
        except SQLAlchemyError as e:
            print(f"Error committing blog posts: {e}")
            db.session.rollback()

if __name__ == "__main__":
    seed_blog()
    print('Seeding process completed.')
