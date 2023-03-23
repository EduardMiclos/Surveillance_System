from flask import Blueprint
from flask_restful import Api

if __name__ == "__main__":
    from routes.FrameReceiver import FrameReceiver
else:
    from .routes.FrameReceiver import FrameReceiver

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
api.add_resource(FrameReceiver, '/send/frames')