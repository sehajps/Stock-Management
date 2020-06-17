import click
from flask.cli import with_appcontext

from Login.extensions import db
from Login.models import user,inventory,outgoing

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()