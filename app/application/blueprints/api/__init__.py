from flask import Blueprint
from flask_restful import Api, Resource

from .routes import *

"""
Creating the Blueprint for the API.
"""
api_bp = Blueprint('api', __name__, url_prefix='/api')

"""
Creating the API for this specific blueprint.
"""
api = Api(api_bp)


"""
Adding all resources resources.
"""

"""
Informers
"""
for resource_class in Informers.InformerInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)
    
    
"""
Providers
"""    
for resource_class in Providers.FootageProviderInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)
    
"""
Utils Providers
"""
for resource_class in UtilsProviders.ProviderInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)


"""
Receivers
"""
for resource_class in Receivers.ReceiverInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)

"""
Others
"""
for resource_class in Others.CameraInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)
    
# """
# Informers
# """
# api.add_resource(PreprocessInformer, '/get/info/preprocess')
# api.add_resource(UtilsInformer, '/get/info/utils')

# """
# File providers
# """
# api.add_resource(BackgrSupprProvider, f'/get/utils/{BackgrSupprProvider.base_route}')
# api.add_resource(CenterCropProvider, f'/get/utils/{CenterCropProvider.base_route}')
# api.add_resource(FrameDifferenceProvider, f'/get/utils/{FrameDifferenceProvider.base_route}')
# api.add_resource(NormalizationProvider, f'/get/utils/{NormalizationProvider.base_route}')

# print(Resource.__subclasses__()[0].__bases__);


# """
# POST resources.
# """
# api.add_resource(FrameReceiver, '/send/frames')