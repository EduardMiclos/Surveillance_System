"""
This config file contains all the necessary information
regarding the preprocessing of images data.
"""

"""
Recommended number of frames to be send
for each request.
"""
RECOMM_CHUNK_SIZE = 32


"""
Recommended number of image color channels.
"""
RECOMM_IMG_CHANNELS = 3


"""
Recommended frame size after cropping.
"""
RECOMM_FRAME_CROP = 224


"""
Recommended frame size before cropping.
"""
RECOMM_FRAME_INITIAL_SIZE = 360


"""
Recommended normalization usage.
"""
RECOMM_NORMALIZATION = True


"""
Recommended frame difference usage.
"""
RECOMM_FRAME_DIFF = True


"""
Recommended background suppression usage.
"""
RECOMM_BACKGR_SUPPR = True


"""
Recommended compression algorithm.
"""
RECOMM_COMPRESSION_ALG = "h264"


"""
Recommended video extension.
"""
RECOMM_VIDEO_EXT = "mp4"