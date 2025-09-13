# routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models import BlogPost, BlogCategory, BlogTag, User, PricePackage
from app.models.project import Project, ProjectTask, ProjectUpdate
from app.models.tech_spec_submission import TechSpecSubmission
from app.auth import AdminUser
import json
import string
import random
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    """Admin logout."""
    logout_user()
    return redirect(url_for('admin.login'))

@admin.route('/')
@login_required
def dashboard():
    """Admin dashboard."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
        
    from sqlalchemy import func
    
    # Basic counts
    recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
    post_count = BlogPost.query.count()
    category_count = BlogCategory.query.count()
    tag_count = BlogTag.query.count()
    user_count = User.query.count()
    
    # Posts per category
    posts_by_category = db.session.query(
        BlogCategory.name,
        func.count(BlogPost.id).label('post_count')
    ).join(BlogPost, BlogCategory.id == BlogPost.category_id
    ).group_by(BlogCategory.name).all()
    
    # Most used tags
    popular_tags = db.session.query(
        BlogTag.name,
        func.count(BlogTag.id).label('tag_count')
    ).join(BlogTag.posts
    ).group_by(BlogTag.name
    ).order_by(func.count(BlogTag.id).desc()
    ).limit(5).all()
    
    # Posts by publish status
    published_posts = BlogPost.query.filter_by(published=True).count()
    draft_posts = post_count - published_posts
    
    return render_template(
        'admin/dashboard.html', 
        recent_posts=recent_posts, 
        post_count=post_count,
        category_count=category_count,
        tag_count=tag_count,
        user_count=user_count,
        posts_by_category=posts_by_category,
        popular_tags=popular_tags,
        published_posts=published_posts,
        draft_posts=draft_posts
    )

@admin.route('/blog/posts')
@login_required
def blog_posts():
    """List all blog posts."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/blog_posts.html', posts=posts)

@admin.route('/blog/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new blog post."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        slug = request.form.get('slug')
        category_id = request.form.get('category_id')
        image_url = request.form.get('image_url')
        published = 'published' in request.form
        
        # Get selected tags
        tag_ids = request.form.getlist('tags')
        tags = BlogTag.query.filter(BlogTag.id.in_(tag_ids)).all()
        
        # Get category
        category = BlogCategory.query.get(category_id)
        
        # Create new blog post
        post = BlogPost(
            title=title,
            content=content,
            excerpt=excerpt,
            slug=slug,
            image_url=image_url,
            published=published,
            author=current_user,
            category=category,
            tags=tags
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
    return render_template('admin/create_post.html', categories=categories, tags=tags)

@admin.route('/blog/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    """Edit a blog post."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.excerpt = request.form.get('excerpt')
        post.slug = request.form.get('slug')
        post.image_url = request.form.get('image_url')
        post.published = 'published' in request.form
        
        # Update category
        category_id = request.form.get('category_id')
        post.category = BlogCategory.query.get(category_id)
        
        # Update tags
        tag_ids = request.form.getlist('tags')
        post.tags = BlogTag.query.filter(BlogTag.id.in_(tag_ids)).all()
        
        db.session.commit()
        
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
    return render_template('admin/edit_post.html', post=post, categories=categories, tags=tags)

@admin.route('/blog/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    """Delete a blog post."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    # Разрешаем оба метода, но обрабатываем их по-разному
    if request.method == 'GET':
        flash('Для удаления поста используйте кнопку удаления на странице списка постов.', 'info')
        return redirect(url_for('admin.blog_posts'))
    
    # Отладочное сообщение
    current_app.logger.info(f"Получен запрос на удаление поста ID {id}")
    current_app.logger.debug(f"Form data: {request.form}")
    
    # Проверяем наличие CSRF токена для отладки
    if 'csrf_token' not in request.form:
        current_app.logger.error(f"CSRF token missing in delete request for post ID {id}")
        flash('Ошибка безопасности: CSRF токен отсутствует в запросе.', 'danger')
        return redirect(url_for('admin.blog_posts'))
    
    # Получаем пост
    post = BlogPost.query.get_or_404(id)
    post_title = post.title  # Запоминаем название поста для сообщения
    
    try:
        # Отвязываем все связи перед удалением
        post.tags = []
        
        # Чтобы избежать проблем с внешними ключами, проверяем связанные записи
        # Если у поста есть связи с сгенерированным контентом, сначала удаляем их
        from app.models import GeneratedContent
        generated_content = GeneratedContent.query.filter(
            (GeneratedContent.en_post_id == post.id) | 
            (GeneratedContent.de_post_id == post.id)
        ).all()
        
        for content in generated_content:
            if content.en_post_id == post.id:
                content.en_post_id = None
            if content.de_post_id == post.id:
                content.de_post_id = None
                
        db.session.commit()
        
        # Удаляем пост
        db.session.delete(post)
        db.session.commit()
        
        flash(f'Post "{post_title}" has been deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting post ID {id}: {str(e)}")
        flash(f'Error deleting post: {str(e)}', 'danger')
    
    return redirect(url_for('admin.blog_posts'))

@admin.route('/blog/categories')
@login_required
def blog_categories():
    """List all blog categories."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    categories = BlogCategory.query.all()
    return render_template('admin/blog_categories.html', categories=categories)

@admin.route('/blog/categories/create', methods=['GET', 'POST'])
@login_required
def create_category():
    """Create a new blog category."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        description = request.form.get('description')
        
        category = BlogCategory(name=name, slug=slug, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.blog_categories'))
    
    return render_template('admin/create_category.html')

@admin.route('/blog/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    """Edit a blog category."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    category = BlogCategory.query.get_or_404(id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.slug = request.form.get('slug')
        category.description = request.form.get('description')
        
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.blog_categories'))
    
    return render_template('admin/edit_category.html', category=category)

@admin.route('/blog/tags')
@login_required
def blog_tags():
    """List all blog tags."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    tags = BlogTag.query.all()
    return render_template('admin/blog_tags.html', tags=tags)

@admin.route('/blog/tags/create', methods=['GET', 'POST'])
@login_required
def create_tag():
    """Create a new blog tag."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        
        tag = BlogTag(name=name, slug=slug)
        db.session.add(tag)
        db.session.commit()
        
        flash('Tag created successfully!', 'success')
        return redirect(url_for('admin.blog_tags'))
    
    return render_template('admin/create_tag.html')

@admin.route('/blog/export')
@login_required
def export_blog_json():
    """Export blog data as JSON."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    # Custom JSON serializer for datetime objects
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    # Get all data
    posts = BlogPost.query.all()
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    
    # Format data for export
    export_data = {
        "posts": [],
        "categories": [],
        "tags": []
    }
    
    for category in categories:
        export_data["categories"].append({
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "description": category.description
        })
    
    for tag in tags:
        export_data["tags"].append({
            "id": tag.id,
            "name": tag.name,
            "slug": tag.slug
        })
    
    for post in posts:
        export_data["posts"].append({
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "content": post.content,
            "excerpt": post.excerpt,
            "image_url": post.image_url,
            "published": post.published,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "category_id": post.category_id,
            "tags": [tag.id for tag in post.tags]
        })
    
    return jsonify(export_data)

@admin.route('/blog/import', methods=['GET', 'POST'])
@login_required
def import_blog_json():
    """Import blog data from JSON."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'import_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['import_file']
        
        # If user does not select file, browser submits empty file without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file:
            try:
                import_data = json.loads(file.read())
                
                # Process categories
                if 'categories' in import_data:
                    for category_data in import_data['categories']:
                        category = BlogCategory.query.filter_by(slug=category_data['slug']).first()
                        if not category:
                            category = BlogCategory(
                                name=category_data['name'],
                                slug=category_data['slug'],
                                description=category_data.get('description', '')
                            )
                            db.session.add(category)
                
                db.session.commit()
                
                # Process tags
                if 'tags' in import_data:
                    for tag_data in import_data['tags']:
                        tag = BlogTag.query.filter_by(slug=tag_data['slug']).first()
                        if not tag:
                            tag = BlogTag(
                                name=tag_data['name'],
                                slug=tag_data['slug']
                            )
                            db.session.add(tag)
                
                db.session.commit()
                
                # Process posts
                if 'posts' in import_data:
                    for post_data in import_data['posts']:
                        post = BlogPost.query.filter_by(slug=post_data['slug']).first()
                        if not post:
                            # Get category
                            category = BlogCategory.query.get(post_data['category_id'])
                            
                            # Create post
                            post = BlogPost(
                                title=post_data['title'],
                                slug=post_data['slug'],
                                content=post_data['content'],
                                excerpt=post_data.get('excerpt', ''),
                                image_url=post_data.get('image_url', ''),
                                published=post_data.get('published', True),
                                created_at=datetime.fromisoformat(post_data['created_at']) if 'created_at' in post_data else datetime.utcnow(),
                                updated_at=datetime.fromisoformat(post_data['updated_at']) if 'updated_at' in post_data else datetime.utcnow(),
                                category=category
                            )
                            
                            # Get author (or use first user)
                            post.author = current_user
                            
                            # Add tags
                            if 'tags' in post_data:
                                post.tags = BlogTag.query.filter(BlogTag.id.in_(post_data['tags'])).all()
                            
                            db.session.add(post)
                
                db.session.commit()
                
                flash('Blog data imported successfully!', 'success')
                return redirect(url_for('admin.dashboard'))
                
            except Exception as e:
                flash(f'Error importing data: {str(e)}', 'danger')
                return redirect(request.url)
    
    return render_template('admin/import_blog.html')

@admin.route('/blog/tags/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    """Edit a blog tag."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    tag = BlogTag.query.get_or_404(id)
    
    if request.method == 'POST':
        tag.name = request.form.get('name')
        tag.slug = request.form.get('slug')
        
        db.session.commit()
        
        flash('Tag updated successfully!', 'success')
        return redirect(url_for('admin.blog_tags'))
    
    return render_template('admin/edit_tag.html', tag=tag)

@admin.route('/blog/tags/delete/<int:id>', methods=['POST'])
@login_required
def delete_tag(id):
    """Delete a blog tag."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    tag = BlogTag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    
    flash('Tag deleted successfully!', 'success')
    return redirect(url_for('admin.blog_tags'))
    
# Price Package Management Routes
@admin.route('/pricing')
@login_required
def pricing_packages():
    """List all pricing packages."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    packages = PricePackage.query.order_by(PricePackage.hours).all()
    return render_template('admin/pricing_packages.html', packages=packages)

@admin.route('/pricing/create', methods=['GET', 'POST'])
@login_required
def create_pricing_package():
    """Create a new pricing package."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        hours = request.form.get('hours')
        price_per_hour = request.form.get('price_per_hour')
        description = request.form.get('description')
        is_active = 'is_active' in request.form
        
        # Validate required fields
        if not all([name, hours, price_per_hour]):
            flash('Name, hours, and price per hour are required', 'danger')
            return redirect(url_for('admin.create_pricing_package'))
        
        try:
            hours = int(hours)
            price_per_hour = float(price_per_hour)
        except ValueError:
            flash('Hours must be an integer and price must be a number', 'danger')
            return redirect(url_for('admin.create_pricing_package'))
        
        package = PricePackage(
            name=name,
            hours=hours,
            price_per_hour=price_per_hour,
            description=description,
            is_active=is_active
        )
        
        db.session.add(package)
        db.session.commit()
        
        flash('Pricing package created successfully!', 'success')
        return redirect(url_for('admin.pricing_packages'))
    
    return render_template('admin/create_pricing_package.html')

@admin.route('/pricing/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pricing_package(id):
    """Edit a pricing package."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    package = PricePackage.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        hours = request.form.get('hours')
        price_per_hour = request.form.get('price_per_hour')
        description = request.form.get('description')
        is_active = 'is_active' in request.form
        
        # Validate required fields
        if not all([name, hours, price_per_hour]):
            flash('Name, hours, and price per hour are required', 'danger')
            return redirect(url_for('admin.edit_pricing_package', id=id))
        
        try:
            hours = int(hours)
            price_per_hour = float(price_per_hour)
        except ValueError:
            flash('Hours must be an integer and price must be a number', 'danger')
            return redirect(url_for('admin.edit_pricing_package', id=id))
        
        package.name = name
        package.hours = hours
        package.price_per_hour = price_per_hour
        package.description = description
        package.is_active = is_active
        
        db.session.commit()
        
        flash('Pricing package updated successfully!', 'success')
        return redirect(url_for('admin.pricing_packages'))
    
    return render_template('admin/edit_pricing_package.html', package=package)

@admin.route('/pricing/delete/<int:id>', methods=['POST'])
@login_required
def delete_pricing_package(id):
    """Delete a pricing package."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    package = PricePackage.query.get_or_404(id)
    db.session.delete(package)
    db.session.commit()
    
    flash('Pricing package deleted successfully!', 'success')
    return redirect(url_for('admin.pricing_packages'))

# User Management Routes
@admin.route('/users')
@login_required
def users():
    """List all users."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:user_id>')
@login_required
def user_detail(user_id):
    """View user details and projects."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)

@admin.route('/users/<int:user_id>/add_project', methods=['GET', 'POST'])
@login_required
def add_user_project(user_id):
    """Add project to user."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        start_date_str = request.form.get('start_date')
        estimated_end_date_str = request.form.get('estimated_end_date')
        budget = request.form.get('budget')
        
        # Validate required fields
        if not all([title, description, status]):
            flash('Title, description and status are required.', 'danger')
            return redirect(url_for('admin.add_user_project', user_id=user_id))
            
        # Convert dates if provided
        start_date = None
        estimated_end_date = None
        
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid start date format. Use YYYY-MM-DD.', 'danger')
                return redirect(url_for('admin.add_user_project', user_id=user_id))
                
        if estimated_end_date_str:
            try:
                estimated_end_date = datetime.strptime(estimated_end_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid estimated end date format. Use YYYY-MM-DD.', 'danger')
                return redirect(url_for('admin.add_user_project', user_id=user_id))
        
        # Create new project
        try:
            budget_value = float(budget) if budget else None
        except ValueError:
            flash('Budget must be a number.', 'danger')
            return redirect(url_for('admin.add_user_project', user_id=user_id))
            
        project = Project(
            title=title,
            description=description,
            status=status,
            start_date=start_date,
            estimated_end_date=estimated_end_date,
            budget=budget_value,
            client=user
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash(f'Project "{title}" added to user {user.name or user.email}!', 'success')
        return redirect(url_for('admin.user_detail', user_id=user_id))

# --------- Новые маршруты для работы с техническими заданиями ----------

@admin.route('/tech-specs')
@login_required
def tech_specs():
    """Список всех технических заданий"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    submissions = TechSpecSubmission.query.order_by(TechSpecSubmission.created_at.desc()).all()
    return render_template('admin/tech_specs.html', submissions=submissions)

@admin.route('/tech-spec/<int:spec_id>', methods=['GET', 'POST'])
@login_required
def tech_spec_detail(spec_id):
    """Просмотр и обработка технического задания"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    submission = TechSpecSubmission.query.get_or_404(spec_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'estimate':
            submission.status = 'estimated'
            submission.estimated_hours = float(request.form.get('estimated_hours', 0))
            submission.estimated_cost = float(request.form.get('estimated_cost', 0))
            submission.estimated_timeline = request.form.get('estimated_timeline')
            db.session.commit()
            
            # Отправка уведомления клиенту о готовой оценке
            try:
                send_estimate_notification(submission)
            except Exception as e:
                current_app.logger.error(f"Failed to send estimate notification: {e}")
            
            flash('Estimate saved successfully.', 'success')
        
        elif action == 'convert':
            # Создаем нового пользователя если email не существует
            user = User.query.filter_by(email=submission.contact_email).first()
            if not user:
                # Генерация временного пароля
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                
                user = User(
                    email=submission.contact_email,
                    name=submission.contact_name,
                    phone=submission.contact_phone,
                    company=submission.company_name,
                    is_admin=False
                )
                user.set_password(temp_password)
                db.session.add(user)
                db.session.flush()  # Получаем ID пользователя
                
                # Отправка пароля клиенту
                try:
                    send_welcome_email(user, temp_password)
                except Exception as e:
                    current_app.logger.error(f"Failed to send welcome email: {e}")
            
            # Создаем проект на основе ТЗ
            new_project = Project(
                title=f"{submission.project_type}: {submission.project_goal[:50]}...",
                description=submission.project_goal,
                status='new',
                budget=submission.estimated_cost,
                client_id=user.id,
                start_date=datetime.utcnow()
            )
            db.session.add(new_project)
            db.session.flush()  # Получаем ID проекта
            
            # Связываем ТЗ с проектом
            submission.project_id = new_project.id
            submission.status = 'approved'
            submission.client_id = user.id
            
            db.session.commit()
            flash('Project created successfully.', 'success')
            
            return redirect(url_for('admin.project_detail', project_id=new_project.id))
    
    return render_template('admin/tech_spec_detail.html', submission=submission)

@admin.route('/project-details/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_detail(project_id):
    """Подробная информация о проекте с возможностью редактирования"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_status':
            project.status = request.form.get('status')
            db.session.commit()
            flash('Project status updated.', 'success')
            
        elif action == 'add_task':
            new_task = ProjectTask(
                title=request.form.get('title'),
                description=request.form.get('description'),
                status='pending',
                project_id=project.id
            )
            if request.form.get('due_date'):
                try:
                    new_task.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
                except ValueError:
                    pass
                
            db.session.add(new_task)
            db.session.commit()
            flash('Task added.', 'success')
            
        elif action == 'update_task':
            task_id = request.form.get('task_id')
            task = ProjectTask.query.get(task_id)
            if task:
                task.status = request.form.get('task_status')
                db.session.commit()
                flash('Task updated.', 'success')
                
        elif action == 'add_update':
            new_update = ProjectUpdate(
                title=request.form.get('title'),
                content=request.form.get('content'),
                is_milestone=request.form.get('is_milestone', 'off') == 'on',
                project_id=project.id
            )
            db.session.add(new_update)
            db.session.commit()
            
            # Отправка уведомления клиенту
            try:
                send_project_update_notification(project, new_update)
            except Exception as e:
                current_app.logger.error(f"Failed to send project update notification: {e}")
            
            flash('Update added.', 'success')
    
    tasks = ProjectTask.query.filter_by(project_id=project_id).all()
    updates = ProjectUpdate.query.filter_by(project_id=project_id).order_by(ProjectUpdate.created_at.desc()).all()
    
    return render_template('admin/project_detail.html', 
                           project=project, 
                           tasks=tasks, 
                           updates=updates)

# Вспомогательные функции для отправки уведомлений
def send_estimate_notification(submission):
    """Отправка уведомления клиенту о готовой оценке"""
    # Здесь можно реализовать отправку email
    current_app.logger.info(f"Estimate notification would be sent to {submission.contact_email}")

def send_welcome_email(user, temp_password):
    """Отправка приветственного письма с временным паролем"""
    # Здесь можно реализовать отправку email
    current_app.logger.info(f"Welcome email with temporary password would be sent to {user.email}")

def send_project_update_notification(project, update):
    """Отправка уведомления об обновлении проекта"""
    # Здесь можно реализовать отправку email
    current_app.logger.info(f"Project update notification would be sent to client {project.client.email if project.client else 'unknown'}")
    
    return render_template('admin/add_user_project.html', user=user)
