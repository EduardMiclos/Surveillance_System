# Third party imports
from flask import render_template, make_response
from flask_login import login_required

# Local application imports
from .ViewerInterface import ViewerInterface
from ....database.models import Footage

class History(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/history'
    
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        footages = Footage.query.all()
        
        return make_response(
            render_template('history.html', 
                            footages = footages), 
            200, headers
            )