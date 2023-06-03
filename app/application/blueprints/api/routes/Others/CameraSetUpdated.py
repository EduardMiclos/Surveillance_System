from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt import JWTError


# Local application imports
from .CameraInterface import CameraInterface
from .....database import db
from .....database.models import Camera
from ...controllers import Response
from .....controllers.EventStreamer import *
    

class CameraSetUpdated(CameraInterface):
    base_route = f'{CameraInterface.base_route}/set-updated'

    @jwt_required() 
    def get(self):
        response = Response()
        
        try:
            camera_id = get_jwt_identity()
            if not camera_id:
                response.set_forbidden()
                return response.get_response()
                    
            camera = Camera.query.get(camera_id)
            camera.status_id = 1
            db.session.add(camera)
            db.session.commit()
            
            event_streamer = EventStreamerFactory.create(EventType.MANAGE_CAMERA_REFRESH)
            event_streamer.stream()
            
        except JWTError:
            response.set_forbidden()
            return response.get_response()
            
        response.add_data('JWT Token', create_access_token(identity = camera_id))
        response.set_success()
        return response.get_response()