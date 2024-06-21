from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from main.services import feeds
from main.services.bom import observations, locationsearch
from .general import Message

router = APIRouter(
    prefix="/api/v1/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)


class Alert(BaseModel):
    title: str
    location: str
    published: str
    link: str


class Location(BaseModel):
    name: str
    geohash: str
    postcode: str
    state: str


class Observation(BaseModel):
    temp: int
    wind_speed: int
    wind_direction: str
    rain_today: int
    humidity: int


'''Get weather alerts'''
@router.get(
    '/alert',
    response_model=List[Alert],
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Get weather alerts notices",
            "content": {
                "application/json": {
                    "example": [{'title': 'Heavy wind alert NSW', 'location': 'New South Wales', 'published': 'some time details', 'link': 'http://somewhere.weather.com'}]
                }
            },
        },
    },
    tags=["weather"])
def alert():
    _alert = feeds.getWeather()
    return _alert
 

'''Get current observed weather from location identifier'''
@router.get(
    '/observation/{geotag}', 
    response_model=Observation,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Get current observed weather from location identifier",
            "content": {
                "application/json": {
                    "example": {'temp': 23, 'wind_speed': 10, 'wind_direction': 'NW', 'rain_today': 0, 'humidity': 63}
                }
            },
        },
    },
    tags=["weather"])
async def observation(geotag: str):
    if geotag:
        _observations = observations(geotag)
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return _observations


''' Get location information based on part of full location name and other values'''
@router.get(
    '/locations/{searchstring}', 
    response_model=List[Location],
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Find location information based on part of search value",
            "content": {
                "application/json": {
                    'example': [{'geohash': 'r6586vr', 'name': 'Mona Vale', 'postcode': '2103', 'state': 'NSW'}]
                }
            },
        },
    },
    tags=["weather"])
async def locations(searchstring):
    if searchstring:
        _locations = locationsearch(searchstring)
        return _locations
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

