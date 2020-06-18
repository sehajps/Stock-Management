from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from Login.config import Config
from Login.commands import create_tables
from Login.models import user
#mysql://sql12349216:G3bCkSkCQ9@sql12.freemysqlhosting.net/sql12349216

db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail=Mail()


def create_app(config_class=Config):
    app =Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))
    from Login.users.routes import users
    from Login.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)

    app.cli.add_command(create_tables)
    return app
