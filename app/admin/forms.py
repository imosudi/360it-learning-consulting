from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

class AdminLoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In to Dashboard')

class StatusUpdateForm(FlaskForm):
    status = SelectField('Status', choices=[], validators=[DataRequired()])
    admin_notes = TextAreaField('Internal Admin Notes', validators=[Optional()])
    submit = SubmitField('Save Changes')

class SendReplyForm(FlaskForm):
    recipient_email = StringField('Recipient Email', validators=[DataRequired(), Email()])
    subject = StringField('Email Subject', validators=[DataRequired()])
    body = TextAreaField('Reply Message', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Send Email Reply')

class CreateAdminUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    role = SelectField('Role Permission', choices=[
        ('Admin', 'Admin (Standard - Full Edit)'),
        ('Readonly Admin', 'Read-Only Admin (View Only)'),
        ('Super Admin', 'Super Admin (Full Edit + User Management)')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Create Admin User')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Update Password')

class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired(), Length(min=3, max=150)])
    icon = StringField('FontAwesome Icon Class (e.g. fa-aws, fa-cubes)', default='fa-graduation-cap', validators=[DataRequired(), Length(max=100)])
    duration = StringField('Duration (e.g. 8 Weeks)', validators=[DataRequired(), Length(max=50)])
    delivery_mode = StringField('Delivery Mode (e.g. Online, Onsite, Hybrid)', validators=[DataRequired(), Length(max=100)])
    skill_level = SelectField('Skill Level', choices=[
        ('Beginner to Advanced', 'Beginner to Advanced'),
        ('Intermediate to Advanced', 'Intermediate to Advanced'),
        ('Advanced Professional', 'Advanced Professional'),
        ('All Levels Welcome', 'All Levels Welcome')
    ], validators=[DataRequired()])
    short_desc = TextAreaField('Short Summary Description', validators=[DataRequired(), Length(min=10)])
    long_desc = TextAreaField('Detailed Course Overview', validators=[Optional()])
    syllabus_list = TextAreaField('Syllabus Topics (Pipe-separated: Topic 1|Topic 2|Topic 3)', validators=[Optional()])
    featured = BooleanField('Featured Course', default=True)
    submit = SubmitField('Save Course')
