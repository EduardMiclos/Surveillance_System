import numpy as np

def normalization(data: np.array) -> np.array:
        data = (data / 255.0).astype(np.float32)
        mean = np.mean(data)
        std = np.std(data)
        return (data - mean) / std