from fastapi import HTTPException
from sqlalchemy import Select, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.models import SubCategory, Category
from src.utils.repository import BaseRepository


class SubCategoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=SubCategory, session=session)
        self.join_model = Category

    def construct_list_stmt(self, user_id: int = None) -> Select:
        stmt = select(self._model).join(self.join_model).filter(self.join_model.fk_user_id == user_id)
        return stmt

    def construct_get_stmt(self, id: int, user_id: int = None) -> Select:
        stmt = select(self._model).join(self.join_model).filter(self.join_model.fk_user_id == user_id).where(
            self._model.id == id)
        return stmt

    async def add(self, values: dict, user_id: int = None):
        category_id = values.get("fk_category_id")
        stmt = select(self.join_model).where(self.join_model.fk_user_id == user_id, self.join_model.id == category_id)
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        if category:
            stmt = self.construct_add_stmt(values=values)
            result = await self._session.execute(stmt)
            await self._session.commit()
            return result.scalar_one()

        return JSONResponse(status_code=400, content={"message": "You don't have category with such id"})

    def construct_delete_stmt(self, id: int, user_id: int = None):
        stmt = delete(self._model).where(self._model.id == id)
        return stmt

    async def delete(self, model_object_id: int, user_id: int = None):
        stmt = select(self._model).join(self.join_model).filter(self.join_model.fk_user_id == user_id).where(
            self._model.id == model_object_id)
        response = await self._session.execute(stmt)
        sub_category = response.scalar_one_or_none()
        if not sub_category:
            raise HTTPException(status_code=404, detail=f"{self._model.__name__} with the specified id was not found")

        await self._session.execute(self.construct_delete_stmt(id=model_object_id))
        await self._session.commit()

    def construct_update_stmt(self, values: dict, id: int, user_id: int = None):
        stmt = update(self._model).where(self._model.id == id).values(**values).returning(self._model)
        return stmt

    async def update(self, values: dict, model_object_id: int, user_id: int = None):
        stmt = select(self._model).join(self.join_model).filter(self.join_model.fk_user_id == user_id).where(
            self._model.id == model_object_id)
        response = await self._session.execute(stmt)
        sub_category = response.scalar_one_or_none()
        if not sub_category:
            raise HTTPException(status_code=404, detail=f"{self._model.__name__} with the specified id was not found")

        response = await self._session.execute(self.construct_update_stmt(id=model_object_id, values=values))
        await self._session.commit()
        return response.scalar_one()



