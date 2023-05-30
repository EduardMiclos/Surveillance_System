# Third party imports
from flask import render_template, make_response
from flask_login import login_required

from .ProfileInterface import ProfileInterface
from ...forms import ChangePasswordForm

class ChangePassword(ProfileInterface):
    base_route = f'{ProfileInterface.base_route}/change-password'
    
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        change_password_form = ChangePasswordForm()
        
        return make_response(
            render_template('change-password.html',
                            form = change_password_form), 
            200, headers
        )