from celery import current_app as celery_app

from reminder.reminder_app.models import Reminder



@celery_app.task()
def remind_reminder(reminder_id):
  reminder = Reminder.query.get(reminder_id)
  
  if reminder is None:
    raise Exception('Reminder was not found in the DB')
  
  reminder.remind()


@celery_app.task()
def reply_to_reminder_request(reminder_id):
  reminder = Reminder.query.get(reminder_id)
  
  if reminder is None:
    raise Exception('Reminder was not found in the DB')
  
  reminder.reply()