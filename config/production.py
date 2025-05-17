import os


class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
