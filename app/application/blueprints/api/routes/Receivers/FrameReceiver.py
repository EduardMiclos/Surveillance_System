from flask import Response as FlaskResponse, current_app, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import jwt
from datetime import datetime
import os
import cv2 as cv
import numpy as np
from random import random
import glob
from moviepy.editor import concatenate_videoclips, VideoFileClip
import shutil
from werkzeug.local import LocalProxy
from multiprocessing import Process
from .nn_adapter import adapter

# Third party imports
from flask_restful import request

# Local application imports
from ..config import FOOTAGE_PATH
from ...controllers import config
from ...controllers import Response
from .....database import db
from flask_restful import request
from .ReceiverInterface import ReceiverInterface
from .....database.models import Camera, Footage

# from .nn_adapter import adapter

class FrameReceiver(ReceiverInterface):
    base_route = f'{ReceiverInterface.base_route}/frames'

    def __delete_oldest_footage(self, directory):
        files = os.listdir(directory)

        if len(files) > 20:
            # Sort the files based on their modification time in ascending order
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
            
            # Delete the oldest file
            oldest_file = sorted_files[0]
            file_path = os.path.join(directory, oldest_file)
            os.remove(file_path)

    def __save_footage(self, temp_footages_path, footages_path, camera_id):
        
        if len(os.listdir(temp_footages_path)) < config.DETECTIONS_THRESHOLD:
            return
        
        # Find MP4 files containing 'V.' in the source folder
        file_pattern = f'{temp_footages_path}/*V.*.mp4'
        mp4_files = glob.glob(file_pattern)
        
        # Sort the files by modification time (most recent last)
        mp4_files.sort(key=lambda x: os.path.getmtime(x))
        
        # Select the last N files
        last_files = mp4_files[-config.DETECTIONS_THRESHOLD:]

    
        clips = [VideoFileClip(file) for file in last_files]
        
        merged_clip = concatenate_videoclips(clips)
        
        last_file_name = os.path.basename(last_files[-1])

        output_path = os.path.join(footages_path, f'{last_file_name}')
        
        merged_clip.write_videofile(output_path)
        
        footage = Footage(name=last_file_name, path = last_file_name, camera_id = camera_id)
        db.session.add(footage)
        db.session.commit()
    
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
                # frame = cv.resize(frame, (360, 360))
                frames[i] = frame

        # Release the video capture object
        cap.release()
        
        p = adapter.predict_violence(frames)
        return p
    
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
        footages_path = f'{FOOTAGE_PATH}/{camera.footages_path}'
        temp_footages_path = f'{FOOTAGE_PATH}/temp/{camera.temp_path}'
        
        current_datetime = datetime.now().strftime('%H%S%f')
        video_path = f'{temp_footages_path}/REG_{camera.name}_{current_datetime}.{config.RECOMM_VIDEO_EXT}'
        
        self.__delete_oldest_footage(temp_footages_path)
        file.save(video_path)
        
        p = self.detect_violence(video_path)
        
        if p > config.VIOLENCE_THRESHOLD:
            os.rename(video_path, f'{temp_footages_path}/V.REG_{camera.name}_{current_datetime}.{config.RECOMM_VIDEO_EXT}')
            
            camera.current_detections += 1
            
            if camera.current_detections >= config.DETECTIONS_THRESHOLD:
                process = Process(target=self.__save_footage, args=(temp_footages_path, footages_path, camera.id))
                process.start()
                
                self.__save_footage(temp_footages_path, footages_path, camera.id)
                
                camera.current_detections = 0
        else:
            camera.current_detections = max(camera.current_detections - 1, 0)
            
        
        db.session.add(camera)
        db.session.commit()
        
        
        response = Response()
        response.add_data('JWT Token', create_access_token(identity = camera_id))
        response.set_success()
        return response.get_response()