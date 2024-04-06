from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.app.schemas import *
from src.database import get_async_session
from src.models import *

from src.auth.auth import current_user, current_superuser

from typing import List

currency_router = APIRouter()
account_router = APIRouter()


@currency_router.get("/list", response_model=List[CurrencyRead])
async def currency_list(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Currency)
    result = await session.execute(stmt)
    return result.scalars().all()


@currency_router.post("/create")
async def create_currency(
        currency_in: CurrencyManage,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    stmt = insert(Currency).values(**currency_in.model_dump())
    try:
        await session.execute(stmt)
        await session.commit()
        return JSONResponse({"message": "Currency successfully created!"}, status_code=201)
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"Integrity error occurred.")


@currency_router.patch("/update/{currency_id}")
async def account_update(
        currency_id: int,
        currency_in_data: CurrencyManage,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    stmt = select(Currency).where(Currency.id == currency_id)
    result = await session.execute(stmt)
    currency = result.scalar_one()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    update_data = currency_in_data.model_dump(exclude_unset=True)
    stmt = update(Currency).where(Currency.id == currency_id).values(update_data)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Currency successfully updated!"}, status_code=200)


@currency_router.delete("/delete/{currency_id}")
async def currency_delete(
        currency_id: int,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Currency).where(Currency.id == currency_id)
    result = await session.execute(stmt)
    currency = result.scalar_one()
    if not currency:
        raise HTTPException(status_code=404, detail=f"Currency not found!")
    stmt = delete(Currency).where(Currency.id ==currency_id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Currency successfully deleted!"})


@account_router.get("/list", response_model=List[AccountRead])
async def account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account).where(Account.fk_user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()


@account_router.get("/{account_id}", response_model=AccountRead)
async def account(
        account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account).where(Account.fk_user_id == user.id, Account.id == account_id)
    result = await session.execute(stmt)
    return result.scalar_one()


@account_router.post("/create")
async def account_create(
        account_in: AccountCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    stmt = insert(Account).values(fk_user_id=user.id, **account_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Account successfully created!"}, status_code=201)


@account_router.patch("/update/{account_id}")
async def account_update(
        account_id: int,
        account_in_data: AccountUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    stmt = select(Account).where(Account.id == account_id)
    result = await session.execute(stmt)
    account = result.scalar_one()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    update_data = account_in_data.model_dump(exclude_unset=True)
    stmt = update(Account).where(Account.id == account_id).values(update_data)
    result = await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Account successfully updated!"}, status_code=200)


@account_router.delete("/delete/{account_id}")
async def account_delete(
        account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account).where(Account.id == account_id)
    result = await session.execute(stmt)
    account = result.scalar_one()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account not found!")
    stmt = delete(Account).where(Account.id ==account_id)
    response = await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Account successfully deleted!"})