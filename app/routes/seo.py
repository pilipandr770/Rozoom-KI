"""SEO routes for robots.txt, sitemap.xml, and ai.txt"""
from flask import Blueprint, send_from_directory, make_response, url_for, current_app
from app.models import BlogPost, BlogCategory
from datetime import datetime
import os

seo_bp = Blueprint('seo', __name__)


@seo_bp.route('/robots.txt')
def robots():
    """Serve robots.txt for search engines and AI crawlers"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'robots.txt',
        mimetype='text/plain'
    )


@seo_bp.route('/ai.txt')
def ai_txt():
    """Serve ai.txt for AI/ML systems"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'ai.txt',
        mimetype='text/plain'
    )


@seo_bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap.xml for search engines"""
    
    # Base URLs with priorities and change frequencies
    static_pages = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': '/services', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/pricing', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/blog', 'priority': '0.8', 'changefreq': 'daily'},
        {'loc': '/about', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': '/contact', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': '/faq', 'priority': '0.6', 'changefreq': 'monthly'},
        {'loc': '/impressum', 'priority': '0.3', 'changefreq': 'yearly'},
        {'loc': '/privacy', 'priority': '0.3', 'changefreq': 'yearly'},
        {'loc': '/terms', 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    
    # Get base URL
    base_url = 'https://andrii-it.de'
    if current_app.config.get('SERVER_NAME'):
        base_url = f"https://{current_app.config['SERVER_NAME']}"
    
    # Start XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    xml += '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    
    # Add static pages
    for page in static_pages:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{page["loc"]}</loc>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        
        # Add language alternates for main pages
        if page['loc'] in ['/', '/services', '/pricing', '/blog', '/about', '/contact', '/faq']:
            xml += f'    <xhtml:link rel="alternate" hreflang="de" href="{base_url}{page["loc"]}?lang=de" />\n'
            xml += f'    <xhtml:link rel="alternate" hreflang="en" href="{base_url}{page["loc"]}?lang=en" />\n'
            xml += f'    <xhtml:link rel="alternate" hreflang="uk" href="{base_url}{page["loc"]}?lang=uk" />\n'
        
        xml += '  </url>\n'
    
    # Add blog posts
    try:
        posts = BlogPost.query.filter_by(published=True).all()
        for post in posts:
            xml += '  <url>\n'
            xml += f'    <loc>{base_url}/blog/{post.slug}</loc>\n'
            if post.updated_at:
                lastmod = post.updated_at.strftime('%Y-%m-%d')
            elif post.created_at:
                lastmod = post.created_at.strftime('%Y-%m-%d')
            else:
                lastmod = datetime.utcnow().strftime('%Y-%m-%d')
            xml += f'    <lastmod>{lastmod}</lastmod>\n'
            xml += '    <changefreq>monthly</changefreq>\n'
            xml += '    <priority>0.7</priority>\n'
            xml += '  </url>\n'
    except Exception as e:
        current_app.logger.warning(f"Could not fetch blog posts for sitemap: {e}")
    
    # Add blog categories
    try:
        categories = BlogCategory.query.all()
        for category in categories:
            xml += '  <url>\n'
            xml += f'    <loc>{base_url}/blog/category/{category.slug}</loc>\n'
            xml += '    <changefreq>weekly</changefreq>\n'
            xml += '    <priority>0.6</priority>\n'
            xml += '  </url>\n'
    except Exception as e:
        current_app.logger.warning(f"Could not fetch blog categories for sitemap: {e}")
    
    xml += '</urlset>'
    
    # Create response
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    response.headers['X-Robots-Tag'] = 'noindex'  # Don't index the sitemap itself
    
    return response


@seo_bp.route('/.well-known/security.txt')
def security_txt():
    """Security contact information for security researchers"""
    
    content = """# Security Contact Information
# Updated: 2025-12-04

Contact: mailto:info@andrii-it.de
Expires: 2026-12-31T23:59:59.000Z
Preferred-Languages: de, en, uk
Canonical: https://andrii-it.de/.well-known/security.txt

# Policy
Policy: https://andrii-it.de/privacy

# Acknowledgments
# We appreciate responsible disclosure of security vulnerabilities

# Hiring
Hiring: https://andrii-it.de/contact
"""
    
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


@seo_bp.route('/humans.txt')
def humans_txt():
    """Humans.txt - credits for the humans behind the website"""
    
    content = """/* TEAM */
Developer: Andrii
Contact: info [at] andrii-it.de
Location: Germany
Languages: German, English, Ukrainian

/* THANKS */
AI Assistants: Claude (Anthropic), GPT-4 (OpenAI)
Icons: Font Awesome
Fonts: Google Fonts
CDN: Cloudflare
Hosting: Render.com

/* SITE */
Last update: 2025-12-04
Standards: HTML5, CSS3, ECMAScript 6+
Components: Flask 3.1, Python 3.13, PostgreSQL
Software: VS Code, Git, GitHub
Security: HTTPS, CSP, HSTS
Languages: Multilingual (DE/EN/UK)
Accessibility: WCAG 2.1 Level AA

/* TECHNOLOGIES */
Backend: Python, Flask, SQLAlchemy
Frontend: HTML5, CSS3, JavaScript, TypeScript
Database: PostgreSQL
AI Integration: OpenAI GPT-4, Anthropic Claude
Payment: Stripe
Analytics: Privacy-focused
Deployment: CI/CD with GitHub Actions

/* FEATURES */
- Multilingual support (German/English/Ukrainian)
- AI-powered chat widget
- Responsive design
- Progressive Web App (PWA) ready
- SEO optimized
- Accessibility compliant
- Security headers implemented
- Fast page load times

/* PHILOSOPHY */
Code quality over quantity
User privacy matters
Accessibility for all
Performance is a feature
Security by design
Open communication
Continuous improvement
"""
    
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response
