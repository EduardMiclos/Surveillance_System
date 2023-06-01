from flask_login import login_required

from .....api.controllers.Response import Response
from ..AdminInterface import AdminInterface, admin_required
from ......database.models import User

class GetUser(AdminInterface):
    base_route = f'{AdminInterface.base_route}/user/get/<int:user_id>'
    
    @login_required
    @admin_required
    def get(self, user_id):
        user = User.query.get(user_id)
    
        response = Response()
        if user is None:
            response.set_not_found()
            response.set_message("User not found!")
            return response.get_response()
    
        # Serialize the user object excluding the password field
        serialized_user = {
            'id': user.id,
            'firstname': user.firstname,
            'secondname': user.secondname,
            'email': user.email,
            'phone': user.phone,
            'is_admin': user.is_admin
        }
        
        response.set_success()
        response.add_data("User", serialized_user)
        return response.get_response()
        