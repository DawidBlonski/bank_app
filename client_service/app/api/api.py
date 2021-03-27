from fastapi import APIRouter, HTTPException, status

from app.api import db_manager

client = APIRouter()


async def client_exist(iban: str, role: str) -> None:
    if not await db_manager.client_exist(iban):
        raise HTTPException(
            status_code=404,
            detail=f"{role} account with given iban:{iban} not found",
        )


async def check_bill(iban: str, transaction: float) -> None:
    if not await db_manager.check_bill(iban, transaction):
        raise HTTPException(status_code=404, detail=f"Insufficient funds")


@client.patch("/{shipper_iban}/tranfer", status_code=status.HTTP_200_OK)
async def tranfser(shipper_iban: str, reciver_iban: str, transaction: float):
    shiper_saldo = await db_manager.client_saldo(shipper_iban)
    reciver_saldo = await db_manager.client_saldo(reciver_iban)
    await client_exist(shipper_iban, "Shipper")
    await client_exist(reciver_iban, "Reciver")
    await check_bill(shipper_iban,transaction)
    await check_bill(reciver_iban,transaction)
    await db_manager.sent_tranfser(
        shipper_iban, reciver_iban, shiper_saldo, reciver_saldo, transaction
    )


@client.patch("/{iban}/payout", status_code=status.HTTP_200_OK)
async def payout(iban: str, transaction: float):
    await client_exist(iban, "Customer")
    await check_bill(iban, transaction)
    saldo = await db_manager.client_saldo(iban)
    await db_manager.change_saldo(iban, saldo - transaction)


@client.patch("/{iban}/deposit", status_code=status.HTTP_200_OK)
async def deposit(iban: str, transaction: float):
    await client_exist(iban, "Customer")
    saldo = await db_manager.client_saldo(iban)
    await db_manager.change_saldo(iban, saldo + transaction)
