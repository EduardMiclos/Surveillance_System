from flask import redirect, session, request


from .AdminInterface import AdminInterface
from .....database import db
from .....database.models import User

class DeleteUser(AdminInterface):
    base_route = f'{AdminInterface.base_route}/delete-user'
    
    def post(self):
        user_id = request.form.get("user_id")
        
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        
        session['deleted_user'] = True
        return redirect('/admin')