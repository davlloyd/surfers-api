import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from main.logger import logger

def get(url) -> json:
    logger.info(f"Reading API Get: {url}")

    try:
        with urlopen(url) as _response:
            _data = _response.read()
            _item = json.loads(_data)
            return _item
    except HTTPError as e:
        logger.error(f'Error code: {e.code}')
    except URLError as e:
        logger.error(f'URL Error: {e.reason}')

    return {}        

