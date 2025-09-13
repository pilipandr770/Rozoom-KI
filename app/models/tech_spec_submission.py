from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class TechSpecSubmission(db.Model):
    """Модель для хранения заполненных технических заданий"""
    __tablename__ = 'tech_spec_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    project_type = db.Column(db.String(50))
    project_goal = db.Column(db.Text)
    target_users = db.Column(db.Text)
    essential_features = db.Column(db.Text)
    nice_to_have_features = db.Column(db.Text)
    timeline = db.Column(db.String(50))
    budget_range = db.Column(db.String(50))
    integrations = db.Column(db.Text)
    technical_requirements = db.Column(db.Text)
    similar_projects = db.Column(db.Text)
    success_metrics = db.Column(db.Text)
    security_requirements = db.Column(db.Text, nullable=True)
    support_level = db.Column(db.String(50))
    existing_assets = db.Column(db.Text, nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    
    # Контактная информация
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    company_name = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)
    
    status = db.Column(db.String(50), default='new')  # new, reviewed, estimated, approved, rejected
    estimated_hours = db.Column(db.Float, nullable=True)
    estimated_cost = db.Column(db.Float, nullable=True)
    estimated_timeline = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с проектом (если ТЗ было одобрено и превратилось в проект)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    project = relationship("Project", backref="tech_spec")
    
    # Связь с пользователем (если пользователь авторизован)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    client = relationship("User", backref="tech_specs")
    
    def __repr__(self):
        return f'<TechSpecSubmission {self.id}: {self.project_type}>'
    
    @property
    def as_dict(self):
        """Возвращает данные ТЗ в виде словаря"""
        return {
            'id': self.id,
            'project_type': self.project_type,
            'project_goal': self.project_goal,
            'target_users': self.target_users,
            'essential_features': self.essential_features,
            'nice_to_have_features': self.nice_to_have_features,
            'timeline': self.timeline,
            'budget_range': self.budget_range,
            'integrations': self.integrations,
            'technical_requirements': self.technical_requirements,
            'similar_projects': self.similar_projects,
            'success_metrics': self.success_metrics,
            'security_requirements': self.security_requirements,
            'support_level': self.support_level,
            'existing_assets': self.existing_assets,
            'additional_info': self.additional_info,
            'contact_info': {
                'name': self.contact_name,
                'email': self.contact_email,
                'company': self.company_name,
                'phone': self.contact_phone
            },
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
