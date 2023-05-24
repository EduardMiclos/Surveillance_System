# Third party imports
from flask import render_template, make_response, session


# Local application imports
from .AdminInterface import AdminInterface
from ..forms import RegisterForm

from ....database.models import User

class Admin(AdminInterface):
    base_route = AdminInterface.base_route
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        register_form = RegisterForm()
        users = User.query.all()
        
        added_new_user = session.pop('added_new_user', default=False)
        deleted_user = session.pop('deleted_user', default=False)
        pwd = session.pop('pwd', default=None)
        
        return make_response(
            render_template('admin.html', 
                            form = register_form,
                            added_new_user = added_new_user,
                            deleted_user = deleted_user,
                            users = users,
                            pwd = pwd), 
            200, headers
            )
            