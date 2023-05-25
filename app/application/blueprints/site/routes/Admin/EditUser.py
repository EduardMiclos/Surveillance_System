from flask import redirect, session, request
from flask_login import login_required

from .AdminInterface import AdminInterface, admin_required
from .....database import db
from ...forms import UserEditForm
from .....database.models import User

class EditUser(AdminInterface):
    base_route = f'{AdminInterface.base_route}/edit-user'
    
    @login_required
    @admin_required
    def post(self):
        useredit_form = UserEditForm()
        
        if useredit_form.validate_on_submit():
            user_id = request.form.get("user_id")
            
            user = User.query.filter_by(id = user_id).first()
            
            user.firstname = useredit_form.firstname.data
            user.secondname = useredit_form.secondname.data
            user.email = useredit_form.email.data
            user.phone = useredit_form.phone.data
            
            db.session.add(user)
            db.session.commit()
        
            useredit_form.process()

            session['edited_user'] = True
            return redirect('/admin')
        else:
            useredit_form.process()
    
            session['edited_user'] = False
            return redirect('/admin')