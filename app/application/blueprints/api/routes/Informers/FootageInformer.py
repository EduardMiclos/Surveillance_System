from flask_login import login_required

from .InformerInterface import InformerInterface
from ..config import FOOTAGE_PATH
from ...controllers.Response import Response
from .....database.models import Footage

class FootageInformer(InformerInterface):
    base_route = f'{InformerInterface.base_route}/footage/<int:footage_id>'
    
    @login_required
    def get(self, footage_id):
        footage = Footage.query.get(footage_id)
    
        response = Response()
        if footage is None:
            response.set_not_found()
            response.set_message("Footage not found!")
            return response.get_response()
    
        # Serialize the user object excluding the password field
        serialized_footage = {
            'id': footage.id,
            'name': footage.name,
            'date': footage.date,
            'path': f'{FOOTAGE_PATH}/{footage.camera.footages_path}/{footage.path}',
            'camera_id': footage.camera_id
        }
        
        response.set_success()
        response.add_data("Footage", serialized_footage)
        return response.get_response()
        