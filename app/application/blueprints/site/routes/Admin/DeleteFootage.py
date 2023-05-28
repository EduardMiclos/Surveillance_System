import os

from flask import redirect, session, request
from flask_login import login_required

from .config import FOOTAGE_PATH
from .AdminInterface import AdminInterface, admin_required
from .....database import db
from .....database.models import Footage

class DeleteFootage(AdminInterface):
    base_route = f'{AdminInterface.base_route}/footage/delete'
    
    @login_required
    @admin_required
    def post(self):
        footage_id = request.form.get("footage_id")
        
        footage_query = Footage.query.filter_by(id=footage_id)
        footage = footage_query.first()
        path = f'{FOOTAGE_PATH}/{footage.camera.footages_path}/{footage.path}'
        
        if os.path.exists(path):
            os.remove(path)
        
        footage_query.delete()
        db.session.commit()
        
        session['deleted_footage'] = True
        return redirect('/admin#manage-footage')