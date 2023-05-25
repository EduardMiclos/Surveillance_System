from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

if __name__ == 'app':
    from application.controllers.Application import Application
    from application.blueprints.api import api_bp
    from application.blueprints.site import site_bp
    from application.database.database import db
    from application.instance import Config
    from application.database.models import User
else:
    from .application.controllers.Application import Application
    from .application.blueprints.api import api_bp
    from .application.blueprints.site import site_bp
    from .application.database.database import db
    from .application.instance import Config
    from .application.database.models import User

"""
Creating the application.
"""
application = Application()

"""
Passing the blueprints to the current application.
"""
app = application.create_app(blueprints = [api_bp, site_bp], config_object = Config)

if __name__ == 'app.app':
    application.kill_port()

"""
Initializing the database.
"""
db.init_app(app)

"""
Initializing the database migration engine.
"""
migrate = Migrate(app, db)

"""
Initializing the login manager.
"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'site.login'

"""
Because Flask-Login knows nothing about databases, 
it needs the application's help in loading a user.
"""
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

