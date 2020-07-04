import pytest

from reminder import create_app


# Pytest-Flask uses this fixture (app)
@pytest.fixture
def app():
  app = create_app(use_test_config=True)
  return app


@pytest.fixture()
def test_db(app):
  from reminder.reminder_app.models import db
  db.init_app(app)
  db.drop_all()
  db.create_all()
  db.session.commit()

  yield db  # this is where the testing happens!
  
  db.session.close()
  db.drop_all()
  db.session.commit()
