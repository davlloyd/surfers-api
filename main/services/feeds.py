import feedparser
from main.data.models import *
from main.logger import logger

def getWeather():
    logger.info('RSS Weather Request')
    _json = []
    for _feedentry in Feed.get():
        _feeddata = readFeed(_feedentry.url, _feedentry.location)
        if _feeddata is not None:
            for _entry in _feeddata:
                _json.append(_entry)

    return _json
 
def readFeed(url, location):
    logger.info('RSS feed Read for: {}'.format(url))
    _headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.bom.gov.au',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
        }
    _feed = feedparser.parse(url, request_headers=_headers)
    logger.info(f"Feed Response: {_feed}")
    _response = None
    for _entry in _feed.entries:
        logger.info("RSS entry keys: {}".format(_entry.keys()))
        if _response is None:
            _response = []
        _feedinfo = {
            'title': _entry.title,
            'location': location,
            'published': _entry.published,
            'link': _entry.link
        }
        _response.append(_feedinfo)

    return _response


