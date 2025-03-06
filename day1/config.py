class default_config():
    DEBUG = False

class development_config(default_config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'