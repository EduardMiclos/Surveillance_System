import subprocess
from time import sleep

from flask import Flask
from flask_restful import Api, Resource
from werkzeug.middleware.profiler import ProfilerMiddleware

PORT_KILL_SLEEP_TIME_SEC = 3

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
    
    def create_app(self, blueprints: object, config_object: object, profiling: bool = False):
        """
        Creating the Flask application.
        """
        self.app = Flask(__name__, instance_relative_config = True)
        
        if profiling:
            """
            Initializing the Profiler.
            """
            self.app.wsgi_app = ProfilerMiddleware(self.app.wsgi_app, profile_dir='/home/miclosedi/Surveillance_System/profile_dir')
            
        """
        Setting up the configuration for the Flask application.
        """
        self.app.config.from_object(config_object)

        """
        Adding all the blueprints to the application.
        """
        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)

        return self.app

    def kill_port(self):
        """
        If there's any process running on the specified port, kill it.
        """
        try:
            subprocess.check_output(['fuser',
                            '-k',
                            f'{self.port}/tcp'], shell = True, stderr=subprocess.STDOUT)
        except:
            pass
        
        sleep(PORT_KILL_SLEEP_TIME_SEC)
        return self.app
         
    def run(self):
        self.app.run(debug = False, port = self.port)
            

        