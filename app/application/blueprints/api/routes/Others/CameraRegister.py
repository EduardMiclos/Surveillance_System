

# from flask import request
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_sse import sse


# Local application imports
from .config import ACCESS_KEY
from ..Informers import PreprocessInformer, UtilsInformer
from .CameraInterface import CameraInterface
from .....database import db
from .....database.models import Camera
from ...controllers import Response
from .....controllers.EventStreamer import *
    

class CameraRegister(CameraInterface):
    base_route = f'{CameraInterface.base_route}/register'
    
    def post(self):
        data = request.json
        access_key = data.get('access_key')
    
        response = Response()
        
        if access_key == ACCESS_KEY:
            name = data.get("name", None)
            description = data.get("description", None)
            footages_path = data.get("footages_path", None)
            temp_path = data.get("temp_path", None)
            preprocess_data = data.get("preprocess_data", None)
            
            camera = Camera(name = name, 
                            description = description,
                            footages_path = footages_path,
                            temp_path = temp_path,
                            preprocess_data = preprocess_data)
            
            db.session.add(camera)
            db.session.commit()
            
            jwt_token = create_access_token(identity = camera.id)
            
            event_streamer = EventStreamerFactory.create(EventType.MANAGE_CAMERA_REFRESH)
            event_streamer.stream()

            response.add_data("JWT Token", jwt_token)
            response.add_data("Camera ID", camera.id)
            
            if preprocess_data:
                preprocess_informer = PreprocessInformer()
                utils_informer = UtilsInformer()
                
                preprocess_data = preprocess_informer.get()
                preprocess_data = preprocess_data.json['Data']
                
                utils_data = utils_informer.get()
                utils_data = utils_data.json['Data']['Endpoints']
                
                response.add_data("Preprocess", preprocess_data)
                response.add_data("Utils", utils_data)
                
            response.set_success()
            return response.get_response()
        
        response.set_forbidden()
        return response.get_response()