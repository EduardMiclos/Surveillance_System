from flask_restful import Resource

from ..controllers.neural_network import config
from ..controllers.Response import Response

class PreprocessInformer(Resource):
    def get(self):
        response = Response()
        
        response.add_data("ChunkSize", config.RECOMM_CHUNK_SIZE)
        response.add_data("Channels", config.RECOMM_IMG_CHANNELS)
        response.add_data("FrameSize", {"Value": config.RECOMM_FRAME_CROP,
                                        "CroppedFrom": config.RECOMM_FRAME_INITIAL_SIZE
                                        })
        response.add_data("Normalization", config.RECOMM_NORMALIZATION)
        response.add_data("FrameDiff", config.RECOMM_FRAME_DIFF)
        response.add_data("BackgrSuppr", config.RECOMM_BACKGR_SUPPR)
        response.add_data("Compression", config.RECOMM_COMPRESSION_ALG)
        response.add_data("DataFormat", config.RECOMM_VIDEO_EXT)        
        
        response.set_success()
        return response.get_response()

    