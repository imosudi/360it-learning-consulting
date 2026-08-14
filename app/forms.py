from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Optional, Length

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=30)])
    subject_choice = SelectField('Department / Subject', choices=[
        ('consulting', 'IT Consulting Services'),
        ('training', 'Professional Training Programs'),
        ('projects', 'Projects & Contracts'),
        ('general', 'General Enquiry')
    ], validators=[DataRequired()])
    subject = StringField('Subject Line', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Your Message', validators=[DataRequired(), Length(min=10)])
    privacy_consent = BooleanField('I consent to the processing of my personal data in accordance with the Privacy Policy.', validators=[DataRequired(message='You must accept the Privacy Policy to submit.')])
    submit = SubmitField('Send Message')

class ConsultationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Business Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=30)])
    organization = StringField('Company / Organization', validators=[Optional(), Length(max=150)])
    service_interest = SelectField('Primary Service of Interest', choices=[
        ('Cloud Consulting', 'Cloud Consulting'),
        ('DevOps Consulting', 'DevOps Consulting'),
        ('Infrastructure Solutions', 'Infrastructure Solutions'),
        ('ERP Implementation & Support', 'ERP Implementation & Support'),
        ('CRM Solutions & Integration', 'CRM Solutions & Integration'),
        ('Lean Six Sigma & IT Process Optimization', 'Lean Six Sigma & IT Process Optimization'),
        ('Digital Transformation', 'Digital Transformation'),
        ('Systems Administration', 'Systems Administration'),
        ('Application Deployment', 'Application Deployment'),
        ('Database Administration', 'Database Administration'),
        ('Managed IT Services', 'Managed IT Services'),
        ('IT Support', 'IT Support'),
        ('Technology Advisory', 'Technology Advisory')
    ], validators=[DataRequired()])
    message = TextAreaField('Project / Consultation Details', validators=[Optional()])
    privacy_consent = BooleanField('I consent to the processing of my personal data in accordance with the Privacy Policy.', validators=[DataRequired(message='You must accept the Privacy Policy to submit.')])
    submit = SubmitField('Request Consultation')

class EnrollmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=30)])
    course_title = SelectField('Training Course', choices=[
        ('AWS Cloud Engineering', 'AWS Cloud Engineering'),
        ('Microsoft Azure', 'Microsoft Azure'),
        ('DevOps Engineering', 'DevOps Engineering'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Software Development', 'Software Development'),
        ('Data Analytics', 'Data Analytics'),
        ('Linux Administration', 'Linux Administration'),
        ('Docker & Kubernetes', 'Docker & Kubernetes'),
        ('IT Support Fundamentals', 'IT Support Fundamentals'),
        ('Corporate Technology Training', 'Corporate Technology Training')
    ], validators=[DataRequired()])
    delivery_mode = SelectField('Preferred Delivery Mode', choices=[
        ('Online Live Interactive', 'Online Live Interactive'),
        ('Onsite Corporate Training', 'Onsite Corporate Training'),
        ('Hybrid', 'Hybrid')
    ], validators=[DataRequired()])
    message = TextAreaField('Additional Notes / Questions', validators=[Optional()])
    privacy_consent = BooleanField('I consent to the processing of my personal data in accordance with the Privacy Policy.', validators=[DataRequired(message='You must accept the Privacy Policy to submit.')])
    submit = SubmitField('Submit Enrollment')
