# Third party imports
from flask import render_template, make_response

# Local application imports
from .ViewerInterface import ViewerInterface


class History(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/history'
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        return make_response(
            render_template('history.html'), 
            200, headers
            )