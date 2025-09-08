import click
from flask.cli import with_appcontext
from app import db
from app.models import BlogCategory

@click.command('update-category')
@with_appcontext
def update_category_command():
    """Update category from 'Технологии' to 'Technology'."""
    # Find "Технологии" category if it exists
    tech_category = BlogCategory.query.filter_by(name="Технологии").first()
    if tech_category:
        click.echo(f"Found category: {tech_category.name} (ID: {tech_category.id})")
        
        # Update to English and fix the slug
        tech_category.name = "Technology"
        tech_category.slug = "technology"
        tech_category.description = "Articles about technology and innovations"
        db.session.commit()
        click.echo(f"Updated category to: {tech_category.name}")
    else:
        # Look for any existing Technology category
        tech_category = BlogCategory.query.filter_by(slug="technology").first()
        if tech_category:
            click.echo(f"Technology category already exists with name: {tech_category.name}")
        else:
            click.echo("No 'Технологии' or 'Technology' category found")
    
    # List all categories for verification
    categories = BlogCategory.query.all()
    click.echo("\nAll categories in database:")
    for category in categories:
        click.echo(f"- {category.name} (slug: {category.slug})")
