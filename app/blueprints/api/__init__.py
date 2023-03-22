from flask import Blueprint
from flask_restful import Api

if __name__ == "__main__":
    from routes.FrameReceiver import FrameReceiver
else:
    from .routes.FrameReceiver import FrameReceiver

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)


api.add_resource(FrameReceiver, '/sendframes')