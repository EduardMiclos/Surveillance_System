from flask_login import login_required

from ....api.controllers.Response import Response
from .AdminInterface import AdminInterface, admin_required
from .....database.models import Camera

class GetCamera(AdminInterface):
    base_route = f'{AdminInterface.base_route}/camera/get/<int:camera_id>'
    
    @login_required
    @admin_required
    def get(self, camera_id):
        camera = Camera.query.get(camera_id)
    
        response = Response()
        if camera is None:
            response.set_not_found()
            response.set_message("Camera not found!")
            return response.get_response()
    
        # Serialize the camera object excluding the password field
        serialized_camera = {
            'id': camera.id,
            'name': camera.name,
            'description': camera.description,
            'status': camera.status.name,
            'last_restart': camera.last_restart,
            'last_update': camera.last_update,
            'footages_path': camera.footages_path,
            'temp_path': camera.temp_path
        }
        
        response.set_success()
        response.add_data("Camera", serialized_camera)
        return response.get_response()
        