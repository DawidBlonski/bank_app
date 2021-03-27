from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, validator


class Client(BaseModel):
    first_name: str
    last_name: str
    pesel: str
    iban: str
    saldo: float


class CreateClient(BaseModel):
    first_name: str
    last_name: str
    pesel: str
    saldo: float

    @validator("pesel")
    def pesel_length(cls, v):
        if len(v) != 11:
            raise HTTPException(status_code=404, detail="Wrong PESEL")
        return v


class UpdateClient(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    pesel: Optional[str] = None
