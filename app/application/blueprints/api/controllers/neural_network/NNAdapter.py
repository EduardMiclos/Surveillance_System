import numpy as np
import cv2 as cv

from .InputMode import InputMode
from .InputAdapter import InputAdapter
from .NNModel import NNModel
    

class NNAdapter:
    pass

    """

    Neural Network adapter

    This class prepares the input for the Neural Network model,
    calls the transform_data() method of the InputAdapter and the predict()
    method of the Neural Network model.

    Static variables:
        input_mode: InputMode
    Args:
        resized (int): The desired size of the image after resize.
    Methods:
        __init__(reized: int): Instantiates the class variables.
        resize(data: object): Resizes the frame.
        predict_violence(data: object): Transforms data
                            by calling the transform_data() method of the 
                            input_adapter. After that, it calls the 
                            predict() method of the Neural Network model.
                          
    """

    input_mode = InputMode.BOTH

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, frame_size: int = 360):
        if not self._initialized:
            self.input_adapter = InputAdapter(frame_size=frame_size)
            self.neural_model = NNModel(NNAdapter.input_mode)
            self._initialized = True

    def predict_violence(self, data: object):
        data = self.input_adapter.transform_data(data)

        p = self.neural_model.predict(data)
        return 1 - p[0]