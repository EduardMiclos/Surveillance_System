from flask_restful import Resource

from ..controllers.neural_network import config

data_preprocessing_info = {
    "Chunk Size": 32,
    "Image Channels": 32,
    "Frame Size": {
        "Value": 224,
        "Cropped From": 360
    },
    "Normalization": True,
    "Frame Difference": True,
    "Background Suppression": True,
    "Shape": "(2, 1, 32, 224, 224, 3)"
}

class PreprocessInformer(Resource):
    def get(self):
        json = {
            "ChunkSize": config.RECOMM_CHUNK_SIZE,
            "Channels": config.RECOMM_IMG_CHANNELS,
            "FrameSize": {
                "Value": config.RECOMM_FRAME_CROP,
                "CroppedFrom": config.RECOMM_FRAME_INITIAL_SIZE
            },
            "Normalization": config.RECOMM_NORMALIZATION,
            "FrameDiff": config.RECOMM_FRAME_DIFF,
            "BackgrSuppr": config.RECOMM_BACKGR_SUPPR,
            "Compression": config.RECOMM_COMPRESSION_ALG,
            "DataFormat": config.RECOMM_VIDEO_EXT
        }
        
        return json
    
    