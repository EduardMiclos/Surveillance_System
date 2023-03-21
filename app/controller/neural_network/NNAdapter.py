import numpy as np
import cv2 as cv

if __name__ == "controller.neural_network.NNAdapter":
    from controller.neural_network.NNAdapter import InputAdapter
    from controller.neural_network.NNAdapter import InputMode
else:
    import InputAdapter
    import InputMode

class NNAdapter:

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

    def __init__(resized: int = 360):
        self.input_adapter = InputAdapter(frame_size = resized)
        self.neural_model = NNModel(InputAdapter.input_mode)

    def resize(self, data: object):
        return cv.resize(data, (self.resized, self.resized))

    def predict_violence(data: object):
        data = self.resize(data)
        data = self.input_adapter.transform_data(data)

        p = self.neural_model.predict(data)
        return 1 - p