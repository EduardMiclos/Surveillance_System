from flask import Flask

from controllers.Application import Application
from blueprints.api import api_bp
from blueprints.site import site_bp

"""
Creating the application.
"""
application = Application()

"""
Passing the blueprints to the current application.
"""
app = application.create_app(blueprints = [api_bp, site_bp], config_file="config.py")

if __name__ == "__main__":
    application.run(prod = False)
