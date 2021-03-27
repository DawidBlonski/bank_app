from pydantic import BaseModel


class Client(BaseModel):
    first_name: str
    last_name: str
    pesel: str
    iban: str
    saldo: float
