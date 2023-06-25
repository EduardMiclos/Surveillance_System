from flask_restful import Resource

from ..ViewerInterface import ViewerInterface

class ProfileInterface(Resource):
    base_route = f'{ViewerInterface.base_route}/profile'