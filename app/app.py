from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

if __name__ == 'app':
    from application.controllers.Application import Application
    from application.blueprints.api import api_bp
    from application.blueprints.site import site_bp
    from application.database.database import db
    from application.instance import Config
else:
    from .application.controllers.Application import Application
    from .application.blueprints.api import api_bp
    from .application.blueprints.site import site_bp
    from .application.database.database import db
    from .application.instance import Config

"""
Creating the application.
"""
application = Application()

"""
Passing the blueprints to the current application.
"""
app = application.create_app(blueprints = [api_bp, site_bp], config_object = Config)

if __name__ == 'app.app':
    print(213123213)
    application.kill_port()

"""
Initializing the database.
"""
db.init_app(app)

"""
Initializing the database migration engine.
"""
migrate = Migrate(app, db)