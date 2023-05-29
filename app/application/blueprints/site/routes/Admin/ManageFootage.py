# Third party imports
from flask import render_template, make_response, session
from flask_login import login_required, current_user

# Local application imports
from .AdminInterface import AdminInterface, admin_required

from .....database.models import Footage

class ManageFootage(AdminInterface):
    base_route = f'{AdminInterface.base_route}/manage-footage'
    
    @login_required
    @admin_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        footages = Footage.query.filter(Footage.date >= current_user.register_date).all()
        deleted_footage = session.pop('deleted_footage', default=False)
        
        return make_response(
            render_template('manage-footage.html',
                            current_user = current_user,
                            footages = footages,
                            deleted_footage = deleted_footage), 
            200, headers
            )
            