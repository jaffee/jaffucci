from flask_wtf import Form
from wtforms import (TextField, RadioField, SelectField, SelectMultipleField,
                     IntegerField, PasswordField)
from wtforms.validators import Required, EqualTo, NumberRange, Email, Optional




class LoginForm(Form):
    user_id = TextField('userid',
                        validators=[Required()])
    password = PasswordField('password',
                             validators=[Required(message="Password Required")])
