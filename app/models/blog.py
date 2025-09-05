from .. import db
from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Many-to-many таблица для связи постов и тегов
post_tags = Table(
    'post_tags',
    db.metadata,
    Column('post_id', Integer, ForeignKey('blog_posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('blog_tags.id'), primary_key=True)
)

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User")
    
    category_id = db.Column(db.Integer, db.ForeignKey('blog_categories.id'))
    category = relationship("BlogCategory")
    
    tags = relationship("BlogTag", secondary=post_tags, backref="posts")
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'


class BlogCategory(db.Model):
    __tablename__ = 'blog_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    posts = relationship("BlogPost", back_populates="category")
    
    def __repr__(self):
        return f'<BlogCategory {self.name}>'


class BlogTag(db.Model):
    __tablename__ = 'blog_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<BlogTag {self.name}>'
