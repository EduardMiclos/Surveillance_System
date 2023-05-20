from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email

from ..database.models import *

class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email(), Length(min=4, max=255)], render_kw={"placeholder": "Email"})
    firstname = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Nume"})
    secondname = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Prenume"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Parola"})
    
    submit = SubmitField("Înregistrează")
    
    def validate_email(self, email):
        existing_email = User.query.filter_by(email = email.data).first()
        
        if existing_email:
            raise ValidationError("Email-ul introdus există deja.")
     