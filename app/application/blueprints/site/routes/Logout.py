# Third party imports
from flask import redirect
from flask_login import logout_user, login_required

# Local application imports
from .ViewerInterface import ViewerInterface

class Logout(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/logout'
    
    @login_required
    def get(self):
        logout_user()
        return redirect('/login')