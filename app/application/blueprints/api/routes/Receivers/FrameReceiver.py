from flask import Response as FlaskResponse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import jwt
import datetime

# Third party imports
from flask_restful import request
import os
import cv2 as cv

# Local application imports
from ...controllers import Response
from flask_restful import request
from .ReceiverInterface import ReceiverInterface
from .....database.models import Camera

class FrameReceiver(ReceiverInterface):
    base_route = f'{ReceiverInterface.base_route}/frames'
    nn_adapter = None
    
    @jwt_required()
    def post(self):
        response = Response()
        camera_id = get_jwt_identity()
        
        if camera_id is None:
            response.set_forbidden()
            return response.get_response()
        
        camera = Camera.query.filter_by(id=camera_id).first()
        if camera.status_id != 1:
            response.set_code(400)
            response.set_message('The camera is supposed to be inactive!')
            return response.get_response()
        
        file = request.files['Video2.mp4']
        file.save('Video.mp4')
        
        response = Response()
        response.add_data('JWT Token', create_access_token(identity = camera_id))
        response.set_success()
        return response.get_response()