from flask import render_template, make_response, redirect, session
from password_generator import PasswordGenerator

from .AdminInterface import AdminInterface
from ....database import db
from ..forms import RegisterForm
from ....database.models import User

class AddUser(AdminInterface):
    base_route = f'{AdminInterface.base_route}/add-user'
    
    def post(self):
        headers = {'Content-Type': 'text/html'}
        register_form = RegisterForm()
    
        
        if register_form.validate_on_submit():
            password_generator = PasswordGenerator()
            password_generator.minlen = 10
            password_generator.maxlen = 10
            
            new_user = User(email = register_form.email.data,
                        firstname = register_form.firstname.data,
                        secondname = register_form.secondname.data,
                        phone = register_form.phone.data,
                        is_admin = register_form.is_admin.data)
            
            pwd = password_generator.generate()
            new_user.set_password(pwd)
            
            db.session.add(new_user)
            db.session.commit()
        
            register_form.process()

            session['added_new_user'] = True
            session['pwd'] = pwd
            return redirect('/admin')
        else:
            register_form.process()
    
            session['added_new_user'] = False
            return redirect('/admin')