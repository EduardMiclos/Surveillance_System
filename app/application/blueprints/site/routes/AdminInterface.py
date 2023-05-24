from flask_restful import Resource

from .ViewerInterface import ViewerInterface

class AdminInterface(Resource):
    base_route = f'{ViewerInterface.base_route}/admin'