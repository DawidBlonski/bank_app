import typing
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import db_manager

from .models import Client, CreateClient, UpdateClient

banker = APIRouter()


@banker.get("/", response_model=List[Client], status_code=status.HTTP_200_OK)
async def clients() -> typing.List[typing.Mapping]:
    return await db_manager.get_all_client()


@banker.post("/client", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(params: dict = Depends(CreateClient)):
    return await db_manager.create_client(params)


@banker.patch("/client/{iban}", status_code=status.HTTP_200_OK)
async def update_client(iban: str, params: dict = Depends(UpdateClient)):
    if not params.dict(exclude_none=True):
        raise HTTPException(status_code=404, detail=f"No params")

    iban = await db_manager.update_client(iban, params)
    if not iban:
        raise HTTPException(
            status_code=404, detail=f"Account with given iban:{iban} not found"
        )

    response = {"iban": iban}
    return response
