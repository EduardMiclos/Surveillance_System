# Third party imports
from flask import render_template, make_response

# Local application imports
from .ViewerInterface import ViewerInterface


class Admin(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/admin'
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        return make_response(
            render_template('admin.html'), 
            200, headers
            )