import datetime
import enum

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import Schema, fields, pre_load, EXCLUDE

from reminder.reminder_app.utils import TwitterController

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.BigInteger, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    screen_name = db.Column(db.String, nullable=False)
    
    @property
    def mention_name(self):
        return f'@{self.screen_name}'
    
    def __repr__(self):
        return f'User ({self.name}, {self.screen_name}, {self.external_id})'


class StatusEnum(enum.Enum):
    PENDING = 0
    SUCCESS = 2
    ERROR = 3


class Reminder(db.Model):
    __tablename__ = 'reminder'
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("reminders", lazy="dynamic"))
    reminder_status_id = db.Column(db.BigInteger, nullable=False)
    reminder_request_status_id = db.Column(db.BigInteger, nullable=False)
    remind_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(StatusEnum), server_default=StatusEnum.PENDING.name)
    
    def remind(self):
        tc = TwitterController()
        
        # Check the status to remind exists
        status_permalink = tc.get_status_permalink(self.reminder_status_id)
        if status_permalink is None:
            self.status = StatusEnum.ERROR
        else:
            message = f'{self.author.mention_name} Wubbalubbadubdub! Here is your reminder'
            ok = tc.post_update(message, attachment_url=status_permalink)
            if ok:
                self.status = StatusEnum.SUCCESS 
            else:
                self.status = StatusEnum.ERROR
        
        db.session.commit()          
    
    def reply(self):
        tc = TwitterController()
        
        # Obtain status request
        request_status_permalink = tc.get_status_permalink(self.reminder_request_status_id)
        if request_status_permalink is None:
            self.status = StatusEnum.ERROR
        else:
            message = f'{self.author.mention_name} Copy that. I will remind you about this.'
            ok = tc.post_update(message, in_reply_to_status_id=self.reminder_request_status_id)
            if not ok:
                self.status = StatusEnum.ERROR
        
        db.session.commit()

## Schemas

class TweetCreateEventUser(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    screen_name = fields.Str(required=True)
    
    class Meta:
        unknown = EXCLUDE


class TweetCreateEvent(Schema):
    text = fields.Str(required=True)
    user = fields.Nested(TweetCreateEventUser, required=True)
    id = fields.Int(required=True)
    in_reply_to_status_id = fields.Int(required=True)
    
    class Meta:
        unknown = EXCLUDE


class ReminderEventSchema(Schema):
    tweet_create_events = fields.Nested(TweetCreateEvent, many=True, required=True)
    
    class Meta:
        unknown = EXCLUDE
