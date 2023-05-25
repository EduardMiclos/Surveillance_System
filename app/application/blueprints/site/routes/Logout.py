# Third party imports
from flask import redirect
from flask_login import logout_user

# Local application imports
from .ViewerInterface import ViewerInterface

class Logout(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/logout'
    
    def get(self):
        logout_user()
        return redirect('/')