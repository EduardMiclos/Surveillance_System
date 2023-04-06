import tensorflow as tf
import numpy as np
import cv2 as cv
import os
from flask_restful import Resource, request

from .schemas.FrameReceiverSchema import frame_receiver_schema
from ..controllers.neural_network.NNAdapter import NNAdapter
from ..controllers.neural_network import config


class FrameReceiver(Resource):
    nn_adapter = None
    
    """
    Caching the NNAdapter (which constructs the Neural
    Model once and loads its weights).
    """
    def __init__(self):
        if FrameReceiver.nn_adapter is None:
            FrameReceiver.nn_adapter = NNAdapter()
    
    def post(self):
        file = request.files['Video2.mp4']
        file.save('./temp/Video.mp4')
        
        # Load the video file
        cap = cv.VideoCapture('./temp/Video.mp4')

        # Get the number of frames in the video
        num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

        # Create a numpy array to store the frames
        frames = np.zeros((num_frames, 360, 360, 3), dtype=np.float32)

        # Loop through the frames and store them in the numpy array
        for i in range(num_frames):
            ret, frame = cap.read()
            if ret:
                frame = cv.resize(frame, (360, 360))
                frames[i] = frame

        # Release the video capture object
        cap.release()
        os.remove('./temo/Video.mp4')
        
        p = FrameReceiver.nn_adapter.predict_violence(frames)
        return str(p)