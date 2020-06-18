from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_mail import Mail
login_manager = LoginManager()
db = SQLAlchemy()
bcrypt=Bcrypt()
mail=Mail()