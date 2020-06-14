import os,click
from flask.cli import with_appcontext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
app =Flask(__name__)
app.config['SECRET_KEY']='cc2a9fc6576e7419f2ff483f62325071'
app.config['SQLALCHEMY_DATABASE_URL']=os.environ.get('DATABASE_URL')
app.config['WHOOSH_BASE']='whoosh'
db=SQLAlchemy(app)
bcrypt=Bcrypt()
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASS')
mail=Mail(app)
from Login import routes

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()