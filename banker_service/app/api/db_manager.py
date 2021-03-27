import typing
from uuid import uuid4

from app.api.db import client, database

from .models import CreateClient, UpdateClient


async def get_all_client() -> typing.List[typing.Mapping]:
    query = client.select()
    return await database.fetch_all(query=query)


async def create_client(params: CreateClient) -> None:
    query = client.insert().values(iban=f"{uuid4()}", **params.dict())
    await database.execute(query)


async def update_client(iban: str, params: UpdateClient) -> str:
    query = (
        client.update()
        .returning(client.c.iban)
        .where(client.c.iban == iban)
        .values(**params.dict(exclude_none=True))
    )
    return await database.fetch_val(query=query)
