from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal
from src.models import SavingsAccount, Account
from src.utils.repository import BaseRepository


class SavingsAccountRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=SavingsAccount, session=session)
        self.join_model = Account

    def construct_get_stmt(self, id: int, user_id: int = None) -> Select:
        stmt = select(self._model).join(self.join_model).filter(self.join_model.fk_user_id == user_id).where(self._model.id == id)
        return stmt

    def construct_list_stmt(self, user_id: int = None) -> Select:
        stmt = select(self._model).join(self.join_model).filter(self.join_model.fk_user_id == user_id)
        return stmt
