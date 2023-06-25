from NNAdapter import NNAdapter
import cv2 as cv
import numpy as np
import time

adapter = NNAdapter()

def detect_violence(file_path):
    # Load the video file
    cap = cv.VideoCapture(file_path)

    # # Get the number of frames in the video
    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    # # Create a numpy array to store the frames
    frames = np.zeros((num_frames, 360, 360, 3), dtype=np.float32)

    # Loop through the frames and store them in the numpy array
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frame = cv.resize(frame, (360, 360))
            frames[i] = frame

    # Release the video capture object
    cap.release()
    
    start_time = time.time()
    p = adapter.predict_violence(frames)
    print("--- %s seconds ---" % (time.time() - start_time))

    return p

p = detect_violence('/home/miclosedi/Surveillance_System/app/application/database/footage/temp/PARTER_1/fight_example.mp4')
print(p)