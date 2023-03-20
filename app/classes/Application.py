from flask import Flask
from flask_restful import Api, Resource
import WSGI

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
    def __init__(port: str = "8080"):
        self.port = port
    
    def run(self, resources: object, debug: bool = False):
        """
        Creating and running the web server gateway interface.
        """
        self.wsgi = WSGI(port = self.port)
        self.wsgi.run()

        """
        Creating the Flask application + restful API.
        """
        self.app = Flask(__name__)
        self.api = Api(app)

        """
        Iterating through all the resources (classes)
        and adding them to the REST API object.
        """
        for resource in resources:
            self.api.add_resource(resource, resource.getUrl())

        """
        Running the app
        """
        self.app.run(debug)

            

        