# Third party imports
from flask import render_template, make_response

# Local application imports
from .ViewerInterface import ViewerInterface


class Profile(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/profile'
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        return make_response(
            render_template('profile.html'), 
            200, headers
            )