from flask_restful import Resource

from ..controllers.neural_network import config


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
    
    