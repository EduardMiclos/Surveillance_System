# Third party imports
from flask import render_template, make_response, flash, redirect
from flask_login import login_required, current_user
import phonenumbers


from .ProfileInterface import ProfileInterface
from ...forms import ChangePersonalInfoForm
from .....database import db
from .....database.models import User

class Profile(ProfileInterface):
    base_route = ProfileInterface.base_route
    
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        return make_response(
            render_template('profile.html'), 
            200, headers
        )
        
    @login_required
    def post(self):
        headers = {'Content-Type': 'text/html'}
        
        change_personal_info_form = ChangePersonalInfoForm()
        
        if change_personal_info_form.validate_on_submit():            
            user = User.query.filter_by(id = current_user.id).first()
            
            firstname = change_personal_info_form.data.firstname
            secondname = change_personal_info_form.data.secondname
            phone = change_personal_info_form.data.phone
            
            phone_number = phonenumbers.parse(phone)
            
            if not phonenumbers.is_possible_number(phone_number):
                flash('Numărul de telefon introdus nu se află în formatul corect!', 'error')
                return redirect('/profile')
            
            user.firstname = firstname
            user.secondname = secondname
            user.phone = phone
            
            db.session.add(user)
            db.session.commit()
            
            flash('Datele au fost actualizate cu succes!')
            return redirect('/profile')
                
        return make_response(
            render_template('profile.html',
                            form = change_personal_info_form), 
            200, headers
        )