from src.models import Account
from src.utils.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AccountRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Account, session=session)
