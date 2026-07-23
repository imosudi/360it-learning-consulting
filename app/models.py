from datetime import datetime
from .extensions import db

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    icon = db.Column(db.String(100), default='fa-laptop-code')
    short_desc = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text)
    features_list = db.Column(db.Text) # Comma or newline separated
    category = db.Column(db.String(100), default='Consulting')

class TrainingCourse(db.Model):
    __tablename__ = 'training_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    icon = db.Column(db.String(100), default='fa-graduation-cap')
    image = db.Column(db.String(255))
    short_desc = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text)
    duration = db.Column(db.String(50), nullable=False) # e.g. "8 Weeks"
    delivery_mode = db.Column(db.String(100), nullable=False) # "Online, Onsite, Hybrid"
    skill_level = db.Column(db.String(50), nullable=False) # "Beginner to Advanced"
    syllabus_list = db.Column(db.Text) # Comma or pipe separated topics
    featured = db.Column(db.Boolean, default=True)

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    tech_stack = db.Column(db.String(255), nullable=False) # e.g. "AWS, Docker, Terraform"
    short_desc = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text)
    image = db.Column(db.String(255))
    category = db.Column(db.String(100), default='Cloud Migration')
    featured = db.Column(db.Boolean, default=True)

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    organization = db.Column(db.String(150), nullable=False)
    service_type = db.Column(db.String(50), nullable=False) # "Consulting" or "Training"
    quote = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(255))
    rating = db.Column(db.Integer, default=5)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ConsultationRequest(db.Model):
    __tablename__ = 'consultation_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    organization = db.Column(db.String(150))
    service_interest = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EnrollmentRequest(db.Model):
    __tablename__ = 'enrollment_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    course_title = db.Column(db.String(150), nullable=False)
    delivery_mode = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
