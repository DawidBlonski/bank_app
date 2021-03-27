from fastapi import FastAPI

from app.api.api import client
from app.api.db import database

app = FastAPI(openapi_url="/api/v1/client/openapi.json", docs_url="/api/v1/client/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(client, prefix="/api/v1/client", tags=["clients"])
