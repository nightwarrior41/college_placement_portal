from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class Student(db.Model, UserMixin):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20))
    cgpa = db.Column(db.Float)
    branch = db.Column(db.String(100))
    passing_year = db.Column(db.Integer)
    skills = db.Column(db.Text)
    resume = db.Column(db.String(200))
    is_blacklisted = db.Column(db.Boolean, default=False)
    applications = db.relationship('Application', backref='student', lazy=True)

    # Bug 3 Fix: prefix get_id() so Student id=1 != Company id=1 != Admin id=1
    def get_id(self):
        return f"student-{self.id}"


class Company(db.Model, UserMixin):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)

    def get_id(self):
        return f"company-{self.id}"


class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    role_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    ctc = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    applications = db.relationship('Application', backref='drive', lazy=True)


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    status = db.Column(db.String(50), default="Applied")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return f"admin-{self.id}"


from app.extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    # Bug 3 Fix: parse the prefixed ID to route to the correct model
    try:
        role, uid = user_id.split('-', 1)
        uid = int(uid)
    except (ValueError, AttributeError):
        return None

    if role == 'student':
        return db.session.get(Student, uid)
    elif role == 'company':
        return db.session.get(Company, uid)
    elif role == 'admin':
        return db.session.get(Admin, uid)
    return None
