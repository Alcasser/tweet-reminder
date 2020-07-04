import json
import datetime

from flask import url_for

from reminder.reminder_app.models import db, User, Reminder, StatusEnum
from reminder.reminder_app.utils import read_s3_contents



def test_can_create_reminder_from_mention(client, test_db):
  # Mention json containing a reminder for tomorrow
  event_data = read_s3_contents('tweet-reminder-api', 'mention2.json')
  event = json.loads(event_data)
  
  # Post user first reminder
  response = client.post(url_for('webhookevent'), json=event)
  assert response.status_code == 201
  
  mention_external_id = event.get('tweet_create_events')[0].get('user').get('id')
  user_reminder = Reminder.query.join(User).filter(User.external_id == mention_external_id).first()
  
  # Test parsed remind date is correct and contains valid tweet to remind id
  assert user_reminder is not None
  today = datetime.datetime.today()
  assert user_reminder.remind_date.day == today.day + 1
  assert user_reminder.remind_date.month == today.month
  assert user_reminder.remind_date.year == today.year
  assert user_reminder.status == StatusEnum.PENDING
  assert user_reminder.reminder_status_id is not None
  assert user_reminder.reminder_request_status_id is not None
  