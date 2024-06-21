from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from main.logger import logger
from . import Base
from . import SessionLocal

# Feed table which contains the details foor RSS feeds
class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    category = Column(String(64), unique=False, index=True)
    location = Column(String(64), unique=False, index=True)
    url = Column(Text)

    def __init__(self, name: str, category: str, location: str, url: str):
        self.name = name
        self.url = url
        self.location = location
        self.category = category
        self.id = self.add()

    def __repr__(self):
        return self.id

    def add(self):
        _id = None
        _session = SessionLocal()
        _session.add(self)
        try:
            _session.commit()
            logger.info('Feed Record Added: %s', self.name)
        except IntegrityError:
            _session.rollback()

        if self.id is None:
            _resp = Feed.query.with_entities(Feed.id).filter(Feed.name == self.name).first()
            _id = _resp.id
        else:
            _id = self.id

        return _id

    @staticmethod
    def get():
        _session = SessionLocal()
        result = _session.query(Feed).all()
        return result





