from flask_restful import Resource, request

if __name__ == "__main__":
    from schemas.FrameReceiverSchema import frame_receiver_schema
else:
    from .schemas.FrameReceiverSchema import frame_receiver_schema
    from controllers.neural_network.NNAdapter import NNAdapter

import tensorflow as tf
import numpy as np

tf.compat.v1.enable_eager_execution()
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
    array = array.reshape((32, 224, 224, 3))

    return array

class FrameReceiver(Resource):
    def post(self):
        data = request.data
        
        # errors = frame_receiver_schema.validate(form_data)
        
        # Continue later
        # if errors:
            # return errors
        
        nn_adapter = NNAdapter()
        frames = deserialize_numpy_array(data)
        return nn_adapter.predict_violence(data)
        
        return "123"