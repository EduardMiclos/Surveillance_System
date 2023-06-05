from flask import Response as FlaskResponse
import os
import cv2 as cv
from time import sleep
from datetime import datetime

from .FramesProviderInterface import FramesProviderInterface
from ..config import FOOTAGE_PATH
from ...controllers import config, Response
from .....database.models import Camera

class FramesProvider(FramesProviderInterface):
    base_route = f'{FramesProviderInterface.base_route}/<int:camera_id>'
    
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
            
            
            # Convert the frame to JPEG format
            ret, buffer = cv.imencode('.jpg', resized_frame)
            if not ret:
                break
            
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