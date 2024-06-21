from fastapi import FastAPI
#from .celery_utils import create_celery
from .logger import logger
from .data.utilities import DataManager


tags_metadata = [
    {
        "name": "surf",
        "description": "Surf report data",
    },
    {
        "name": "weather",
        "description": "Weather related data",
    },
    {
        "name": "general",
        "description": "General system level APIs",
    },
]


def create_app() -> FastAPI:
    logger.info(f'Initialising App Factory')
    app = FastAPI(
        debug=True, title="Surfers Lookout APIs",
        description="REST APIs for surf and weather forecasts",
        version="0.1.0",
        openapi_url="/api/v1/api-docs",
        openapi_tags=tags_metadata
    ) 

    #logger.info(f'Create celery instance')
    #app.celery_app = create_celery()

    logger.info(f'Setup database')
    DataManager.initDB()

    logger.info(f'Create routers')

    from .apis.surf import router as surf_router
    app.include_router(surf_router)

    from .apis.weather import router as weather_router
    app.include_router(weather_router)

    from .apis.general import router as general_router
    app.include_router(general_router)

    return app
