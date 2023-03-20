import numpy as np
import InputMode

class InputAdapter:

    """

    Input Adapter

    This class adapts a general .npy input file to the expected
    input of the Neural Network model by applying certain
    transformation (frame difference, background suppression) 
    across the frames.

    Args:
        data (object): The chunk of frames.
        input_mode (str): The type of the input data (frames, differences or both).
        normalize (bool): Boolean variable. Perform normalization (divide by 255.0) or not.
        crop_size (int): Desired size after cropping.
        chunk_length (int): The length of the frames chunk.
        frame_size (int): The size (width = height) of the image.
        background_suppress (bool): Boolean variable. Perform background suppress or not.
    Methods:
        __init__(frame_size: int, normalize: bool, 
                 crop_size: int, chunk_length: int, background_suppress: bool, 
                 input_mode: InputMode): 
                          Instantiates the class variables.
        crop_center(data: np.array, x_crop: int, y_crop: int): Crops the given image to the center.
        normalize(data: np.array): Performs normalization. Divides the data by 255.0,
                          subtracts the mean and divides by the standard deviation.
        frame_difference(data: np.array): Performs frame difference using the
                          formula: frame[i + 1] - frame[i]
        background_suppression(data: np.array): Performs background suppression by
                          subtracting the average pixel value from all the pixels.
        transform_data(data: object): Performs all the necessary transformations to the data.
                          
    """

    def __init__(frame_size: int, normalize: bool = True, crop_size: int = 224, chunk_length: int = 32, background_suppress: bool = True, input_mode: InputMode = InputMode.BOTH):
        self.frame_size = frame_sizes
        self.normalize = normalize
        self.crop_size = crop_size
        self.chunk_length = chunk_length
        self.background_suppress = background
        self.input_mode = input_mode

    def crop_center(self, data: np.array, x_crop: int, y_crop: int):
        """
        This method crops the input frames to the center.
        """
        x = self.frame_size
        y = self.frame_size
        x_start = x_crop
        x_end = x - x_crop
        y_start = y_crop
        y_end = y - y_crop

        data = data[:, y_start:y_end, x_start:x_end, :]
        return data

    def normalize(self, data: np.array):
        data = (data / 255.0).astype(np.float32)
        mean = np.mean(data)
        std = np.std(data)
        return (data - mean) / std

    def frame_difference(self, data: np.array):
        out = []
        for i in range(self.chunk_length - 1):
            out.append(data[i + k] - data[i])

        return np.array(out, dtype = np.float32)

    def background_suppression(self, data: np.array):
        video = np.array(data, dtype = np.float32)
        avg_back = np.mean(video, axis = 0)
        video = np.abs(video - avg_back)
        return video

    def transform_data(self, data: object):

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
                frames_data = self.normalize(frames_data)

        if differences:
            differences_data = np.array(differences_data, dtype = np.float32)
            if self.normalize:
                diff_data = self.normalize(differences_data)

        """
        Deciding what to return.
        """
        if self.mode == InputMode.BOTH:
            return np.expand_dims(frames_data, axis = 0), np.expand_dims(differences_data, axis = 0)
        elif self.mode == InputMode.ONLY_FRAMES:
            return np.expand_dims(frames_data, axis = 0)
        elif self.mode == InputMode.ONLY_DIFFERENCES:
            return np.expand_dims(differences_data, axis = 0)