from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

from ....database.models import *

class ChangePersonalInfoForm(FlaskForm):
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
    submit = SubmitField("Salvează")
     