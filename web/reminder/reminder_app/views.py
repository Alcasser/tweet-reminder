import hmac
import hashlib
import base64
import datetime
from dateparser.search import search_dates

from flask import request, current_app
from flask_restful import reqparse, Api, Resource
from marshmallow import ValidationError

from reminder.reminder_app.models import User, Reminder, ReminderEventSchema, db
from reminder.reminder_app.tasks import remind_reminder, reply_to_reminder_request


reminder_api = Api()


class HelloWorld(Resource):
    def get(self):
        print(request.args)
        return {'message': 'Hello World 1'}


class WebhookEvent(Resource):
    def get(self):
        """
        This view is used by Twitter to validate the registered endpoint
        """
        consumer_secret = bytes(current_app.config.get('TWITTER_CONSUMER_SECRET'), 'latin-1')
        msg = bytes(request.args.get('crc_token'), 'latin-1')
        sha256_hash_digest = hmac.new(
            consumer_secret, msg=msg, digestmod=hashlib.sha256).digest()
        
        # construct response data with base64 encoded hash
        return {
            'response_token': 'sha256=' + base64.b64encode(
                sha256_hash_digest).decode('utf-8')
        }
    
    #TODO: Move logic to serializer or use case controller
    def post(self):
        request_data = request.get_json()
        
        # Validate and deserialize event input
        try:
            data = ReminderEventSchema().load(request_data)
        except ValidationError as err:
            return err.messages, 400
        event_data = data.get('tweet_create_events')[0]
        
        # Get or create reminder author (A given user will perform consecutive reminders)
        user_data = event_data.get('user')
        author = User.query.filter_by(external_id=user_data.get('id')).first()
        if author is None:
            author = User(
                external_id=user_data.get('id'),
                name=user_data.get('name'),
                screen_name=user_data.get('screen_name'))
            db.session.add(author)
        
        # Parse reminder date with dateparser
        obtained_dates = search_dates(
            event_data.get('text'), settings={'PREFER_DATES_FROM': 'future'})
        if obtained_dates is None or obtained_dates[0][1] < datetime.datetime.now():
            raise Exception('Could not parse remind date from text: {}'.format(
                event_data.get('text')))
        
        # Create reminder
        remind_date = obtained_dates[0][1]
        reminder = Reminder(
            author=author, remind_date=remind_date,
            reminder_request_status_id=event_data.get('id'),
            reminder_status_id=event_data.get('in_reply_to_status_id'))
        db.session.add(reminder)
        db.session.commit()
        
        # Schedule reminder
        remind_reminder.apply_async(
            (reminder.id,), eta=reminder.remind_date)
        reply_to_reminder_request.apply_async((reminder.id,))
        
        return None, 201


reminder_api.add_resource(HelloWorld, '/')
reminder_api.add_resource(WebhookEvent, '/webhook/twitter')
