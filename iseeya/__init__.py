from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from iseeya.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

from flask_socketio import send, emit


from flask_socketio import SocketIO

from flask_socketio import emit

io = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    io.init_app(app)
    socketio = SocketIO(app)

    from iseeya.users.routes import users
    from iseeya.pages.admin_routes import admin
    from iseeya.pages.routes import pages
    from iseeya.main.routes import main
    from iseeya.iwanna.routes import iwanna
    from iseeya.errors.handlers import errors
    from iseeya.streamer.routes import streamer
    app.register_blueprint(users)
    app.register_blueprint(admin)
    app.register_blueprint(pages)
    app.register_blueprint(iwanna)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    streamer.init_io(socketio)

    return socketio, app


