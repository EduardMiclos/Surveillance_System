import os
import shutil

from flask import redirect, session, request
from flask_login import login_required

from ..config import FOOTAGE_PATH
from ..AdminInterface import AdminInterface, admin_required
from ......database import db
from ......database.models import Footage, Camera
from ......controllers.EventStreamer import *

class ToggleCamera(AdminInterface):
    base_route = f'{AdminInterface.base_route}/camera/toggle'
    
    @login_required
    @admin_required
    def post(self):
        camera_id = request.form.get("toggled_camera_id")
        camera = Camera.query.filter_by(id=camera_id).first()
        camera.status_id = camera.status_id ^ 1
        
        if camera.status_id:
            event_streamer = EventStreamerFactory.create(EventType.RASP_START)
        else:
            event_streamer = EventStreamerFactory.create(EventType.RASP_STOP)
        
        event_streamer.add_data('Camera ID', camera.id)
        event_streamer.stream()
            
        db.session.add(camera)
        db.session.commit()
        
        return redirect('/admin/manage-surveillance-cameras')