from flask import Blueprint, render_template, request, redirect, url_for, abort, g
from app.models import BlogPost, BlogCategory, BlogTag
from app import db
from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload, selectinload
import time

blog = Blueprint('blog', __name__, url_prefix='/blog')

_SIDEBAR_CACHE_TTL_SECONDS = 300
_sidebar_cache = {
    'expires_at': 0.0,
    'categories': None,
    'tags': None,
}


def _use_german_posts() -> bool:
    """Use German blog variants for DE/UK UI locales."""
    return getattr(g, 'locale', 'en') in ('de', 'uk')


def _apply_locale_filter(query):
    """Filter blog posts by slug convention: German posts end with '-de'."""
    if _use_german_posts():
        return query.filter(BlogPost.slug.ilike('%-de'))
    return query.filter(~BlogPost.slug.ilike('%-de'))


def get_sidebar_data():
    """Return cached sidebar entities to cut repeat queries on list/search views."""
    now = time.time()
    if (
        _sidebar_cache['categories'] is not None
        and _sidebar_cache['tags'] is not None
        and now < _sidebar_cache['expires_at']
    ):
        return _sidebar_cache['categories'], _sidebar_cache['tags']

    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    _sidebar_cache['categories'] = categories
    _sidebar_cache['tags'] = tags
    _sidebar_cache['expires_at'] = now + _SIDEBAR_CACHE_TTL_SECONDS
    return categories, tags

@blog.route('/')
def index():
    """Main blog index page with pagination."""
    page = request.args.get('page', 1, type=int)
    posts_query = BlogPost.query.options(
        joinedload(BlogPost.category),
        selectinload(BlogPost.tags),
    ).filter_by(published=True)
    posts_query = _apply_locale_filter(posts_query)

    posts = posts_query.order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get cached categories and tags for sidebar.
    categories, tags = get_sidebar_data()
    
    return render_template(
        'blog/blog.html', 
        posts=posts, 
        categories=categories,
        tags=tags,
        current_category=None,
        current_tag=None
    )

@blog.route('/post/<string:slug>')
def post(slug):
    """Display a single blog post."""
    if _use_german_posts() and not slug.endswith('-de'):
        de_variant = BlogPost.query.filter_by(slug=f"{slug}-de", published=True).first()
        if de_variant:
            return redirect(url_for('blog.post', slug=de_variant.slug), code=302)

    post = BlogPost.query.options(
        joinedload(BlogPost.category),
        selectinload(BlogPost.tags),
    ).filter_by(slug=slug, published=True).first_or_404()
    
    # Get related posts (same category or tag)
    related_query = BlogPost.query.options(
        joinedload(BlogPost.category),
        selectinload(BlogPost.tags),
    ).filter(
        BlogPost.id != post.id,
        BlogPost.published == True,
        (
            (BlogPost.category_id == post.category_id) | 
            (BlogPost.tags.any(BlogTag.id.in_([tag.id for tag in post.tags])))
        )
    )
    related_query = _apply_locale_filter(related_query)
    related_posts = related_query.order_by(desc(BlogPost.created_at)).limit(3).all()
    
    categories, tags = get_sidebar_data()
    return render_template('blog/blog_post.html', post=post, related_posts=related_posts, categories=categories, tags=tags)

@blog.route('/category/<string:slug>')
def category(slug):
    """Show posts filtered by category."""
    category = BlogCategory.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    posts_query = BlogPost.query.options(
        joinedload(BlogPost.category),
        selectinload(BlogPost.tags),
    ).filter_by(
        published=True, 
        category_id=category.id
    )
    posts_query = _apply_locale_filter(posts_query)

    posts = posts_query.order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get cached categories and tags for sidebar.
    categories, tags = get_sidebar_data()
    
    return render_template(
        'blog/blog_category.html', 
        posts=posts, 
        category=category, 
        categories=categories,
        tags=tags,
        current_category=category,
        current_tag=None
    )

@blog.route('/tag/<string:slug>')
def tag(slug):
    """Show posts filtered by tag."""
    tag = BlogTag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    posts_query = BlogPost.query.options(
        joinedload(BlogPost.category),
        selectinload(BlogPost.tags),
    ).filter(
        BlogPost.published == True,
        BlogPost.tags.any(BlogTag.id == tag.id)
    )
    posts_query = _apply_locale_filter(posts_query)

    posts = posts_query.order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get cached categories and tags for sidebar.
    categories, tags = get_sidebar_data()
    
    return render_template(
        'blog/blog_tag.html', 
        posts=posts, 
        tag=tag, 
        categories=categories,
        tags=tags,
        current_category=None,
        current_tag=tag
    )

@blog.route('/search')
def search():
    """Search blog posts."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('blog.index'))
    
    # Search in title, content and excerpt
    posts_query = BlogPost.query.options(
        joinedload(BlogPost.category),
        selectinload(BlogPost.tags),
    ).filter(
        BlogPost.published == True,
        (
            BlogPost.title.ilike(f'%{query}%') | 
            BlogPost.content.ilike(f'%{query}%') | 
            BlogPost.excerpt.ilike(f'%{query}%')
        )
    )
    posts_query = _apply_locale_filter(posts_query)

    posts = posts_query.order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get cached categories and tags for sidebar.
    categories, tags = get_sidebar_data()
    
    return render_template(
        'blog/blog_search.html', 
        posts=posts, 
        query=query,
        categories=categories,
        tags=tags,
        current_category=None,
        current_tag=None
    )

@blog.route('/image/<int:post_id>')
def get_image(post_id):
    """Serve blog post image with deploy-safe fallback order."""
    from flask import make_response, redirect
    
    post = db.session.get(BlogPost, post_id)
    if post is None:
        abort(404)

    # 1) Serve persisted binary image first (stable across deploys)
    if post.image_data:
        data = post.image_data
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            mime = 'image/png'
        elif data[:2] == b'\xff\xd8':
            mime = 'image/jpeg'
        elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
            mime = 'image/webp'
        elif data[:6] in (b'GIF87a', b'GIF89a'):
            mime = 'image/gif'
        else:
            mime = 'image/png'

        response = make_response(data)
        response.headers.set('Content-Type', mime)
        response.headers.set('Cache-Control', 'public, max-age=31536000')
        return response

    # 2) Fallback to image_url (remote URL or static path)
    image_url = (post.image_url or '').strip()
    if image_url:
        if image_url.startswith('http://') or image_url.startswith('https://'):
            return redirect(image_url, code=302)
        if image_url.startswith('/static/'):
            return redirect(image_url, code=302)
        if image_url.startswith('static/'):
            return redirect(f'/{image_url}', code=302)

    # 3) Last fallback to original temporary image URL if present
    original_image_url = (post.original_image_url or '').strip()
    if original_image_url.startswith('http://') or original_image_url.startswith('https://'):
        return redirect(original_image_url, code=302)

    abort(404)
