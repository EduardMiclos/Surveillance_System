from flask import Blueprint
from flask_restful import Api

from .routes.FrameReceiver import FrameReceiver
from .routes.PreprocessInformer import PreprocessInformer
from .routes.BackgrSupprProvider import BackgrSupprProvider
from .routes.CenterCropProvider import CenterCropProvider
from .routes.FrameDifferenceProvider import FrameDifferenceProvider
from .routes.NormalizationProvider import NormalizationProvider
from .routes.UtilsInformer import UtilsInformer

"""
Creating the Blueprint for the API.
"""
api_bp = Blueprint('api', __name__, url_prefix='/api')

"""
Creating the API for this specific blueprint.
"""
api = Api(api_bp)

"""
Adding all the necessary resources to the blueprint's api.
"""

"""
GET resources.
"""

"""
Informers
"""
api.add_resource(PreprocessInformer, '/get/info/preprocess')
api.add_resource(UtilsInformer, '/get/info/utils')

"""
File providers
"""
api.add_resource(BackgrSupprProvider, f'/get/utils/{BackgrSupprProvider.request_endpoint}')
api.add_resource(CenterCropProvider, f'/get/utils/{CenterCropProvider.request_endpoint}')
api.add_resource(FrameDifferenceProvider, f'/get/utils/{FrameDifferenceProvider.request_endpoint}')
api.add_resource(NormalizationProvider, f'/get/utils/{NormalizationProvider.request_endpoint}')

"""
POST resources.
"""
api.add_resource(FrameReceiver, '/send/frames')