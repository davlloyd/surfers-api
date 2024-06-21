from enum import Enum, unique
from main.logger import logger
from . import web


"""
Get current weather observations for stated location. 
Location needs to be set by the BOM geohash value
"""
def observations(geohash):
    logger.info(f"reading current weather from BOM for location {geohash}")
    _observations = web.get(API_URL.OBSERVATIONS.set_location(geohash))
    _data = {}
    if _observations['data'] is not None:
        _data = {
            'temp': _observations['data']['temp'],
            'wind_speed': _observations['data']['wind']['speed_kilometre'],
            'wind_direction': _observations['data']['wind']['direction'],
            'rain_today': _observations['data']['rain_since_9am'],
            'humidity': _observations['data']['humidity']
        }
    return _data

"""
Do a BOM location search, can use full or partial string matchs including name, postcode, state
"""
def locationsearch(location):
    _search = location.replace(" ", "+").replace("_", "+").replace(",", "+")
    _location = web.get(API_URL.LOCATION_SEARCH.set_location(_search))
    _locations = []
    if len(_location['data']) > 0:
        for _entry in _location['data']:
            _data = {
                'geohash': _entry['geohash'][:6],
                'name': _entry['name'],
                'postcode': _entry['postcode'],
                'state': _entry['state']
                }
            _locations.append(_data)
    return _locations


@unique
class API_URL(Enum):
    LOCATION_SEARCH = 'https://api.weather.bom.gov.au/v1/locations?search={}'
    OBSERVATIONS = 'https://api.weather.bom.gov.au/v1/locations/{}/observations'
    FORECAST_DAILY = 'https://api.weather.bom.gov.au/v1/locations/{}/forecasts/daily'
    FORECAST_3HRLY = 'https://api.weather.bom.gov.au/v1/locations/{}/forecasts/3-hourly'

    def set_location(self, location):
        _url = self.value.format(location)
        return _url
