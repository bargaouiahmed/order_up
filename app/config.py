import os

class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Use the DATABASE_URL from .env
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppress the warning about track modifications
