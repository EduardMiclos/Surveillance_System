import numpy as np

def frame_difference(chunk_length: int, data: np.array) -> np.array:
        out = []
        for i in range(chunk_length - 1):
            out.append(data[i + 1] - data[i])

        return np.array(out, dtype = np.float32)