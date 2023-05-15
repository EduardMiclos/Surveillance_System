from flask import Flask
from flask_restful import Api, Resource

from .WSGI import WSGI

class Application:
    """

    Application

    Application class used for initializing and managing a Flask application.

    Args:
        port (str): The output port.
    Methods:
        __init__(port: str): Instantiates the class variables.
        run(debug: bool): Starts the Flask application.

    """
    def __init__(self, port: str = "8080"):
        self.port = port
    
    def create_app(self, blueprints: object, config_file: str = 'config.py'):
        """
        Creating the Flask application.
        """
        self.app = Flask(__name__, instance_relative_config = True)
        print(self.app.static_folder)
        """
        Setting up the configuration for the Flask application.
        """
        self.app.config.from_pyfile(config_file)

        """
        Adding all the blueprints to the application.
        """
        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)

        return self.app

    def run(self, debug: bool = False):
        """
        Creating and running the web server gateway interface.
        """
        self.wsgi = WSGI(port = self.port)
        self.wsgi.run()

        """
        Running the app
        """
        self.app.run(debug = debug, port = self.port)

            

        