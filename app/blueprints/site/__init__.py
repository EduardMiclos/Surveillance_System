from flask import Blueprint
from flask_restful import Api

from .routes.Login import Login


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
api.add_resource(Login, '/login')


"""
POST resources.
"""