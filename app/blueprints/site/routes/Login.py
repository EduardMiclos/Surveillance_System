# Third party imports
from flask import render_template, make_response

# Local application imports
from .ViewerInterface import ViewerInterface
from ....forms import *

class Login(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/login'
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        login_form = LoginForm()
        return make_response(
            render_template('login.html', form=login_form), 
            200, headers
            )