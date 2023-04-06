from flask import Blueprint
from flask_restful import Api

from .routes.FrameReceiver import FrameReceiver
from .routes.PreprocessInformer import PreprocessInformer


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
api.add_resource(PreprocessInformer, '/get/preprocessinfo')


"""
POST resources.
"""
api.add_resource(FrameReceiver, '/send/frames')