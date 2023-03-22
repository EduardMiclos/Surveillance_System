import subprocess

class WSGI:
    """

    Web Server Gateway Interface

    Uses gunicorn to initialize a gateway interface to a specified port. This
    class makes use of the subprocess library for invoking subprocesses and
    runs a command described by arguments.

    Args:
        app_module (str): The name of the Python module that contains the
                          Flask application.
        application_instance (str):The variable name of the Flask 
                          application instance within that module.
        port (str): The output port.

    Methods:
        __init__(app_module: str, application_instance: str, port: str): 
                          Instantiates the class variables.
        run(): Performs a try-catch operation and tries 
                          to run the command using subprocess.

    """
    def __init__(self, app_module: str = "app", application_instance: str = "app", port: str = "8080"):
        self.app_module = app_module
        self.application_instance = application_instance
        self.port = port
    
    def run(self):
        try:
            subprocess.run(['gunicorn', 
                            f'{self.app_module}:{self.application_instance}', 
                            '--bind',
                            f'0.0.0.0:{self.port}'], check = True)
        except subprocess.CalledProcessError as err:
            print(f'ERROR: Occured when trying to initialize a gateway interface.\nError code: {err.returncode}\nError output: {err.output}')
            

        