from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from Application.models import Official, Election, Candidates

class Officials_Registration(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,20}$', message='Your password needs to be longer than 6 characters')])
    confirm_password = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    invite_code = PasswordField('Admin Secret Code', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        mail = Official.query.filter_by(Email=email.data).first()
        if mail:
            raise ValidationError('This email is already being used.')

    def validate_invite_code(self, invite_code):
        expected_code = os.environ.get('ADMIN_INVITE_CODE', '123gpa444')
        if invite_code.data != expected_code:
            raise ValidationError('Invalid Admin Secret Code. Registration denied.')

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class CreateElectionForm(FlaskForm):
    title = StringField('Title of the Eleciton', validators=[DataRequired()])
    election_date = DateField('What Date will the election take place? (YYYY-MM-DD)',  format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('What time does polling start?', validators=[DataRequired()])
    end_time = TimeField('What time does polling end?', validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def validate_title(self, title):
        election_title = Election.query.filter_by(title=title.data).first()
        if election_title:
            raise ValidationError('This title is already in use')
