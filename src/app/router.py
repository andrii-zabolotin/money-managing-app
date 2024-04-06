from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas import *
from src.database import get_async_session
from src.models import *

from src.auth.auth import current_user

from typing import List

currency_router = APIRouter()
account_router = APIRouter()


@currency_router.get("/list", response_model=List[CurrencyRead])
async def currency_list(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Currency)
    result = await session.execute(stmt)
    return result.fetchall()


@account_router.get("/list", response_model=List[AccountRead])
async def account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account)
    result = await session.execute(stmt)
    return result.fetchall()


@account_router.post("/create")
async def account_create(
        account_in: AccountCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> None:
    stmt = insert(Account).values(fk_user_id=user.id, **account_in.model_dump())
    await session.execute(stmt)
