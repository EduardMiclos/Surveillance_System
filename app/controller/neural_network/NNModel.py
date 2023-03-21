import InputMode


class NNModel(object):
    """

    Neural Network Model

    This class is a Singleton wrapper for the already trained
    Neural Network model.

    Static variables:
        input_mode: InputMode
    Args:
        input_mode (InputMode): The type of the input data (frames, differences or both).
    Methods:
        __init__(reized: int): Instantiates the class variables.
        
                          
    """

    """
    Singleton logic for the NNModel class.
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NNModel, cls).__new__(cls)
        return cls.instance

    def __init__(input_mode: InputMode):
        self.input_mode = input_mode
        self.generate_model()

    def generate_model(self):
        pass

    def predict(self, data: object):
        return 0.1
