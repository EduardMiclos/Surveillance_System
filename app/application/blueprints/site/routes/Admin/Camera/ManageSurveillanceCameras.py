# Third party imports
from flask import render_template, make_response, session
from flask_login import login_required, current_user

# Local application imports
from ..AdminInterface import AdminInterface, admin_required
from ....forms import CameraEditForm

from ......database.models import Camera

class ManageSurveillanceCameras(AdminInterface):
    base_route = f'{AdminInterface.base_route}/manage-surveillance-cameras'
    
    @login_required
    @admin_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        cameraedit_form = CameraEditForm()
        cameras = Camera.query.all()
        deleted_camera = session.pop('deleted_camera', default=False)
        edited_camera = session.pop('edited_camera', default=False)
        
        return make_response(
            render_template('manage-surveillance-cameras.html',
                            current_user = current_user,
                            cameras = cameras,
                            deleted_camera = deleted_camera,
                            edited_camera = edited_camera, 
                            cameraedit_form = cameraedit_form),
            200, headers
            )
            