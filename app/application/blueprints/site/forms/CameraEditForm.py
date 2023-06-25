from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length

from ....database.models import *

class CameraEditForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=2, max=255)], 
                                        render_kw={
                                            "placeholder": "Introduceți denumirea camerei",
                                            "id": "name"
                                            })
    description = TextAreaField(validators=[InputRequired(), Length(min=2, max=500)], 
                                         render_kw={
                                             "placeholder": "Introduceți descrierea",
                                             "id": "description"
                                            })
    
    preprocess_data = BooleanField(render_kw = {"id": "preprocess_data"})
    submit = SubmitField("Salvează")
     