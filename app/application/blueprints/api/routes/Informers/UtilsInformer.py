# Local application imports
from ...controllers import Response
from .. import UtilsProviders
from .InformerInterface import InformerInterface

class UtilsInformer(InformerInterface):
    base_route = f'{InformerInterface.base_route}/utils'
    
    def get(self):
        response = Response()
        response.add_data("Description", "The end-user is able to fetch certain utils files in order to perform the frame preprocessing before sending the chunk of data to the central server. This results in a faster request response.")
        
        response.add_data("Endpoints:", 
                         [f'/api/get/utils/{provider.base_route}' for provider in UtilsProviders.ProviderInterface.__subclasses__()])
        
        response.set_success()
        return response.get_response()
        

    