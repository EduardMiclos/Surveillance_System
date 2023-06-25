from flask import redirect, session, request
from flask_login import login_required

from ..AdminInterface import AdminInterface, admin_required
from .....api.routes.Informers import PreprocessInformer, UtilsInformer
from ......database import db
from ....forms import CameraEditForm
from ......database.models import Camera
from ......controllers.EventStreamer import *

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
            
            event_streamer = EventStreamerFactory.create(EventType.RASP_EDIT)
            
            if cameraedit_form.preprocess_data.data and not camera.preprocess_data:
                preprocess_informer = PreprocessInformer()
                utils_informer = UtilsInformer()
                
                preprocess_data = preprocess_informer.get()
                preprocess_data = preprocess_data.json['Data']
                
                utils_data = utils_informer.get()
                utils_data = utils_data.json['Data']['Endpoints']
                
                event_streamer.add_data("Preprocess", preprocess_data)
                event_streamer.add_data("Utils", utils_data)
            
            camera.preprocess_data = cameraedit_form.preprocess_data.data
            
            event_streamer.add_data('Camera ID', camera.id)
            event_streamer.add_data('Camera Name', camera.name)
            event_streamer.add_data('Camera Description', camera.description)
            event_streamer.add_data('Camera Preprocess', camera.preprocess_data)
        
        
            db.session.add(camera)
            db.session.commit()
        
            cameraedit_form.process()

            event_streamer.stream()
            session['edited_camera'] = True
            return redirect('/admin/manage-surveillance-cameras')
        else:
            cameraedit_form.process()
    
            session['edited_camera'] = False
            return redirect('/admin/manage-surveillance-cameras')