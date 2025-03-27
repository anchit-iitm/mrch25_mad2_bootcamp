class default_config():
    DEBUG = False

class development_config(default_config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'

    SECRET_KEY = 'super-secret'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    SECURITY_TRACKABLE = True

    CACHE_TYPE = 'RedisCache'
    CACHE_KEY_PREFIX = 'flask_cache_'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 60

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'admin@a.com'

class celery_config():
    broker_url = 'redis://localhost:6379/1'
    result_backend = 'redis://localhost:6379/2'
    timezone = 'Asia/Kolkata'