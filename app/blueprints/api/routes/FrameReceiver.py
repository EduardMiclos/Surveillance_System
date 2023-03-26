from flask_restful import Resource, request

if __name__ == "__main__":
    from schemas.FrameReceiverSchema import frame_receiver_schema
else:
    from .schemas.FrameReceiverSchema import frame_receiver_schema
    from controllers.neural_network.NNAdapter import NNAdapter

import tensorflow as tf
import numpy as np
import cv2


# tf.compat.v1.enable_eager_execution()
array_msg = tf.train.Example(features=tf.train.Features(feature={
    'data': tf.train.Feature(bytes_list=tf.train.BytesList(value=[b'']))}))

def serialize_numpy_array(array):
    # Convert the NumPy array to a byte string
    byte_string = array.tobytes()

    # Update the protobuf message with the byte string
    array_msg.features.feature['data'].bytes_list.value[0] = byte_string

    # Serialize the protobuf message to a byte string
    serialized = array_msg.SerializeToString()

    return serialized

def deserialize_numpy_array(byte_string):
    # Parse the protobuf message from the byte string
    array_msg.ParseFromString(byte_string)

    # Extract the byte string from the message
    byte_string = array_msg.features.feature['data'].bytes_list.value[0]

    # Convert the byte string back to a NumPy array
    array = np.frombuffer(byte_string, dtype=np.float32)
    array = array.reshape((32, 360, 360, 3))

    return array

import cv2 as cv
from matplotlib import pyplot as plt

class FrameReceiver(Resource):
    nn_adapter = None
    
    def __init__(self):
        if FrameReceiver.nn_adapter is None:
            FrameReceiver.nn_adapter = NNAdapter()
    
    def post(self):
        file = request.files['Video2.mp4']
        file.save('Video.mp4')
        
        # Load the video file
        cap = cv2.VideoCapture('Video.mp4')

        # Get the number of frames in the video
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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

        p = FrameReceiver.nn_adapter.predict_violence(frames)
        return str(p)