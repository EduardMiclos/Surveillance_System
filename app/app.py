from flask import Flask

from controllers.Application import Application
from blueprints.api import api_bp

"""
Creating the application.
"""
application = Application(port = "8080")

"""
Passing the blueprints to the current application.
"""
app = application.create_app(blueprints = [api_bp])

if __name__ == "__main__":
    application.run()
