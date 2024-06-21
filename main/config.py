import os
import pathlib
import sys
from functools import lru_cache

class BaseConfig:
    BASEDIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    ENV: str = os.environ.get('ENV', 'default')
    DATABASE_URL: str = os.environ.get('DATABASE_URL')
    DATABASE_TRACK_MODIFICATIONS: bool = False
    DATABASE_CONNECT_DICT: dict = {}
    DATA_FILE: str =  f'{BASEDIR}/surfersapi/data/data.json'
    USER_PORT: int = os.environ.get('USER_PORT', 8080)
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")            # NEW
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0") 
    WILLY_API_KEY: str = os.environ.get("WILLY_API_KEY")


class ProductionConfig(BaseConfig):
    ENV = 'production'
    if BaseConfig.DATABASE_URL is None:
        DATABASE_URL = 'sqlite:///' + os.path.join(BaseConfig.BASEDIR, 'data.sqlite')

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'
    if BaseConfig.DATABASE_URL is None:
        DATABASE_URL = 'sqlite:///' + os.path.join(BaseConfig.BASEDIR, 'data.sqlite')

class TestingConfig(BaseConfig):
    TESTING = True
    ENV = 'testing'
    if BaseConfig.DATABASE_URL is None:
        DATABASE_URL = 'sqlite://'


@lru_cache()
def get_settings():
    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    _config = config[BaseConfig.ENV]
    if 'sqlite' in _config.DATABASE_URL:
         _config.DATABASE_CONNECT_DICT = {'check_same_thread': False}
    return _config

settings = get_settings()
