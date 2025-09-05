"""
Script to link questionnaire submissions to projects
Run this periodically or use as a background job
"""

from app import db, create_app
from app.models import Lead, User, Project
import json
from datetime import datetime

def link_questionnaire_to_projects():
    """
    Process questionnaire submissions and convert them to projects
    """
    app = create_app()
    
    with app.app_context():
        # Find leads with questionnaire data that haven't been processed yet
        leads = Lead.query.filter(
            Lead.data.isnot(None),  # Has questionnaire data
            Lead.status == 'new'     # Not processed yet
        ).all()
        
        for lead in leads:
            # Try to find an existing user with this email
            user = User.query.filter_by(email=lead.email).first()
            
            if not user:
                # Create a new user account with a temporary password
                user = User(
                    email=lead.email,
                    name=lead.name,
                    phone=lead.phone,
                    company=lead.company
                )
                user.set_password('temporary')  # They'll need to use password reset
                db.session.add(user)
                
                # Save to get the user ID
                db.session.flush()
            
            # Parse the questionnaire data
            try:
                questionnaire_data = json.loads(lead.data)
                
                # Extract project details from questionnaire
                project_title = questionnaire_data.get('project_name', 'New Project')
                project_description = questionnaire_data.get('project_description', '')
                
                # Create a new project for the user
                project = Project(
                    title=project_title,
                    description=project_description,
                    status='new',
                    client_id=user.id,
                    created_at=datetime.utcnow()
                )
                db.session.add(project)
                
                # Update lead status
                lead.status = 'converted'
                
                # Commit changes
                db.session.commit()
                
                print(f"Created project '{project_title}' for user {user.email}")
                
            except Exception as e:
                db.session.rollback()
                print(f"Error processing lead {lead.id}: {str(e)}")
    
    print("Questionnaire to project linking complete")

if __name__ == "__main__":
    link_questionnaire_to_projects()
