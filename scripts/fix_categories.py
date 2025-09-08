import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set SQLite mode
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models import BlogCategory

def fix_categories():
    """Fix category names in the database."""
    app = create_app()
    with app.app_context():
        # Find "Технологии" category if it exists
        tech_category = BlogCategory.query.filter_by(name="Технологии").first()
        if tech_category:
            print(f"Found category: {tech_category.name} (ID: {tech_category.id})")
            
            # Update to English and fix the slug
            tech_category.name = "Technology"
            tech_category.slug = "technology"
            tech_category.description = "Articles about technology and innovations"
            db.session.commit()
            print(f"Updated category to: {tech_category.name}")
        else:
            # Create Technology category if it doesn't exist
            tech_category = BlogCategory.query.filter_by(slug="technology").first()
            if not tech_category:
                tech_category = BlogCategory(
                    name="Technology", 
                    slug="technology",
                    description="Articles about technology and innovations"
                )
                db.session.add(tech_category)
                db.session.commit()
                print(f"Created new Technology category with ID: {tech_category.id}")
            else:
                print(f"Technology category already exists with name: {tech_category.name}")
        
        # Check for German translation via other model connections if needed
        # (This would require additional code if we store translations in models)
        
        # List all categories for verification
        categories = BlogCategory.query.all()
        print("\nAll categories in database:")
        for category in categories:
            print(f"- {category.name} (slug: {category.slug})")

if __name__ == "__main__":
    fix_categories()
