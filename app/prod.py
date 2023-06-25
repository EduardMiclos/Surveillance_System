from application.controllers.WSGI import WSGI

wsgi = WSGI(port="8000")
wsgi.run()