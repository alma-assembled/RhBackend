from decouple import config


class Config():
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:#4ayN23*@127.0.0.1/OPS'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:#4ayN23*@127.0.0.1/OPS'
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelopmentConfig
}

