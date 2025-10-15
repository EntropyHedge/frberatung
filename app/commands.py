import click
from flask.cli import with_appcontext
from app.extensions import db


@click.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')


@click.command()
@with_appcontext
def drop_db():
    """Drop all database tables."""
    if click.confirm('This will delete all data. Are you sure?'):
        db.drop_all()
        click.echo('Dropped all database tables.')


@click.command()
@with_appcontext
def reset_db():
    """Reset the database (drop and recreate)."""
    if click.confirm('This will delete all data and recreate tables. Are you sure?'):
        db.drop_all()
        db.create_all()
        click.echo('Database reset complete.')


def register_commands(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(init_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(reset_db)