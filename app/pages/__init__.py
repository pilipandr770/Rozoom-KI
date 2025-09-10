from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from ..models import Lead
from ..auth import AdminUser
from .. import db
import json
from flask_mail import Message
from flask_mail import Mail
from datetime import datetime
import os

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/health')
def health_check():
    """Health check endpoint для мониторинга сервиса на Render.com"""
    return jsonify({"status": "ok", "service": "rozoom-ki"}), 200

@pages_bp.route('/services')
def services():
    return render_template('services.html')
    
@pages_bp.route('/submit-questionnaire', methods=['POST'])
def submit_questionnaire():
    """Handle project questionnaire submissions."""
    try:
        # Get form data
        form_data = request.form.to_dict()
        
        # Handle multiple select and checkboxes
        if 'security_requirements' in request.form:
            form_data['security_requirements'] = request.form.getlist('security_requirements')
            
        if 'existing_assets[]' in request.form:
            form_data['existing_assets'] = request.form.getlist('existing_assets[]')
            
        # Save to database - you could create a model for this
        questionnaire_data = json.dumps(form_data)
        
        # Create a lead
        lead = Lead(
            name=form_data.get('contact_name', ''),
            email=form_data.get('contact_email', ''),
            phone=form_data.get('contact_phone', ''),
            company=form_data.get('company_name', ''),
            message=f"Project Questionnaire: {form_data.get('project_type', '')}",
            data=questionnaire_data,
            source='project_questionnaire',
            created_at=datetime.utcnow()
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Send email to admin
        try:
            send_questionnaire_notification(form_data)
        except Exception as e:
            current_app.logger.error(f"Failed to send notification email: {str(e)}")
            
        # Send notification via Telegram
        try:
            from app.services.telegram_service import send_tech_spec_notification
            
            # Prepare data for Telegram notification
            tech_spec_data = {
                'answers': []
            }
            
            # Format each question-answer pair from the form data
            # The form sends data with specific field names
            tech_spec_data['answers'].append({
                'question': 'Project Type',
                'answer': form_data.get('project_type', 'Not specified')
            })
            tech_spec_data['answers'].append({
                'question': 'Project Goal',
                'answer': form_data.get('project_goal', 'Not specified')
            })
            tech_spec_data['answers'].append({
                'question': 'Target Users',
                'answer': form_data.get('target_users', 'Not specified')
            })
            tech_spec_data['answers'].append({
                'question': 'Timeline',
                'answer': form_data.get('timeline', 'Not specified')
            })
            tech_spec_data['answers'].append({
                'question': 'Budget Range',
                'answer': form_data.get('budget_range', 'Not specified')
            })
            
            # Add language information
            tech_spec_data['language'] = 'en'  # Default to English
            
            # Prepare contact information
            contact_info = {
                'name': form_data.get('contact_name', 'Not provided'),
                'email': form_data.get('contact_email', 'Not provided'),
                'phone': form_data.get('contact_phone', 'Not provided')
            }
            
            # Try to send via Telegram
            success = send_tech_spec_notification(tech_spec_data, contact_info)
            if success:
                current_app.logger.info("Tech spec notification sent to Telegram successfully")
            else:
                current_app.logger.warning("Failed to send tech spec notification to Telegram")
                # Try to send via email as fallback
                try:
                    send_tech_spec_email_notification(tech_spec_data, contact_info)
                    current_app.logger.info("Tech spec notification sent via email as fallback")
                except Exception as email_error:
                    current_app.logger.error(f"Failed to send email fallback notification: {str(email_error)}")
                
        except Exception as e:
            current_app.logger.error(f"Failed to send Telegram notification: {str(e)}")
            # Try to send via email as fallback
            try:
                send_tech_spec_email_notification(tech_spec_data, contact_info)
                current_app.logger.info("Tech spec notification sent via email as fallback")
            except Exception as email_error:
                current_app.logger.error(f"Failed to send email fallback notification: {str(email_error)}")
            
        flash('Your project questionnaire has been submitted successfully! We will contact you soon with a time and budget estimate.', 'success')
    except Exception as e:
        current_app.logger.error(f"Error in questionnaire submission: {str(e)}")
        db.session.rollback()
        flash('There was an error processing your submission. Please try again.', 'danger')
        
    return redirect(url_for('pages.services'))
    
def send_questionnaire_notification(form_data):
    """Send email notification to admin about new questionnaire submission."""
    try:
        mail = Mail(current_app)
        
        # Get admin email
        admin = AdminUser.query.first()
        if not admin or not admin.email:
            current_app.logger.warning("No admin email found for notification")
            return
            
        # Format the email content
        project_type = form_data.get('project_type', 'Not specified')
        contact_name = form_data.get('contact_name', 'Not provided')
        contact_email = form_data.get('contact_email', 'Not provided')
        
        subject = f"New Project Questionnaire: {project_type}"
        
        # Create an HTML message with the form data
        html_content = f"""
        <h1>New Project Questionnaire Submission</h1>
        <p><strong>Submitted on:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        <p><strong>Contact:</strong> {contact_name} ({contact_email})</p>
        <p><strong>Project Type:</strong> {project_type}</p>
        
        <h2>Project Details</h2>
        <ul>
            <li><strong>Project Goal:</strong> {form_data.get('project_goal', 'Not provided')}</li>
            <li><strong>Target Users:</strong> {form_data.get('target_users', 'Not provided')}</li>
            <li><strong>Timeline:</strong> {form_data.get('timeline', 'Not specified')}</li>
            <li><strong>Budget Range:</strong> {form_data.get('budget_range', 'Not specified')}</li>
        </ul>
        
        <p>Login to the admin dashboard to view the full questionnaire details.</p>
        """
        
        msg = Message(
            subject=subject,
            recipients=[admin.email],
            html=html_content,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@rozoom-ki.com')
        )
        
        mail.send(msg)
        current_app.logger.info(f"Questionnaire notification sent to {admin.email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send questionnaire notification: {str(e)}")
        raise

def send_tech_spec_email_notification(tech_spec_data: dict, contact_info: dict):
    """Send email notification about technical specification submission."""
    try:
        mail = Mail(current_app)
        
        # Get admin email
        admin = AdminUser.query.first()
        if not admin or not admin.email:
            current_app.logger.warning("No admin email found for tech spec notification")
            return
            
        # Format the email content
        subject = f"New Technical Specification: {contact_info.get('name', 'Unknown')}"
        
        html_content = f"""
        <h1>New Technical Specification Submission</h1>
        <p><strong>Submitted on:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        
        <h2>Contact Information</h2>
        <ul>
            <li><strong>Name:</strong> {contact_info.get('name', 'Not provided')}</li>
            <li><strong>Email:</strong> {contact_info.get('email', 'Not provided')}</li>
            <li><strong>Phone:</strong> {contact_info.get('phone', 'Not provided')}</li>
        </ul>
        
        <h2>Technical Specification Details</h2>
        """
        
        # Add each answer
        for i, answer in enumerate(tech_spec_data.get('answers', [])):
            html_content += f"""
            <h3>{i+1}. {answer.get('question', 'Question')}</h3>
            <p>{answer.get('answer', 'No answer')}</p>
            """
        
        html_content += """
        <p>Please review the technical specification and contact the client as soon as possible.</p>
        <p>Login to the admin dashboard to view the full details.</p>
        """
        
        msg = Message(
            subject=subject,
            recipients=[admin.email],
            html=html_content,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@rozoom-ki.com')
        )
        
        mail.send(msg)
        current_app.logger.info(f"Tech spec email notification sent to {admin.email}")
        
    except Exception as e:
        current_app.logger.error(f"Failed to send tech spec email notification: {str(e)}")
        raise

@pages_bp.route('/pricing')
def pricing():
    from app.models import PricePackage
    packages = PricePackage.query.filter_by(is_active=True).order_by(PricePackage.hours).all()
    return render_template('pricing.html', packages=packages)

@pages_bp.route('/faq')
def faq():
    return render_template('faq.html')

@pages_bp.route('/about')
def about():
    return render_template('about.html')

@pages_bp.route('/blog')
@pages_bp.route('/blog/page/<int:page>')
def blog(page=1):
    # Get blog posts with pagination
    from app.models import BlogPost, BlogCategory, BlogTag
    
    posts_per_page = 6
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=posts_per_page, error_out=False)
    
    # Get categories with post count
    categories = db.session.query(
        BlogCategory, 
        db.func.count(BlogPost.id).label('count')
    ).outerjoin(BlogPost).filter(
        (BlogPost.published == True) | (BlogPost.id == None)
    ).group_by(BlogCategory.id).all()
    
    # Format categories for template
    formatted_categories = [
        {'name': c.BlogCategory.name, 'slug': c.BlogCategory.slug, 'count': c.count} 
        for c in categories
    ]
    
    # Get popular tags
    tags = db.session.query(
        BlogTag, 
        db.func.count(BlogPost.id).label('count')
    ).join(BlogTag.posts).filter(
        BlogPost.published == True
    ).group_by(BlogTag.id).order_by(
        db.func.count(BlogPost.id).desc()
    ).limit(15).all()
    
    # Format tags for template
    formatted_tags = [
        {'name': t.BlogTag.name, 'slug': t.BlogTag.slug, 'count': t.count} 
        for t in tags
    ]
    
    # Get recent posts
    recent_posts = BlogPost.query.filter_by(
        published=True
    ).order_by(
        BlogPost.created_at.desc()
    ).limit(5).all()
    
    return render_template(
        'blog.html',
        posts=posts.items,
        pagination=posts,
        categories=formatted_categories,
        tags=formatted_tags,
        recent_posts=recent_posts
    )

@pages_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    error = None
    success = False
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        privacy_consent = request.form.get('privacy_consent')
        
        # Validate form data
        if not name:
            error = "Please enter your name."
        elif not email:
            error = "Please enter your email address."
        elif not '@' in email or '.' not in email:
            error = "Please enter a valid email address."
        elif not message:
            error = "Please enter your message."
        elif not privacy_consent:
            error = "You must consent to our privacy policy."
        else:
            try:
                # Create and save lead in the database
                lead = Lead(name=name, email=email, message=message)
                db.session.add(lead)
                db.session.commit()
                
                # Send notification via Telegram
                try:
                    from app.services import send_contact_form_notification
                    form_data = {
                        'name': name,
                        'email': email,
                        'message': message
                    }
                    send_contact_form_notification(form_data)
                except Exception as e:
                    # Log the error but don't disrupt the user experience
                    print(f"Failed to send Telegram notification: {str(e)}")
                
                success = True
            except Exception as e:
                db.session.rollback()
                error = "An error occurred. Please try again later."
                print(f"Database error: {e}")
    
    return render_template('contact.html', error=error, success=success)

@pages_bp.route('/impressum')
def impressum():
    # Check current language and use appropriate template
    from flask import g
    if g.locale == 'de':
        return render_template('de/impressum.html')
    elif g.locale == 'ru':
        return render_template('ru/impressum.html')
    else:
        return render_template('impressum.html')

@pages_bp.route('/privacy')
def privacy():
    # Check current language and use appropriate template
    from flask import g
    if g.locale == 'de':
        return render_template('de/privacy.html')
    elif g.locale == 'ru':
        return render_template('ru/privacy.html')
    else:
        return render_template('privacy.html')

@pages_bp.route('/terms')
def terms():
    # Check current language and use appropriate template
    from flask import g
    if g.locale == 'de':
        return render_template('de/terms.html')
    elif g.locale == 'ru':
        return render_template('ru/terms.html')
    else:
        return render_template('terms.html')

@pages_bp.route('/blog/<slug>')
def blog_post(slug):
    from app.models import BlogPost, BlogCategory, BlogTag
    
    # Get post by slug
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Get previous and next posts
    prev_post = BlogPost.query.filter(
        BlogPost.published == True,
        BlogPost.created_at < post.created_at
    ).order_by(BlogPost.created_at.desc()).first()
    
    next_post = BlogPost.query.filter(
        BlogPost.published == True,
        BlogPost.created_at > post.created_at
    ).order_by(BlogPost.created_at.asc()).first()
    
    # Get related posts
    if post.category:
        related_posts = BlogPost.query.filter(
            BlogPost.published == True,
            BlogPost.id != post.id,
            BlogPost.category_id == post.category_id
        ).order_by(
            BlogPost.created_at.desc()
        ).limit(3).all()
    else:
        related_posts = BlogPost.query.filter(
            BlogPost.published == True,
            BlogPost.id != post.id
        ).order_by(
            BlogPost.created_at.desc()
        ).limit(3).all()
    
    # Get post's tags as strings
    post_tags = [tag.name for tag in post.tags] if post.tags else []
    
    return render_template(
        'blog_post.html',
        post=post,
        prev_post=prev_post,
        next_post=next_post,
        related_posts=related_posts,
        tags=post_tags
    )

@pages_bp.route('/blog/category/<category>')
@pages_bp.route('/blog/category/<category>/page/<int:page>')
def blog_category(category, page=1):
    from app.models import BlogPost, BlogCategory, BlogTag
    
    # Get category
    category_obj = BlogCategory.query.filter_by(slug=category).first_or_404()
    
    # Get posts in category with pagination
    posts_per_page = 6
    posts = BlogPost.query.filter_by(
        category_id=category_obj.id,
        published=True
    ).order_by(
        BlogPost.created_at.desc()
    ).paginate(
        page=page,
        per_page=posts_per_page,
        error_out=False
    )
    
    # Get all categories with post count
    categories = db.session.query(
        BlogCategory, 
        db.func.count(BlogPost.id).label('count')
    ).outerjoin(BlogPost).filter(
        (BlogPost.published == True) | (BlogPost.id == None)
    ).group_by(BlogCategory.id).all()
    
    # Format categories for template
    formatted_categories = [
        {'name': c.BlogCategory.name, 'slug': c.BlogCategory.slug, 'count': c.count} 
        for c in categories
    ]
    
    # Get recent posts
    recent_posts = BlogPost.query.filter_by(
        published=True
    ).order_by(
        BlogPost.created_at.desc()
    ).limit(5).all()
    
    return render_template(
        'blog_category.html',
        category=category_obj.name,
        posts=posts.items,
        pagination=posts,
        categories=formatted_categories,
        recent_posts=recent_posts
    )

@pages_bp.route('/blog/tag/<tag>')
@pages_bp.route('/blog/tag/<tag>/page/<int:page>')
def blog_tag(tag, page=1):
    from app.models import BlogPost, BlogCategory, BlogTag
    
    # Get tag
    tag_obj = BlogTag.query.filter_by(slug=tag).first_or_404()
    
    # Get posts with tag (pagination)
    posts_per_page = 6
    posts = BlogPost.query.join(BlogPost.tags).filter(
        BlogTag.id == tag_obj.id,
        BlogPost.published == True
    ).order_by(
        BlogPost.created_at.desc()
    ).paginate(
        page=page,
        per_page=posts_per_page,
        error_out=False
    )
    
    # Get categories with post count
    categories = db.session.query(
        BlogCategory, 
        db.func.count(BlogPost.id).label('count')
    ).outerjoin(BlogPost).filter(
        (BlogPost.published == True) | (BlogPost.id == None)
    ).group_by(BlogCategory.id).all()
    
    # Format categories for template
    formatted_categories = [
        {'name': c.BlogCategory.name, 'slug': c.BlogCategory.slug, 'count': c.count} 
        for c in categories
    ]
    
    # Get popular tags
    tags = db.session.query(
        BlogTag, 
        db.func.count(BlogPost.id).label('count')
    ).join(BlogTag.posts).filter(
        BlogPost.published == True
    ).group_by(BlogTag.id).order_by(
        db.func.count(BlogPost.id).desc()
    ).limit(15).all()
    
    # Format tags for template
    formatted_tags = [
        {'name': t.BlogTag.name, 'slug': t.BlogTag.slug, 'count': t.count} 
        for t in tags
    ]
    
    # Get recent posts
    recent_posts = BlogPost.query.filter_by(
        published=True
    ).order_by(
        BlogPost.created_at.desc()
    ).limit(5).all()
    
    return render_template(
        'blog_tag.html',
        tag=tag_obj.name,
        posts=posts.items,
        pagination=posts,
        categories=formatted_categories,
        tags=formatted_tags,
        recent_posts=recent_posts
    )

@pages_bp.route('/blog/search')
def blog_search():
    from app.models import BlogPost, BlogCategory, BlogTag
    from sqlalchemy import or_
    
    # Get search query
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('pages.blog'))
    
    # Get page number
    page = request.args.get('page', 1, type=int)
    
    # Search for posts
    posts_per_page = 6
    search_query = f"%{query}%"
    posts = BlogPost.query.filter(
        BlogPost.published == True,
        or_(
            BlogPost.title.ilike(search_query),
            BlogPost.content.ilike(search_query),
            BlogPost.excerpt.ilike(search_query)
        )
    ).order_by(
        BlogPost.created_at.desc()
    ).paginate(
        page=page,
        per_page=posts_per_page,
        error_out=False
    )
    
    # Process posts to highlight search terms
    for post in posts.items:
        # Create search excerpt with highlighted terms
        if query.lower() in post.excerpt.lower():
            # Simple highlight for demonstration
            # In production, use a more sophisticated approach
            excerpt = post.excerpt
            start_pos = excerpt.lower().find(query.lower())
            end_pos = start_pos + len(query)
            
            # Create excerpt with surrounding context
            start_context = max(0, start_pos - 50)
            end_context = min(len(excerpt), end_pos + 50)
            
            excerpt = excerpt[start_context:end_context]
            
            # Add ellipsis if excerpt doesn't start/end at the original text boundaries
            if start_context > 0:
                excerpt = '...' + excerpt
            if end_context < len(post.excerpt):
                excerpt = excerpt + '...'
            
            # Highlight the search term
            highlighted = excerpt.replace(
                query, 
                f'<em>{query}</em>', 
                1
            )
            post.search_excerpt = highlighted
        else:
            post.search_excerpt = post.excerpt[:150] + '...'
    
    # Get categories with post count
    categories = db.session.query(
        BlogCategory, 
        db.func.count(BlogPost.id).label('count')
    ).outerjoin(BlogPost).filter(
        (BlogPost.published == True) | (BlogPost.id == None)
    ).group_by(BlogCategory.id).all()
    
    # Format categories for template
    formatted_categories = [
        {'name': c.BlogCategory.name, 'slug': c.BlogCategory.slug, 'count': c.count} 
        for c in categories
    ]
    
    # Get popular tags
    tags = db.session.query(
        BlogTag, 
        db.func.count(BlogPost.id).label('count')
    ).join(BlogTag.posts).filter(
        BlogPost.published == True
    ).group_by(BlogTag.id).order_by(
        db.func.count(BlogPost.id).desc()
    ).limit(15).all()
    
    # Format tags for template
    formatted_tags = [
        {'name': t.BlogTag.name, 'slug': t.BlogTag.slug, 'count': t.count} 
        for t in tags
    ]
    
    # Get recent posts
    recent_posts = BlogPost.query.filter_by(
        published=True
    ).order_by(
        BlogPost.created_at.desc()
    ).limit(5).all()
    
    return render_template(
        'blog_search.html',
        query=query,
        posts=posts.items,
        pagination=posts,
        categories=formatted_categories,
        tags=formatted_tags,
        recent_posts=recent_posts
    )
