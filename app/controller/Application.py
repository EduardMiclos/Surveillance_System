from flask import Flask
from flask_restful import Api, Resource

if __name__ == "controller.Application":
    from controller.WSGI import WSGI
else:
    from WSGI import WSGI

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
    
    def create_app(self, resources: object):
        """
        Creating the Flask application + restful API.
        """
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.init_app(self.app)

        """
        Iterating through all the resources (classes)
        and adding them to the REST API object.
        """
        for resource in resources:
            self.api.add_resource(resource, resource.route)

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

        self.app.run(debug = debug)

            

        