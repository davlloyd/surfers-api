import json
import os
import sys
from unicodedata import category
from main.data.models import Feed
from . import models, SessionLocal, Base
from main.config import settings
from main.logger import logger



class DataManager():

    @staticmethod
    def initDB():
        logger.info(f'DB URI: {settings.DATABASE_URL}')
        logger.info('Create DB')
        
        _localfile = os.path.join(settings.BASEDIR, 'data.sqlite')
        if os.path.exists(_localfile):
            os.remove(_localfile)
        _session = SessionLocal()
        Base.metadata.create_all(_session.bind)
        _session.commit()
        DataManager.importData()

    @staticmethod
    def importData():
        logger.info('Importing data')
        _config = settings
        try:
            with open(_config.DATA_FILE, 'r') as f:
                table = json.loads(f.read())
        except:
            logger.error(f"Error reading data import file: {settings.DATA_FILE}")
        else:
            for _feed in table['feed']:
                Feed(name=_feed['name'],
                            location=_feed['location'],
                            category=_feed['category'],
                            url=_feed['url'])
            logger.info(f"Data import completed")
                
