from flask import current_app

from flask.cli import FlaskGroup, with_appcontext
from flask_migrate import MigrateCommand

from reminder import create_app
from reminder.reminder_app.models import db


cli = FlaskGroup(create_app=create_app)
cli.add_command('db', MigrateCommand)


@cli.command('create_db')
@with_appcontext
def create_db():
    db.init_app(current_app)
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
