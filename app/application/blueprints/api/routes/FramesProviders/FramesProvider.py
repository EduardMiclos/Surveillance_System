from flask import Response as FlaskResponse
import os
import cv2 as cv
from time import sleep
from datetime import datetime
import numpy as np


from .FramesProviderInterface import FramesProviderInterface
from ..config import FOOTAGE_PATH
from ...controllers import config, Response
from .....database import db
from .....database.models import Camera

class FramesProvider(FramesProviderInterface):
    base_route = f'{FramesProviderInterface.base_route}/<int:camera_id>'
    
    border_top = 5
    border_bottom = border_top
    border_left = 5
    border_right = border_left
    border_color = [51, 25, 130]
    border_type = cv.BORDER_CONSTANT
    
    """
    Caching the NNAdapter (which constructs the Neural
    Model once and loads its weights).
    """
    # def __init__(self):
    #     if FramesProvider.nn_adapter is None:
    #         FramesProvider.nn_adapter = NNAdapter()
    #     self.nn_adapter = FramesProvider.nn_adapter
    
    # def detect_violence(self, file_path):
    #     # Load the video file
    #     cap = cv.VideoCapture(file_path)

    #     # # Get the number of frames in the video
    #     num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    #     # # Create a numpy array to store the frames
    #     frames = np.zeros((num_frames, 360, 360, 3), dtype=np.float32)

    #     # Loop through the frames and store them in the numpy array
    #     for i in range(num_frames):
    #         ret, frame = cap.read()
    #         if ret:
    #             frame = cv.resize(frame, (360, 360))
    #             frames[i] = frame

    #     # Release the video capture object
    #     cap.release()
        
    #     p = adapter.predict_violence(frames)
    #     return p
    
    def _add_border(self, frame):
        return cv.copyMakeBorder(frame, 
                                 self.border_top, 
                                 self.border_bottom, 
                                 self.border_left, 
                                 self.border_right, 
                                 self.border_type, 
                                 None, 
                                 self.border_color)
        
    
    def generate_frames(self, camera):
        footages_path = f'{FOOTAGE_PATH}/temp/{camera.temp_path}'

        # Get the list of files in the directory
        files = os.listdir(footages_path)
        
        if files:
            # Get the latest file based on its modification time
            latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(footages_path, x)))
            latest_file_path = os.path.join(footages_path, latest_file)
        else:
            response = Response()
            response.set_not_found()
            return response.get_response()
    
    
        # p = self.detect_violence(latest_file_path)
    
        # Open the saved video file
        cap = cv.VideoCapture(latest_file_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Perform any processing on the frame here if needed

            resized_frame = cv.resize(frame, (config.RECOMM_FRAME_INITIAL_SIZE, config.RECOMM_FRAME_INITIAL_SIZE - 120))
            
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cv.putText(resized_frame, current_datetime, (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            
            if 'aa.' in latest_file_path:
                resized_frame = self._add_border(resized_frame)
            
            
            # Convert the frame to JPEG format
            ret, buffer = cv.imencode('.jpg', resized_frame)
            if not ret:
                break
            
            sleep(1/32)
            
            # Yield the frame as bytes for streaming
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        # Release the video capture object
        cap.release()
    
    def get(self, camera_id):
        camera = Camera.query.filter_by(id=camera_id).first()
        
        if camera is None:
            response = Response()
            response.set_not_found()
            return response.get_response()
        
        # Create a Flask response with the frames as a stream
        return FlaskResponse(self.generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')