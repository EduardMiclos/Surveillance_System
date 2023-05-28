from flask import redirect, session, request
from flask_login import login_required

from .AdminInterface import AdminInterface, admin_required
from .....database import db
from ...forms import CameraEditForm
from .....database.models import Camera

class EditCamera(AdminInterface):
    base_route = f'{AdminInterface.base_route}/camera/edit'
    
    @login_required
    @admin_required
    def post(self):
        cameraedit_form = CameraEditForm()
        
        if cameraedit_form.validate_on_submit():
            camera_id = request.form.get("camera_id")
            
            camera = Camera.query.filter_by(id = camera_id).first()
            
            camera.name = cameraedit_form.name.data
            camera.description = cameraedit_form.description.data
            
            db.session.add(camera)
            db.session.commit()
        
            cameraedit_form.process()

            session['edited_camera'] = True
            return redirect('/admin#manage-surveillance-cameras')
        else:
            cameraedit_form.process()
    
            session['edited_camera'] = False
            return redirect('/admin#manage-surveillance-cameras')