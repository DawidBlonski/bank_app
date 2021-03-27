import typing

from sqlalchemy import select

from app.api.db import client, database


async def get_all_client() -> typing.List[typing.Mapping]:
    query = client.select()
    return await database.fetch_all(query=query)



async def client_exist(iban: str) -> bool:
    reciver_exist_query = select([client.c.iban]).where(client.c.iban == iban)
    if await database.fetch_val(query=reciver_exist_query):
        return True


async def client_saldo(iban: str) -> float:
    client_saldo_query = select([client.c.saldo]).where(client.c.iban == iban)
    return await database.fetch_val(query=client_saldo_query)


async def check_bill(iban: str, transation: float) -> float:
    saldo = await client_saldo(iban)
    if saldo > transation:
        return saldo


async def change_saldo(iban: str, saldo: float) -> str:
    query = (
        client.update()
        .returning(client.c.iban)
        .where(client.c.iban == iban)
        .values({"saldo": saldo})
    )

    return await database.fetch_val(query=query)


async def sent_tranfser(
    shipper_iban: str,
    reciver_iban: str,
    shipper_saldo: float,
    reciver_saldo: float,
    transation: float,
) -> typing.List[typing.Mapping]:
    reciver_transfer = await change_saldo(
        reciver_iban, saldo=reciver_saldo + transation
    )
    shipper_transfer = await change_saldo(
        shipper_iban, saldo=shipper_saldo - transation
    )

    if reciver_transfer and shipper_transfer:
        return True
