from flask import Flask

from controllers.Application import Application
from blueprints.api import api_bp

application = Application()
app = application.create_app(blueprints = [api_bp])

if __name__ == "__main__":
    print(app.blueprints)
    application.run()
