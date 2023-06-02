import os
import shutil

from flask import redirect, session, request
from flask_login import login_required
from sqlalchemy import func

from ..AdminInterface import AdminInterface, admin_required
from ......database import db
from ......database.models import Camera
from ......controllers.EventStreamer import *

class UpdateCamera(AdminInterface):
    base_route = f'{AdminInterface.base_route}/camera/update'
    
    @login_required
    @admin_required
    def post(self):
        camera_id = request.form.get("updated_camera_id")
        
        camera = Camera.query.filter_by(id=camera_id).first()
        camera.last_update = func.current_timestamp()
        camera.status_id = 2
        
        db.session.add(camera)
        db.session.commit()
        
        event_streamer = EventStreamerFactory.create(EventType.RASP_UPDATE)
        event_streamer.add_data('Camera ID', camera.id)
        event_streamer.stream()
        
        session['updated_camera'] = True
        return redirect('/admin/manage-surveillance-cameras')