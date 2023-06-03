from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt import JWTError

# Third party imports
from flask_restful import request
import os
import cv2 as cv

# Local application imports
from flask import Response, render_template
from flask_restful import request
from .ReceiverInterface import ReceiverInterface

class FrameReceiver(ReceiverInterface):
    base_route = f'{ReceiverInterface.base_route}/frames'
    nn_adapter = None
    
    def generate_frames(self):
        # Open the saved video file
        cap = cv.VideoCapture('Video.mp4')

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Perform any processing on the frame here if needed

            # Convert the frame to JPEG format
            ret, buffer = cv.imencode('.jpg', frame)
            if not ret:
                break

            # Yield the frame as bytes for streaming
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        # Release the video capture object
        cap.release()
        # Delete the temporary video file
        
        if os.path.exists('Video.mp4'):
            os.remove('Video.mp4')
    
    @jwt_required()
    def post(self):
        camera_id = get_jwt_identity()
        
        if camera_id is None:
            return 403
        
        file = request.files['Video2.mp4']
        file.save('Video.mp4')
        
        return 200

    def get(self):
        # Create a Flask response with the frames as a stream
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')