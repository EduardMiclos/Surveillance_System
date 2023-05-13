from flask_restful import Resource

from ..controllers.Response import Response

from .BackgrSupprProvider import BackgrSupprProvider
from .CenterCropProvider import CenterCropProvider
from .FrameDifferenceProvider import FrameDifferenceProvider
from .NormalizationProvider import NormalizationProvider

providers = [BackgrSupprProvider, CenterCropProvider, FrameDifferenceProvider, NormalizationProvider]

class UtilsInformer(Resource):
    def get(self):
        response = Response()
        response.add_data("Description", "The end-user is able to fetch certain utils files in order to perform the frame preprocessing before sending the chunk of data to the central server. This results in a faster request response.")
        
        response.add_data("Endpoints:", 
                         [f'/api/get/utils/{provider.request_endpoint}' for provider in providers])
        
        response.set_success()
        return response.get_response()
        

    