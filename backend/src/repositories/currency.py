from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal
from src.models import Currency
from src.utils.repository import BaseRepository


class CurrencyRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Currency, session=session)
