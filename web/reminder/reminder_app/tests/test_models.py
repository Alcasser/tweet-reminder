from unittest.mock import patch
import datetime
import pytest

from reminder.reminder_app.models import Reminder, User, db, StatusEnum


@pytest.fixture
def test_reminder(test_db):
  user = User(external_id=1, name='test', screen_name='test')
  reminder = Reminder(
    author=user, remind_date=datetime.datetime.utcnow(),
    reminder_request_status_id=1,
    reminder_status_id=123)
  db.session.add(reminder)
  db.session.commit()
  
  return reminder


@patch('reminder.reminder_app.utils.TwitterController.post_update')
@patch('reminder.reminder_app.utils.TwitterController.get_status_permalink')
def test_can_remind_reminder(get_s_p, post_u, test_db, test_reminder):
  get_s_p.return_value = 123
  post_u.return_value = True
  test_reminder.remind()
  assert test_reminder.status == StatusEnum.SUCCESS


@patch('reminder.reminder_app.utils.TwitterController.post_update')
@patch('reminder.reminder_app.utils.TwitterController.get_status_permalink')
def test_remind_post_error(get_s_p, post_u, test_db, test_reminder):
  get_s_p.return_value = 123
  post_u.return_value = False
  test_reminder.remind()
  assert test_reminder.status == StatusEnum.ERROR


@patch('reminder.reminder_app.utils.TwitterController.post_update')
@patch('reminder.reminder_app.utils.TwitterController.get_status_permalink')
def test_remind_status_not_found_or_error(get_s_p, test_db, test_reminder):
  get_s_p.return_value = None
  test_reminder.remind()
  assert test_reminder.status == StatusEnum.ERROR
