import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, BlogPost, BlogCategory, BlogTag
from datetime import datetime, timedelta
import random

def seed_blog():
    """Seed the blog with sample data."""
    app = create_app()
    with app.app_context():
        # Create test user if it doesn't exist
        user = User.query.filter_by(email='admin@rozoom-ki.com').first()
        if not user:
            try:
                user = User(email='admin@rozoom-ki.com', name='Admin User')
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(f"Error creating user with name: {e}")
                # Try without name field
                db.session.rollback()
                user = User(email='admin@rozoom-ki.com')
                db.session.add(user)
                db.session.commit()
        
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
            ('Startups', 'startups'),
            ('Technology', 'technology'),
            ('Cloud', 'cloud'),
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
        
        # Create first blog post
        post1 = BlogPost.query.filter_by(slug='how-ai-is-transforming-web-development').first()
        if not post1:
            post1 = BlogPost(
                title='How AI is Transforming Web Development',
                slug='how-ai-is-transforming-web-development',
                content='<p>Artificial Intelligence (AI) is revolutionizing the web development industry in unprecedented ways. From automating repetitive tasks to enhancing user experiences through personalization, AI technologies are becoming an essential part of modern web development workflows.</p><p>One of the most significant benefits of AI in web development is automation. Developers can now use AI-powered tools to generate code, test applications, and identify bugs more efficiently than ever before.</p><p>AI is also transforming how websites interact with users. By analyzing user behavior and preferences, AI algorithms can deliver personalized content, product recommendations, and experiences tailored to individual users.</p>',
                excerpt='Discover how artificial intelligence is revolutionizing web development processes, from automated coding to personalized user experiences.',
                image_url='/static/img/blog/ai-web-dev.jpg',
                published=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                author=user,
                category=category_objects['AI & Machine Learning']
            )
            post1.tags.append(tag_objects['AI'])
            post1.tags.append(tag_objects['Web Design'])
            post1.tags.append(tag_objects['Technology'])
            db.session.add(post1)
            
        # Create second blog post
        post2 = BlogPost.query.filter_by(slug='building-scalable-applications-with-flask').first()
        if not post2:
            post2 = BlogPost(
                title='Building Scalable Applications with Flask',
                slug='building-scalable-applications-with-flask',
                content='<p>Flask\'s simplicity and flexibility make it an excellent choice for building scalable web applications. While it\'s often categorized as a microframework, Flask is capable of powering complex, high-traffic applications when properly structured and optimized.</p><p>One of Flask\'s most powerful features for scalability is Blueprints. These allow you to organize your application into discrete components, each with its own views, templates, and static files.</p><p>As your Flask application scales, database performance becomes increasingly important. Implementing effective caching is crucial for scalable applications.</p>',
                excerpt='Learn practical strategies for building highly scalable web applications using Flask.',
                image_url='/static/img/blog/flask-scaling.jpg',
                published=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                author=user,
                category=category_objects['Web Development']
            )
            post2.tags.append(tag_objects['Python'])
            post2.tags.append(tag_objects['Flask'])
            post2.tags.append(tag_objects['Web Design'])
            db.session.add(post2)
            
        # Create third blog post
        post3 = BlogPost.query.filter_by(slug='the-business-case-for-ai-integration').first()
        if not post3:
            post3 = BlogPost(
                title='The Business Case for AI Integration',
                slug='the-business-case-for-ai-integration',
                content='<p>As artificial intelligence technologies mature, businesses across industries are facing a critical decision: when and how to integrate AI into their operations and offerings. This article explores the compelling business case for AI adoption and provides a framework for evaluating AI opportunities.</p><p>While AI has generated significant hype, its business value is increasingly tangible and measurable. According to McKinsey, AI could potentially deliver additional global economic output of $13 trillion by 2030.</p><p>The most successful AI implementations focus not on technology for its own sake but on solving specific business problems and creating measurable value.</p>',
                excerpt='Explore how businesses are leveraging artificial intelligence to drive revenue growth and enhance operational efficiency.',
                image_url='/static/img/blog/business-ai.jpg',
                published=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                author=user,
                category=category_objects['Business & Technology']
            )
            post3.tags.append(tag_objects['AI'])
            post3.tags.append(tag_objects['Business'])
            post3.tags.append(tag_objects['Technology'])
            db.session.add(post3)
            
        # Create fourth blog post
        post4 = BlogPost.query.filter_by(slug='introducing-our-new-chat-widget').first()
        if not post4:
            post4 = BlogPost(
                title='Introducing Our New Chat Widget',
                slug='introducing-our-new-chat-widget',
                content='<p>We\'re excited to announce the launch of our new AI-powered chat widget, designed to enhance customer support and provide instant assistance to website visitors. This new feature represents our commitment to leveraging cutting-edge technology to improve user experience.</p><p>Our new chat widget uses advanced natural language processing to understand and respond to customer inquiries in real-time. Unlike traditional chatbots that rely on rigid decision trees, our solution can interpret complex questions, understand context, and provide relevant, helpful responses.</p>',
                excerpt='We\'re excited to announce our new AI-powered chat widget, designed to provide instant, intelligent support to all website visitors.',
                image_url='/static/img/blog/chat-widget.jpg',
                published=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                author=user,
                category=category_objects['Product Updates']
            )
            post4.tags.append(tag_objects['AI'])
            post4.tags.append(tag_objects['Technology'])
            db.session.add(post4)
            
        # Create fifth blog post
        post5 = BlogPost.query.filter_by(slug='securing-your-web-applications-best-practices').first()
        if not post5:
            post5 = BlogPost(
                title='Securing Your Web Applications: Best Practices',
                slug='securing-your-web-applications-best-practices',
                content='<p>Web application security is more critical than ever as businesses increasingly rely on web-based solutions for essential operations. With cyber threats constantly evolving, protecting your applications requires a comprehensive, proactive approach.</p><p>Never trust user input. Implement thorough validation and sanitization for all data coming into your application, regardless of source. This includes parameters in URLs, form inputs, cookies, and API responses.</p><p>Secure all communication with HTTPS, including internal APIs and administrative interfaces. Configure TLS correctly, using modern protocols and ciphers while disabling older, vulnerable options.</p>',
                excerpt='Learn essential strategies and best practices for securing your web applications against common vulnerabilities.',
                image_url='/static/img/blog/web-security.jpg',
                published=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                author=user,
                category=category_objects['Web Development']
            )
            post5.tags.append(tag_objects['Security'])
            post5.tags.append(tag_objects['Web Design'])
            post5.tags.append(tag_objects['Technology'])
            db.session.add(post5)
        
        db.session.commit()
        print("Blog data seeded successfully!")

if __name__ == "__main__":
    seed_blog()
