# from flask import request
from flask import request, jsonify
from flask_socketio import SocketIO, emit
from flask_sse import sse
from flask_jwt_extended import create_access_token


# Local application imports
from .config import ACCESS_KEY
from ...controllers import Response, config
from .CameraInterface import CameraInterface
from .....database import db
from .....database.models import Camera

class CameraRegister(CameraInterface):
    base_route = f'{CameraInterface.base_route}/register'
    
    def post(self):
        data = request.json
        
        access_key = data.get('access_key')
        
        if access_key == ACCESS_KEY:
            name = request.json.get("name", None)
            description = request.json.get("description", None)
            footages_path = request.json.get("footages_path", None)
            temp_path = request.json.get("temp_path", None)
            
            camera = Camera(name = name, 
                            description = description,
                            footages_path = footages_path,
                            temp_path = temp_path)
            
            db.session.add(camera)
            db.session.commit()
            
            access_token = create_access_token(identity = camera.id)

            sse.publish({"message": "camera_register_refresh"}, type='camera_register_refresh')
            return jsonify({ "token": access_token, "camera_id": camera.id })
        return 403
        
        