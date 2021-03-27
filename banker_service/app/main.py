from fastapi import FastAPI

from app.api.api import banker
from app.api.db import database

app = FastAPI(openapi_url="/api/v1/banker/openapi.json", docs_url="/api/v1/banker/docs")


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


app.include_router(banker, prefix="/api/v1/banker", tags=["banker"])
