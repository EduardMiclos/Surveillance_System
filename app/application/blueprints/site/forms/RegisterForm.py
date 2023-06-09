from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email

from ....database.models import *

class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email(), 
                                   Length(min=4, max=255)], 
                                   render_kw={
                                       "placeholder": "Introduceți adresa de email",
                                       "id": "email"
                                       })
    firstname = StringField(validators=[InputRequired(), Length(min=2, max=50)], 
                                        render_kw={
                                            "placeholder": "Introduceți numele",
                                            "id": "firstname"
                                            })
    secondname = StringField(validators=[InputRequired(), Length(min=2, max=50)], 
                                         render_kw={
                                             "placeholder": "Introduceți prenumele",
                                             "id": "secondname"
                                            })
    phone = StringField(validators=[InputRequired(), Length(min=5, max=15)], 
                                    render_kw={"placeholder": "Introduceți numărul de telefon",
                                                "id": "phone"
                                            })
    
    is_admin = BooleanField(render_kw = {"id": "is_admin"})
    submit = SubmitField("Înregistrează")
    
    def validate_email(self, email):
        existing_email = User.query.filter_by(email = email.data).first()
        
        if existing_email:
            raise ValidationError("Email-ul introdus există deja.")
     