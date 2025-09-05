from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Project(db.Model):
    """Project model for client projects"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='new')  # new, in_progress, testing, completed, etc
    start_date = db.Column(db.DateTime)
    estimated_end_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client = relationship("User", back_populates="projects")
    
    # Project has many tasks
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    
    # Project has many updates
    updates = relationship("ProjectUpdate", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    @property
    def progress(self):
        """Calculate project progress based on completed tasks"""
        if not self.tasks:
            return 0
        completed = sum(1 for task in self.tasks if task.status == 'completed')
        return int((completed / len(self.tasks)) * 100)


class ProjectTask(db.Model):
    """Tasks associated with projects"""
    __tablename__ = 'project_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f'<ProjectTask {self.title}>'


class ProjectUpdate(db.Model):
    """Updates or milestones for projects"""
    __tablename__ = 'project_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    is_milestone = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = relationship("Project", back_populates="updates")
    
    def __repr__(self):
        return f'<ProjectUpdate {self.title}>'
