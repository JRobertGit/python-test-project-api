import os

basedir = os.path.abspath(os.path.dirname(__file__))

env_db = os.getenv("DATABASE_URL")
env_redis_url = os.getenv("REDIS_URL")
env_redis_password = os.getenv("REDIS_PASSWORD")


class Config:
    DEBUG = False


class DEV(Config):
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 50
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "database/github_users.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TEST(Config):
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 50
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "database/github_users.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


class PROD(Config):
    DEBUG = False
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = env_redis_url
    CACHE_REDIS_PASSWORD = env_redis_password
    CACHE_DEFAULT_TIMEOUT = 50
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = env_db


config = dict(dev=DEV, test=TEST, prod=PROD)
