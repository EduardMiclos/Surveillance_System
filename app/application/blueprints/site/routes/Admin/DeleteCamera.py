import os
import shutil

from flask import redirect, session, request
from flask_login import login_required

from .config import FOOTAGE_PATH
from .AdminInterface import AdminInterface, admin_required
from .....database import db
from .....database.models import Footage, Camera

class DeleteCamera(AdminInterface):
    base_route = f'{AdminInterface.base_route}/camera/delete'
    
    @login_required
    @admin_required
    def post(self):
        camera_id = request.form.get("camera_id")
        delete_footages = request.form.get("delete_footages")
        
        camera_query = Camera.query.filter_by(id=camera_id)
        camera = camera_query.first()
        footages_path = f'{FOOTAGE_PATH}/{camera.footages_path}'
        temp_path = f'{FOOTAGE_PATH}/temp/{camera.temp_path}'
        
        if delete_footages:
            footages = Footage.query.filter_by(camera_id=camera_id).all()
            for footage in footages:
                db.session.delete(footage)
                
            if os.path.exists(footages_path):
                shutil.rmtree(footages_path)
                
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
                              
        camera_query.delete()
        db.session.commit()
        
        session['deleted_camera'] = True
        return redirect('/admin#manage-surveillance-cameras')