from flask import Response as FlaskResponse
import os
import cv2 as cv

from .FramesProviderInterface import FramesProviderInterface

class FramesProvider(FramesProviderInterface):
    base_route = f'{FramesProviderInterface.base_route}/<int:camera_id>'
    
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
    
    def get(self, camera_id):
        # Create a Flask response with the frames as a stream
        return FlaskResponse(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')