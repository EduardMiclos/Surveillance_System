# Third party imports
from flask import render_template, make_response
from flask_login import login_required

# Local application imports
from .ViewerInterface import ViewerInterface


class Base(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/'
    
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        return make_response(
            render_template('base.html'), 
            200, headers
            )