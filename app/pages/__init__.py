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
    return jsonify({"status": "ok", "service": "andrii-it"}), 200

@pages_bp.route('/services')
def services():
    return render_template('services.html')


@pages_bp.route('/lebenslauf')
def lebenslauf():
    """Public CV / Lebenslauf page."""
    from app.models.cv import (
        CVProfile, CVExperience, CVEducation, CVSkill,
        CVProject, CVSocialLink, CVLanguage, CVCertification
    )
    profile = CVProfile.query.first()
    experiences = CVExperience.query.order_by(CVExperience.order_idx, CVExperience.created_at.desc()).all()
    educations = CVEducation.query.order_by(CVEducation.order_idx, CVEducation.created_at.desc()).all()
    skills = CVSkill.query.order_by(CVSkill.category, CVSkill.order_idx).all()
    projects = CVProject.query.order_by(CVProject.order_idx, CVProject.created_at.desc()).all()
    social_links = CVSocialLink.query.order_by(CVSocialLink.order_idx).all()
    languages = CVLanguage.query.order_by(CVLanguage.order_idx).all()
    certifications = CVCertification.query.order_by(CVCertification.order_idx).all()

    # Group skills by category
    skills_by_cat = {}
    for s in skills:
        cat = s.category or 'Sonstige'
        skills_by_cat.setdefault(cat, []).append(s)

    return render_template(
        'cv.html',
        profile=profile,
        experiences=experiences,
        educations=educations,
        skills_by_cat=skills_by_cat,
        projects=projects,
        social_links=social_links,
        languages=languages,
        certifications=certifications,
    )



@pages_bp.route('/submit-questionnaire', methods=['POST'])
def submit_questionnaire():
    """Handle project questionnaire submissions (ALL 15 fields)."""
    try:
        from app.services.telegram_service import send_tech_spec_notification
        from app.utils.telegram_queue import send_telegram_message_with_retry
        from datetime import datetime
        import json
        from app.models.base import Lead
        from app import db

        # 1) РЎРёСЂС– РґР°РЅС– С„РѕСЂРјРё
        form_data = request.form.to_dict(flat=True)

        # РњР°СЃРёРІРё (С‡РµРєР±РѕРєСЃРё/РјСѓР»СЊС‚РёРІРёР±С–СЂ)
        security_requirements = request.form.getlist('security_requirements')
        existing_assets = request.form.getlist('existing_assets[]')

        # 2) РџС–РґРіРѕС‚РѕРІРєР° В«РІС–РґРїРѕРІС–РґРµР№В» вЂ” РґРѕРґР°С”РјРѕ РЈРЎР† 15 РїРѕР»С–РІ
        answers = []

        # 1
        answers.append({
            'question': 'Project Type',
            'answer': form_data.get('project_type', 'Not specified')
        })
        # 2
        answers.append({
            'question': 'Main Goal',
            'answer': form_data.get('project_goal', 'Not specified')
        })
        # 3
        answers.append({
            'question': 'Target Users',
            'answer': form_data.get('target_users', 'Not specified')
        })
        # 4
        answers.append({
            'question': 'Essential Features',
            'answer': form_data.get('essential_features', 'Not specified')
        })
        # 5
        answers.append({
            'question': 'Nice-to-have Features',
            'answer': form_data.get('nice_to_have_features', 'Not specified')
        })
        # 6
        answers.append({
            'question': 'Timeline',
            'answer': form_data.get('timeline', 'Not specified')
        })
        # 7
        answers.append({
            'question': 'Budget Range',
            'answer': form_data.get('budget_range', 'Not specified')
        })
        # 8
        answers.append({
            'question': 'Integrations (existing systems to integrate)',
            'answer': form_data.get('integrations', 'Not specified')
        })
        # 9
        answers.append({
            'question': 'Technical Requirements / Preferences',
            'answer': form_data.get('technical_requirements', 'Not specified')
        })
        # 10
        answers.append({
            'question': 'Similar Projects (examples/inspiration)',
            'answer': form_data.get('similar_projects', 'Not specified')
        })
        # 11
        answers.append({
            'question': 'Success Metrics (KPIs)',
            'answer': form_data.get('success_metrics', 'Not specified')
        })
        # 12
        sr = ', '.join(security_requirements) if security_requirements else 'Not specified'
        if form_data.get('other_security_requirements'):
            sr = (sr + '; Other: ' + form_data['other_security_requirements']).strip('; ')
        answers.append({
            'question': 'Security / Compliance Requirements',
            'answer': sr
        })
        # 13
        answers.append({
            'question': 'Required Ongoing Support After Launch',
            'answer': form_data.get('support_level', 'Not specified')
        })
        # 14
        assets = ', '.join(existing_assets) if existing_assets else 'None'
        answers.append({
            'question': 'Existing Design Assets / Docs',
            'answer': assets
        })
        # 15
        answers.append({
            'question': 'Additional Info',
            'answer': form_data.get('additional_info', 'Not provided')
        })

        tech_spec_data = {
            'answers': answers,
            # РњРѕР¶РµС€ Р·Р±РµСЂС–РіР°С‚Рё РјРѕРІСѓ, СЏРєС‰Рѕ С‚СЂРµР±Р°
            'language': 'en'
        }

        # РљРѕРЅС‚Р°РєС‚Рё Р·Р°РјРѕРІРЅРёРєР°
        contact_info = {
            'name': form_data.get('contact_name', 'Not provided'),
            'email': form_data.get('contact_email', 'Not provided'),
            'phone': form_data.get('contact_phone', 'Not provided'),
            'company': form_data.get('company_name', '')
        }

        # 3) РќР°РґСЃРёР»Р°РЅРЅСЏ Сѓ Telegram Р· Р±РµР·РїРµС‡РЅРёРј СЂРѕР·Р±РёС‚С‚СЏРј
        #    (РІСЂР°С…РѕРІСѓС” Р»С–РјС–С‚ 4096 СЃРёРјРІРѕР»С–РІ)
        full_message = send_tech_spec_notification(
            tech_spec_data,
            contact_info=contact_info,
            return_message_only=True  # РћС‚СЂРёРјСѓС”РјРѕ С‚РµРєСЃС‚ Р±РµР· РІС–РґРїСЂР°РІРєРё
        )

        def _send_long_message_in_chunks(msg: str, chunk_size: int = 3500):
            # Р РѕР·Р±РёРІР°С”РјРѕ Р·Р° РїСѓСЃС‚РёРјРё СЂСЏРґРєР°РјРё, РїРѕС‚С–Рј СЃР»С–РїР°С”РјРѕ РєСѓСЃРєРё, С‰РѕР± РЅРµ СЂРІР°С‚Рё СЃР»РѕРІР°
            import textwrap
            parts = []
            buf = ""
            for para in msg.split("\n\n"):
                if len(buf) + len(para) + 2 <= chunk_size:
                    buf = (buf + "\n\n" + para) if buf else para
                else:
                    if buf:
                        parts.append(buf)
                    # СЏРєС‰Рѕ Р°Р±Р·Р°С† РґСѓР¶Рµ РґРѕРІРіРёР№ вЂ” РЅР°СЂС–Р·Р°С”РјРѕ
                    if len(para) > chunk_size:
                        for sub in textwrap.wrap(para, chunk_size):
                            parts.append(sub)
                        buf = ""
                    else:
                        buf = para
            if buf:
                parts.append(buf)

            sent_ok = True
            for part in parts:
                if not send_telegram_message_with_retry(part):
                    sent_ok = False
            return sent_ok

        sent = _send_long_message_in_chunks(full_message)

        if not sent:
            current_app.logger.warning("Failed to send full tech spec to Telegram (queued or partially sent).")

        # 4) РЎРѕС…СЂР°РЅСЏРµРј РґР°РЅРЅС‹Рµ С„РѕСЂРјС‹ РІ Р±Р°Р·Сѓ РґР°РЅРЅС‹С…
        try:
            from app.models.tech_spec_submission import TechSpecSubmission
            
            # РЎРѕР±РёСЂР°РµРј security_requirements РІ СЃС‚СЂРѕРєСѓ
            security_reqs = ', '.join(security_requirements) if security_requirements else ''
            if form_data.get('other_security_requirements'):
                security_reqs = (security_reqs + '; Other: ' + form_data['other_security_requirements']).strip('; ')
            
            # РЎРѕР·РґР°РµРј Р·Р°РїРёСЃСЊ РўР—
            tech_spec = TechSpecSubmission(
                project_type=form_data.get('project_type'),
                project_goal=form_data.get('project_goal'),
                target_users=form_data.get('target_users'),
                essential_features=form_data.get('essential_features'),
                nice_to_have_features=form_data.get('nice_to_have_features'),
                timeline=form_data.get('timeline'),
                budget_range=form_data.get('budget_range'),
                integrations=form_data.get('integrations'),
                technical_requirements=form_data.get('technical_requirements'),
                similar_projects=form_data.get('similar_projects'),
                success_metrics=form_data.get('success_metrics'),
                security_requirements=security_reqs,
                support_level=form_data.get('support_level'),
                existing_assets=','.join(existing_assets) if existing_assets else '',
                additional_info=form_data.get('additional_info'),
                
                # РљРѕРЅС‚Р°РєС‚РЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ
                contact_name=form_data.get('contact_name'),
                contact_email=form_data.get('contact_email'),
                company_name=form_data.get('company_name'),
                contact_phone=form_data.get('contact_phone')
            )
            
            # Р•СЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ Р°РІС‚РѕСЂРёР·РѕРІР°РЅ, СЃРІСЏР·С‹РІР°РµРј РўР— СЃ РЅРёРј
            from flask_login import current_user
            if current_user and current_user.is_authenticated:
                tech_spec.client_id = current_user.id
            
            db.session.add(tech_spec)
            db.session.commit()
            
            # РўР°РєР¶Рµ СЃРѕС…СЂР°РЅСЏРµРј Р»РёРґ РґР»СЏ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё СЃ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРј РєРѕРґРѕРј
            lead = Lead(
                name=contact_info['name'],
                email=contact_info['email'],
                phone=contact_info['phone'],
                company=form_data.get('company_name'),
                message='Tech spec submission',
                data=json.dumps({'questionnaire': form_data}, ensure_ascii=False),
                source='services_form',
                created_at=datetime.utcnow()
            )
            db.session.add(lead)
            db.session.commit()
            
            current_app.logger.info(f"Tech spec saved to database with ID {tech_spec.id}")
        except Exception as db_err:
            current_app.logger.error(f"Tech spec save failed: {db_err}")

        flash('Your request has been submitted successfully. We will contact you soon.', 'success')
        return redirect(url_for('pages.services'))

    except Exception as e:
        current_app.logger.exception(f"Questionnaire submit error: {e}")
        flash('Something went wrong while submitting the form. Please try again later.', 'danger')
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
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@andrii-it.com')
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
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@andrii-it.com')
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
    # Delegate to the unified blog blueprint to avoid locale mix between EN/DE posts.
    params = dict(request.args)
    if page and page != 1:
        params['page'] = page
    return redirect(url_for('blog.index', **params), code=302)

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
    elif g.locale == 'uk':
        return render_template('uk/impressum.html')
    else:
        return render_template('impressum.html')

@pages_bp.route('/privacy')
def privacy():
    # Check current language and use appropriate template
    from flask import g
    if g.locale == 'de':
        return render_template('de/privacy.html')
    elif g.locale == 'uk':
        return render_template('uk/privacy.html')
    else:
        return render_template('privacy.html')

@pages_bp.route('/terms')
def terms():
    # Check current language and use appropriate template
    from flask import g
    if g.locale == 'de':
        return render_template('de/terms.html')
    elif g.locale == 'uk':
        return render_template('uk/terms.html')
    else:
        return render_template('terms.html')

@pages_bp.route('/blog/<slug>')
def blog_post(slug):
    params = dict(request.args)
    return redirect(url_for('blog.post', slug=slug, **params), code=302)

@pages_bp.route('/blog/category/<category>')
@pages_bp.route('/blog/category/<category>/page/<int:page>')
def blog_category(category, page=1):
    params = dict(request.args)
    if page and page != 1:
        params['page'] = page
    return redirect(url_for('blog.category', slug=category, **params), code=302)

@pages_bp.route('/blog/tag/<tag>')
@pages_bp.route('/blog/tag/<tag>/page/<int:page>')
def blog_tag(tag, page=1):
    params = dict(request.args)
    if page and page != 1:
        params['page'] = page
    return redirect(url_for('blog.tag', slug=tag, **params), code=302)

@pages_bp.route('/blog/search')
def blog_search():
    params = dict(request.args)
    return redirect(url_for('blog.search', **params), code=302)


