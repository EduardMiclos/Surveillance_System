from flask import Response as FlaskResponse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import jwt
from datetime import datetime
import os
import cv2 as cv
import numpy as np


# Third party imports
from flask_restful import request

# Local application imports
from ..config import FOOTAGE_PATH
from ...controllers import config
from ...controllers import Response
from flask_restful import request
from .ReceiverInterface import ReceiverInterface
from .....database.models import Camera

# from .nn_adapter import adapter

class FrameReceiver(ReceiverInterface):
    base_route = f'{ReceiverInterface.base_route}/frames'
    
    def _delete_oldest_footage(self, directory):
        files = os.listdir(directory)

        if len(files) > 20:
            # Sort the files based on their modification time in ascending order
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
            
            # Delete the oldest file
            oldest_file = sorted_files[0]
            file_path = os.path.join(directory, oldest_file)
            os.remove(file_path)
    
    def detect_violence(self, file_path):
        # Load the video file
        cap = cv.VideoCapture(file_path)

        # # Get the number of frames in the video
        num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

        # # Create a numpy array to store the frames
        frames = np.zeros((num_frames, 360, 360, 3), dtype=np.float32)

        # Loop through the frames and store them in the numpy array
        for i in range(num_frames):
            ret, frame = cap.read()
            if ret:
                frame = cv.resize(frame, (360, 360))
                frames[i] = frame

        # Release the video capture object
        cap.release()
        
        # p = adapter.predict_violence(frames)
        # return p
    
    @jwt_required()
    def post(self):
        response = Response()
        camera_id = get_jwt_identity()
        
        if camera_id is None:
            response.set_forbidden()
            return response.get_response()
        
        camera = Camera.query.filter_by(id=camera_id).first()
        
        if camera is None:
            response.set_forbidden()
            return response.get_response()
        
        if camera.status_id != 1:
            response.set_code(400)
            response.set_message('The camera is supposed to be inactive!')
            return response.get_response()
        
        file = request.files[f'{config.RECOMM_CHUNK_NAME}.{config.RECOMM_VIDEO_EXT}']
        footages_path = f'{FOOTAGE_PATH}/temp/{camera.temp_path}'
        
        current_datetime = datetime.now().strftime('%H%S%f')
        video_path = f'{footages_path}/REG_{camera.name}_{current_datetime}.{config.RECOMM_VIDEO_EXT}'
        
        self._delete_oldest_footage(footages_path)
        
        file.save(video_path)
        
        # p = self.detect_violence(video_path)
        # print(p)
        
        response = Response()
        response.add_data('JWT Token', create_access_token(identity = camera_id))
        response.set_success()
        return response.get_response()