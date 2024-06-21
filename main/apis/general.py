from fastapi import APIRouter
from main.config import settings
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/v1",
    tags=["general"],
    responses={404: {"description": "Not found"}},
)


class Health(BaseModel):
    health: str
    environment: str
    database: str


class Message(BaseModel):
    message: str 


# Status query page, can also be used for the benchmark testing 
@router.get(
    '/healthz', 
    response_model=Health,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "System information such as health status and db conenctions",
            "content": {
                "application/json": {
                    "example": {'health': 'ok','environment': 'development', 'database': 'sqlite://'}
                }
            },
        },
    },
    tags=["general"])
async def health():
    _status = {
        "health": "ok",
        "environment": settings.ENV,
        "database": settings.DATABASE_URL[:10]
    }
    return _status
