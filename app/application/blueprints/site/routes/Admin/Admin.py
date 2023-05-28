# Third party imports
from flask import render_template, make_response, session
from flask_login import login_required, current_user

# Local application imports
from .AdminInterface import AdminInterface, admin_required
from ...forms import RegisterForm, UserEditForm, CameraEditForm

from .....database.models import User, Camera, Footage

class Admin(AdminInterface):
    base_route = AdminInterface.base_route
    
    @login_required
    @admin_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
       
        register_form = RegisterForm()
        useredit_form = UserEditForm()
        cameraedit_form = CameraEditForm()
        users = User.query.all()
        cameras = Camera.query.all()
        footages = Footage.query.filter(Footage.date >= current_user.register_date).all()
        
        added_new_user = session.pop('added_new_user', default=False)
        edited_user = session.pop('edited_user', default=False)
        deleted_user = session.pop('deleted_user', default=False)
        deleted_footage = session.pop('deleted_footage', default=False)
        deleted_camera = session.pop('deleted_camera', default=False)
        edited_camera = session.pop('edited_camera', default=False)
        pwd = session.pop('pwd', default=None)
        
        return make_response(
            render_template('admin.html', 
                            form = register_form,
                            useredit_form = useredit_form,
                            cameraedit_form = cameraedit_form,
                            added_new_user = added_new_user,
                            edited_user = edited_user,
                            deleted_user = deleted_user,
                            deleted_footage = deleted_footage,
                            deleted_camera = deleted_camera,
                            users = users,
                            cameras = cameras,
                            footages = footages,
                            edited_camera = edited_camera,
                            pwd = pwd), 
            200, headers
            )
            