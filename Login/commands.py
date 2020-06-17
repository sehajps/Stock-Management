import click
from flask.cli import with_appcontext

from Login import db
from Login.models import user,inventory,outgoing

@click.comman(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()