from flask import Blueprint
from flask_restful import Api, Resource

from .routes import *


"""
Creating the Blueprint for the API.
"""
site_bp = Blueprint('site', __name__, template_folder='views')

"""
Creating the API for this specific blueprint.
"""
api = Api(site_bp)

"""
Adding all the necessary resources to the blueprint's api.
"""

"""
GET resources.
"""

for resource_class in ViewerInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)

print(AdminInterface.__subclasses__())
for resource_class in AdminInterface.__subclasses__():
    api.add_resource(resource_class, resource_class.base_route)

"""
POST resources.
"""