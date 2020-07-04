import os

from flask import Flask
from celery import Celery


def create_app(use_test_config=False):
  app = Flask(__name__)
  
  if use_test_config:
    app.config.from_object('reminder.config.TestConfig')
  else:
    app.config.from_object('reminder.config.Config')
  
  from reminder.reminder_app.models import db, migrate
  db.init_app(app)
  migrate.init_app(app, db)
  
  from reminder.reminder_app.views import reminder_api
  reminder_api.init_app(app)
  
  return app


def make_celery(app):
  with app.app_context():
    celery = Celery(
      app.import_name,
      broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
      def __call__(self, *args, **kwargs):
        with app.app_context():
          return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery
