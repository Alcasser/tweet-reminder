import os


class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AWS
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_ACCESS_SECRET = os.getenv('AWS_ACCESS_SECRET')
    
    # Twitter
    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
    
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    

class Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4 # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    TESTING = True
