import numpy as np

def center_crop(frame_size: int, data: np.array, x_crop: int, y_crop: int) -> np.array:
        """
        This method crops the input frames to the center.
        """
        x = frame_size
        y = frame_size
        x_start = x_crop
        x_end = x - x_crop
        y_start = y_crop
        y_end = y - y_crop

        data = data[:, y_start:y_end, x_start:x_end, :]
        return data