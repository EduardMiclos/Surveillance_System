# Third party imports
from flask import render_template, make_response

# Local application imports
from .ViewerInterface import ViewerInterface


class Base(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/'
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        return make_response(
            render_template('base.html'), 
            200, headers
            )