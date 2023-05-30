# Third party imports
from flask import render_template, make_response
from flask_login import login_required

from .ProfileInterface import ProfileInterface

class Profile(ProfileInterface):
    base_route = ProfileInterface.base_route
    
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        return make_response(
            render_template('profile.html'), 
            200, headers
        )