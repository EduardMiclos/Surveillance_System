from flask import redirect, session, request
from flask_login import login_required

from .AdminInterface import AdminInterface, admin_required
from .....database import db
from .....database.models import User

class DeleteUser(AdminInterface):
    base_route = f'{AdminInterface.base_route}/user/delete'
    
    @login_required
    @admin_required
    def post(self):
        user_id = request.form.get("user_id")
        
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        
        session['deleted_user'] = True
        return redirect('/admin')