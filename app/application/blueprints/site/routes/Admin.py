# Third party imports
from flask import render_template, make_response
from password_generator import PasswordGenerator


# Local application imports
from .ViewerInterface import ViewerInterface
from ..forms import RegisterForm

from ....database import db
from ....database.models import User

class Admin(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/admin'
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        register_form = RegisterForm()
        users = User.query.all()
        
        return make_response(
            render_template('admin.html', 
                            form = register_form,
                            added_new_user = False,
                            users = users), 
            200, headers
            )
        
        
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
            
            users = User.query.all()
            return make_response(
                render_template('admin.html', 
                                form = register_form, 
                                added_new_user = True,
                                pwd = pwd,
                                users = users),
                200, headers
            )
        else:
            register_form.process()
            
            users = User.query.all()
            return make_response(
                render_template('admin.html', 
                                form = register_form,
                                added_new_user = False,
                                users = users), 
                200, headers
            )
            