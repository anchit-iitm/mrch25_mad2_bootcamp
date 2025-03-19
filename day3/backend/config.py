class default_config():
    DEBUG = False

class development_config(default_config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'

    SECRET_KEY = 'super-secret'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    SECURITY_TRACKABLE = True