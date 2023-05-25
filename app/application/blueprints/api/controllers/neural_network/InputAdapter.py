import numpy as np

from .InputMode import InputMode
from .utils import *

class InputAdapter:

    """

    Input Adapter

    This class adapts an array object to the expected
    input of the Neural Network model by applying certain
    transformations (frame difference, background suppression) 
    across the frames.

    Args:
        frame_size (int): The size (width = height) of the image.
        normalize (bool): Boolean variable. Perform normalization or not.
        crop_size (int): Desired size after cropping.
        chunk_length (int): The length of the frames chunk.
        background_suppress (bool): Boolean variable. Perform background suppress or not.
        input_mode (InputMode): The type of the input data (frames, differences or both).
    Methods:
        __init__(frame_size: int, normalize: bool, 
                 crop_size: int, chunk_length: int, background_suppress: bool, 
                 input_mode: InputMode): 
                          Instantiates the class variables.
        crop_center(data: np.array, x_crop: int, y_crop: int): Crops the given image to the center.
        normalize(data: np.array): Performs normalization. Divides the data by 255.0,
                          subtracts the mean and divides by the standard deviation.
        frame_difference(data: np.array): Performs frame difference using the
                          formula: frame[i + 1] - frame[i].
        background_suppression(data: np.array): Performs background suppression by
                          subtracting the average pixel value from all the pixels.
        transform_data(data: object): Performs all the necessary transformations to the data.
                          
    """

    def __init__(self, 
                 frame_size: int, 
                 normalize: bool = True, 
                 crop_size: int = 224, 
                 chunk_length: int = 32, 
                 background_suppress: bool = True, 
                 input_mode: InputMode = InputMode.BOTH) -> None:
        self.frame_size = frame_size
        self.normalize = normalize
        self.crop_size = crop_size
        self.chunk_length = chunk_length
        self.background_suppress = background_suppress
        self.input_mode = input_mode

    def crop_center(self, data: np.array, x_crop: int, y_crop: int) -> np.array:
        """
        This method crops the input frames to the center.
        """
        return center_crop(self.frame_size, data, x_crop, y_crop)

    def normalize_data(self, data: np.array) -> np.array:
        return normalization(data)

    def frame_difference(self, data: np.array) -> np.array:
        return frame_difference(self.chunk_length, data)

    def background_suppression(self, data: np.array) -> np.array:
        return backgr_suppr(data)

    def transform_data(self, data: object) -> object:

        """
        Converting the data to float32.
        """
        data = np.float32(data)

        """
        Deciding which actions to take depending
        on the input mode.
        """
        if self.input_mode == InputMode.BOTH:
            frames = True
            differences = True
        elif self.input_mode == InputMode.ONLY_FRAMES:
            frames = True
            differences = False
        elif self.input_mode == InputMode.ONLY_DIFFERENCES:
            frames = False
            differences = True

        """
        Cropping the image
        """
        data = self.crop_center(data, 
                                x_crop = (self.frame_size - self.crop_size)//2, 
                                y_crop = (self.frame_size - self.crop_size)//2)

        """
        Performing frame difference, if it's the case.
        """
        if differences:
            differences_data = self.frame_difference(data)

        """
        Performing background suppression, if it's the case.
        """
        if frames and self.background_suppress:
            frames_data = self.background_suppression(data)

        
        """
        Performing normalization.
        """
        if frames:
            frames_data = np.array(frames_data, dtype = np.float32)
            if self.normalize:     
                frames_data = self.normalize_data(frames_data)

        if differences:
            differences_data = np.array(differences_data, dtype = np.float32)
            if self.normalize:
                differences_data = self.normalize_data(differences_data)

        """
        Deciding what to return.
        We're also expanding the dims according to the model input shape: 
        (chunk_length, crop_size, crop_size, 3) -> (1, chunk_length, crop_size, crop_size, 3)
        """
        if self.input_mode == InputMode.BOTH:
            return np.expand_dims(frames_data, axis = 0), np.expand_dims(differences_data, axis = 0)
        elif self.input_mode == InputMode.ONLY_FRAMES:
            return np.expand_dims(frames_data, axis = 0)
        elif self.input_mode == InputMode.ONLY_DIFFERENCES:
            return np.expand_dims(differences_data, axis = 0)