from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas import *
from src.database import get_async_session
from src.models import *

from typing import List

currency_router = APIRouter()


@currency_router.get("/list", response_model=List[CurrencyRead])
async def currency_list(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Currency)
    result = await session.execute(stmt)
    return result.fetchall()
