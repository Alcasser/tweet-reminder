import boto3
import twitter

from flask import current_app


def read_s3_contents(bucket_name, key):
  session = boto3.Session(
    aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=current_app.config.get('AWS_ACCESS_SECRET'))
  s3 = session.resource('s3')
  response = s3.Object(bucket_name, key).get()
  return response['Body'].read()


class TwitterController():
  
  def __init__(self):
    self.api = twitter.Api(
      consumer_key=current_app.config.get('TWITTER_CONSUMER_KEY'),
      consumer_secret=current_app.config.get('TWITTER_CONSUMER_SECRET'),
      access_token_key=current_app.config.get('TWITTER_ACCESS_TOKEN'),
      access_token_secret=current_app.config.get('TWITTER_ACCESS_SECRET'))
    
    assert self.api.VerifyCredentials() is not None
  
  def get_status_permalink(self, status_id):
    try: 
      statuses = self.api.GetStatuses([status_id])
    except Exception as e:
      return None
    
    if len(statuses) != 1:
      return None
    
    status = statuses[0]
    if status.user and status.user.screen_name:
      return f'https://twitter.com/{status.user.screen_name}/status/{status_id}'
    
    return None
  
  def post_update(self, message, **kwargs):
    try:
      self.api.PostUpdate(message, **kwargs)
      return True
    except Exception as e:
      return False
