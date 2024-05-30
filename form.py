from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=150)], render_kw={
        'placeholder': 'Username'
    })
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)], render_kw={
        'placeholder': 'Password'
    })
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')], render_kw={
        'placeholder': 'Confirm Password'
    })
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email is already in use. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
        'placeholder': 'Username'
    })
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
        'placeholder': 'Password'
    })
    submit = SubmitField('Login')


class URLForm(FlaskForm):
    url = URLField('URL', validators=[DataRequired()], render_kw={
        'placeholder': 'URL to shorten'
    })
    submit = SubmitField('Shorten Url')
