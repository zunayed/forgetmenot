from flask_wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, ValidationError
from models import db, User


class SignupForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter a valid email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password."), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.checkPassword(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False
