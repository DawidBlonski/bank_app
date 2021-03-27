import os

from databases import Database
from sqlalchemy import (FLOAT, Column, Integer, MetaData, String, Table,
                        create_engine)

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
metadata = MetaData()

client = Table(
    "client",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(100)),
    Column("pesel", String(11)),
    Column("iban", String(36), unique=True),
    Column("saldo", FLOAT),
)

engine = create_engine(DATABASE_URL)
