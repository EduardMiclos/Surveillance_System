from flask import Flask

from controllers.Application import Application
from blueprints.api import api_bp
from blueprints.site import site_bp
from database.database import db
from instance import Config

"""
Creating the application.
"""
application = Application()

"""
Passing the blueprints to the current application.
"""
app = application.create_app(blueprints = [api_bp, site_bp], config = Config)

"""
Initializing the database.
"""
db.init_app(app)

if __name__ == "__main__":
    application.run(prod = False)
