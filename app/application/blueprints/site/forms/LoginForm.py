from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, ValidationError

from ....database.models import *

class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email(), Length(min=4, max=255)], render_kw={"placeholder": "Introduceți adresa de email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Introduceți parola"})
    
    submit = SubmitField("Autentificare")
     