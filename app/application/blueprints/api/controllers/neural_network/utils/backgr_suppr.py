import numpy as np

def backgr_suppr(data: np.array) -> np.array:
        video = np.array(data, dtype = np.float32)
        avg_back = np.mean(video, axis = 0)
        video = np.abs(video - avg_back)
        return video