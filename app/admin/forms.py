from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

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
