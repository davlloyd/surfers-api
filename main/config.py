import os
import pathlib
import sys, json
from functools import lru_cache
from pyservicebinding import binding


class BaseConfig:
    BASEDIR = os.getcwd()
    ENV: str = os.environ.get('ENV', 'default')
    DATABASE_CONNECT_DICT: dict = {}
    USER_PORT: int = os.environ.get('USER_PORT', 8080)
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")            # NEW
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0") 
    WILLY_API_KEY: str = os.environ.get("WILLY_API_KEY")

    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('DB_TRACK_MODIFICATIONS') or False
    DATA_FILE = os.environ.get('DATA_FILE') or f'{BASEDIR}/main/data/data.json'

    if 'VCAP_SERVICES' in os.environ:
        _vcap_services = json.loads(os.environ['VCAP_SERVICES'])
        if len(_vcap_services) > 0 and 'p.mysql' in _vcap_services[0]:
            _mysql_srv = _vcap_services['p.mysql'][0]
            _cred = _mysql_srv['credentials']
            if _cred:
                DATABASE_URL = f"mysql+pymysql://{_cred['username']}:{_cred['password']}@{_cred['hostname']}:{_cred['port']}/{_cred['name']}"
            else:
                print("VCAP_SERVICES present but no db binding detected")
        else:
            DATABASE_URL = 'sqlite:///' + os.path.join(BASEDIR, 'data.sqlite')
    else:
        try:
            _sb = binding.ServiceBinding()
            _db = _sb.bindings('mysql')
        except binding.ServiceBindingRootMissingError:
            print("Environment Variable SERVICE_BINDING_ROOT not set")
        else:
            if _db:
                DATABASE_URL = f"mysql+pymysql://{_db[0]['username']}:{_db[0]['password']}@{_db[0]['host']}:{_db[0]['port']}/{_db[0]['database']}"
                print(f'Binding DB URI: {DATABASE_URL}')
            else:
                print('MySQL Binding not found, reverting to sqlite local store')


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
