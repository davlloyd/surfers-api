from fastapi import APIRouter
from pydantic import BaseModel
from .general import Message

router = APIRouter(
    prefix="/api/v1/surf",
    tags=["surf"],
    responses={404: {"description": "Not found"}},
)


swell_example = {
        'height': 6,
        'interval': 11,
        'direction': 'SE'
    }


water_example = {'temperature': 22}


class Swell(BaseModel):
    height: int
    interval: int
    direction: str

class Water(BaseModel):
    temperature: int


@router.get(
    '/swell/{location_id}', 
    response_model=Swell,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Get information on the locations current surf conditions such as wave height",
            "content": {
                "application/json": {
                    "example": {'height': 6,'interval': 11,'direction': 'SE'}
                }
            },
        },
    },
    tags=['surf'])
async def swell(location_id: str):
    if location_id:
        '''Get swell forecast from location identifier'''
        return swell_example


@router.get(
    '/water/{location_id}', 
    response_model=Water,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Get info on the locations water condition such as temnperatue.",
            "content": {
                "application/json": {
                    "example": {'temperature': 26}
                }
            },
        },
    },
    tags=['surf'])
async def water(location_id):
    '''Get water forecast from location identifier'''
    return water_example

