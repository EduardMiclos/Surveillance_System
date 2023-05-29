from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sse import sse
from flask_jwt_extended import JWTManager
from redis import StrictRedis, exceptions


if __name__ == 'app':
    from application.controllers.Application import Application
    from application.blueprints.api import api_bp
    from application.blueprints.site import site_bp
    from application.database.database import db
    from application.instance import Config
    from application.database.models import User
else:
    from .application.controllers.Application import Application
    from .application.blueprints.api import api_bp
    from .application.blueprints.site import site_bp
    from .application.database.database import db
    from .application.instance import Config
    from .application.database.models import User

"""
Creating the application.
"""
application = Application()

"""
Passing the blueprints to the current application.
"""
sse.url_prefix = '/stream'
app = application.create_app(blueprints = [api_bp, site_bp, sse], config_object = Config)

if __name__ == 'app.app':
    application.kill_port()

"""
Initializing the database.
"""
db.init_app(app)


@app.route('/send')
def send_message():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"


"""
Initializing the database migration engine.
"""
migrate = Migrate(app, db)

"""
Initializing the login manager.
"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'site.login'

"""
Because Flask-Login knows nothing about databases, 
it needs the application's help in loading a user.
"""
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


"""
Checking the connection to Redis cache.
"""
redis_client = StrictRedis.from_url(app.config['REDIS_URL'])

try:
    redis_client.ping()
    print('[CONNECTIVITY SUCCESS] Redis connection is working!')
except exceptions.ConnectionError as e:
    print(f'[CONNECTIVITY FAIL] Error connecting to Redis: {str(e)}')
    exit(1)

"""
Initializing the JWT.
"""
jwt = JWTManager(app)