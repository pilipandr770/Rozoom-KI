"""
CV / Lebenslauf models
All sections editable from the admin panel.
"""
from .. import db
from datetime import datetime


class CVProfile(db.Model):
    """Main profile: personal info shown at the top of the CV."""
    __tablename__ = 'cv_profile'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False, default='')
    headline = db.Column(db.String(300), default='')          # e.g. "Full-Stack Developer"
    email = db.Column(db.String(200), default='')
    phone = db.Column(db.String(80), default='')
    location = db.Column(db.String(200), default='')          # e.g. "Berlin, Germany"
    website = db.Column(db.String(300), default='')
    summary = db.Column(db.Text, default='')                  # professional summary / Profil
    photo_url = db.Column(db.String(500), default='')
    # German-market extras
    date_of_birth = db.Column(db.String(20), default='')      # optional, common in DE CVs
    nationality = db.Column(db.String(100), default='')
    driving_license = db.Column(db.String(100), default='')   # e.g. "Klasse B"
    available_from = db.Column(db.String(100), default='')    # e.g. "ab sofort"
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CVProfile {self.full_name}>'


class CVExperience(db.Model):
    """Work experience entries (Berufserfahrung)."""
    __tablename__ = 'cv_experience'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(300), nullable=False, default='')
    position = db.Column(db.String(300), nullable=False, default='')
    location = db.Column(db.String(200), default='')
    start_year = db.Column(db.String(20), default='')         # e.g. "2020" or "Jan 2020"
    end_year = db.Column(db.String(20), default='')           # blank / "heute" if current
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, default='')              # bullet points as markdown/text
    technologies = db.Column(db.String(500), default='')      # comma-separated tech tags
    order_idx = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CVExperience {self.position} @ {self.company}>'


class CVEducation(db.Model):
    """Education entries (Ausbildung / Studium)."""
    __tablename__ = 'cv_education'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(300), nullable=False, default='')
    degree = db.Column(db.String(200), default='')            # e.g. "Bachelor of Science"
    field = db.Column(db.String(200), default='')             # e.g. "Computer Science"
    location = db.Column(db.String(200), default='')
    start_year = db.Column(db.String(20), default='')
    end_year = db.Column(db.String(20), default='')
    is_current = db.Column(db.Boolean, default=False)
    grade = db.Column(db.String(50), default='')              # e.g. "1,7" or "sehr gut"
    description = db.Column(db.Text, default='')
    order_idx = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CVEducation {self.degree} @ {self.institution}>'


class CVSkill(db.Model):
    """Skill entries grouped by category (Kenntnisse)."""
    __tablename__ = 'cv_skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, default='')
    category = db.Column(db.String(100), default='')          # e.g. "Languages", "Frameworks"
    level = db.Column(db.Integer, default=80)                 # 0–100 for the progress bar
    level_label = db.Column(db.String(50), default='')        # e.g. "Expert", "Grundkenntnisse"
    order_idx = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CVSkill {self.name}>'


class CVProject(db.Model):
    """Portfolio projects (Projekte)."""
    __tablename__ = 'cv_project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, default='')
    description = db.Column(db.Text, default='')
    url = db.Column(db.String(500), default='')               # live demo
    github_url = db.Column(db.String(500), default='')
    image_url = db.Column(db.String(500), default='')
    technologies = db.Column(db.String(500), default='')      # comma-separated
    year = db.Column(db.String(20), default='')
    featured = db.Column(db.Boolean, default=False)
    order_idx = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CVProject {self.title}>'


class CVSocialLink(db.Model):
    """Social / contact links (LinkedIn, GitHub, Xing, etc.)."""
    __tablename__ = 'cv_social_link'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=False, default='')  # e.g. "LinkedIn"
    url = db.Column(db.String(500), nullable=False, default='')
    icon_class = db.Column(db.String(100), default='')                 # FontAwesome class
    display_name = db.Column(db.String(200), default='')               # shown label
    order_idx = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CVSocialLink {self.platform}>'


class CVLanguage(db.Model):
    """Language proficiency (Sprachkenntnisse)."""
    __tablename__ = 'cv_language'

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100), nullable=False, default='')
    level = db.Column(db.String(50), default='')              # e.g. "C1", "Muttersprache", "B2"
    level_percent = db.Column(db.Integer, default=80)         # 0–100 for bar
    order_idx = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CVLanguage {self.language} {self.level}>'


class CVCertification(db.Model):
    """Certifications and courses (Zertifikate / Weiterbildungen)."""
    __tablename__ = 'cv_certification'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, default='')
    issuer = db.Column(db.String(300), default='')
    date = db.Column(db.String(30), default='')               # e.g. "2023" or "April 2023"
    url = db.Column(db.String(500), default='')
    description = db.Column(db.Text, default='')
    order_idx = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CVCertification {self.name}>'
