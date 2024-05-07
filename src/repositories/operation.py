from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.models import Operation, Category, Account
from src.utils.repository import BaseRepository


class OperationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Operation, session=session)

    async def add(self, values: dict, user_id: int = None):
        category_id = values.get("fk_category_id")
        account_id = values.get("fk_account_id")
        stmt = select(Category).where(Category.fk_user_id == user_id, Category.id == category_id)
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        stmt = select(Account).where(Account.fk_user_id == user_id, Account.id == account_id)
        result = await self._session.execute(stmt)
        account = result.scalar_one_or_none()
        if category and account:
            stmt = self.construct_add_stmt(values=values, user_id=user_id)
            result = await self._session.execute(stmt)
            await self._session.commit()
            return result.scalar_one()

        if not category:
            return JSONResponse(status_code=400, content={"message": "You don't have category with such id"})
        if not account:
            return JSONResponse(status_code=400, content={"message": "You don't have account with such id"})
