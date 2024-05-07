from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category
from src.utils.repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Category, session=session)
