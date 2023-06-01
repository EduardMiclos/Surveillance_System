from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

from ....database.models import *

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], 
                                        render_kw={
                                            "placeholder": "Introduceți vechea parolă",
                                            "id": "old_pwd"
                                            })
    new_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], 
                                         render_kw={
                                             "placeholder": "Introduceți noua parolă",
                                             "id": "new_pwd"
                                            })
    
    repeat_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], 
                                         render_kw={
                                             "placeholder": "Rescrieți noua parolă",
                                             "id": "repeat_new_pwd"
                                            })
    submit = SubmitField("Salvează")
     