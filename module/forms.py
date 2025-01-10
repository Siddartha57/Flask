from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField, PasswordField, DateField
from wtforms.validators import EqualTo, DataRequired, Length, ValidationError, Email, InputRequired
from module.models import User

class Register(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('user already exits')
    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('email already exists')

    def validate_phone(self, phone_to_check):
        phone = User.query.filter_by(phone=phone_to_check.data).first()
        if phone:
            raise ValidationError('phone numbers already exists')


    username = StringField(validators=[DataRequired(), Length(min=6)])
    email_address = EmailField(validators=[DataRequired(), Email()])
    phone = StringField(validators=[DataRequired(), Length(min=10)])
    password1 = PasswordField(validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField()


class Login(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=6)])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])
    submit = SubmitField()

class Booking(FlaskForm):
    From = StringField(label='Source', validators=[DataRequired()])
    To = StringField(label='Destination',validators=[DataRequired()])
    Date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField()