from flask import redirect, session
from flask_login import login_required
from password_generator import PasswordGenerator

from ..AdminInterface import AdminInterface, admin_required
from ......database import db
from ....forms import RegisterForm
from ......database.models import User

class AddUser(AdminInterface):
    base_route = f'{AdminInterface.base_route}/user/add'
    
    @login_required
    @admin_required
    def post(self):
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