from flask import Blueprint, render_template, request, redirect, url_for, abort
from app.models import BlogPost, BlogCategory, BlogTag
from sqlalchemy import desc, func

blog = Blueprint('blog', __name__, url_prefix='/blog')

@blog.route('/')
def index():
    """Main blog index page with pagination."""
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(published=True).order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get all categories and tags for sidebar
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
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
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Get related posts (same category or tag)
    related_posts = BlogPost.query.filter(
        BlogPost.id != post.id,
        BlogPost.published == True,
        (
            (BlogPost.category_id == post.category_id) | 
            (BlogPost.tags.any(BlogTag.id.in_([tag.id for tag in post.tags])))
        )
    ).order_by(desc(BlogPost.created_at)).limit(3).all()
    
    return render_template('blog/blog_post.html', post=post, related_posts=related_posts)

@blog.route('/category/<string:slug>')
def category(slug):
    """Show posts filtered by category."""
    category = BlogCategory.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    posts = BlogPost.query.filter_by(
        published=True, 
        category_id=category.id
    ).order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get all categories and tags for sidebar
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
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
    
    posts = BlogPost.query.filter(
        BlogPost.published == True,
        BlogPost.tags.any(BlogTag.id == tag.id)
    ).order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get all categories and tags for sidebar
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
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
    posts = BlogPost.query.filter(
        BlogPost.published == True,
        (
            BlogPost.title.ilike(f'%{query}%') | 
            BlogPost.content.ilike(f'%{query}%') | 
            BlogPost.excerpt.ilike(f'%{query}%')
        )
    ).order_by(
        desc(BlogPost.created_at)
    ).paginate(page=page, per_page=6, error_out=False)
    
    # Get all categories and tags for sidebar
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
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
    """Serve blog post image from database."""
    from flask import send_file, make_response
    import io
    
    post = BlogPost.query.get_or_404(post_id)
    
    if not post.image_data:
        abort(404)
    
    # Create response with image data
    response = make_response(post.image_data)
    response.headers.set('Content-Type', 'image/png')  # Assuming PNG format
    response.headers.set('Cache-Control', 'public, max-age=31536000')  # Cache for 1 year
    
    return response
