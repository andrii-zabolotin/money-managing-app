from abc import ABC
from typing import Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete, Insert

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from src.models import Base


class BaseRepository:
    def __init__(self, session: AsyncSession, model: Type[Base]):
        self._session = session
        self._model = model

    def construct_get_stmt(self, id: int, user_id: int = None) -> Select:
        stmt = select(self._model).where(self._model.id == id)
        if user_id:
            stmt = select(self._model).where(self._model.id == id, self._model.fk_user_id == user_id)
        return stmt

    async def get(self, model_object_id: int, user_id: int = None):
        query = self.construct_get_stmt(id=model_object_id, user_id=user_id)
        result = await self._session.execute(query)
        model_object = result.scalar_one_or_none()
        if not model_object:
            raise HTTPException(status_code=404, detail=f"{self._model.__name__} with the specified id was not found")
        return model_object

    def construct_list_stmt(self, user_id: int = None) -> Select:
        stmt = select(self._model)
        if user_id:
            stmt = select(self._model).where(self._model.fk_user_id == user_id)
        return stmt

    async def list(self, user_id: int = None):
        query = self.construct_list_stmt(user_id=user_id)
        result = await self._session.execute(query)
        return result.scalars().all()

    def construct_add_stmt(self, values: dict, user_id: int = None) -> Insert:
        stmt = insert(self._model).values(**values).returning(self._model)
        if user_id:
            stmt = insert(self._model).values(fk_user_id=user_id, **values).returning(self._model)
        return stmt

    async def add(self, values: dict, user_id: int = None):
        stmt = self.construct_add_stmt(values=values, user_id=user_id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    def construct_update_stmt(self, values: dict, id: int, user_id: int = None):
        stmt = update(self._model).where(self._model.id == id).values(**values).returning(self._model)
        if user_id:
            stmt = update(self._model).where(self._model.id == id, self._model.fk_user_id == user_id).values(
                **values).returning(self._model)
        return stmt

    async def update(self, values: dict, model_object_id: int, user_id: int = None):
        stmt = self.construct_update_stmt(values=values, id=model_object_id, user_id=user_id)
        result = await self._session.execute(stmt)
        model_object = result.scalar_one_or_none()
        if not model_object:
            raise HTTPException(status_code=404, detail=f"{self._model.__name__} with the specified id was not found")
        await self._session.commit()
        return model_object

    def construct_delete_stmt(self, id: int, user_id: int = None):
        stmt = delete(self._model).where(self._model.id == id)
        if user_id:
            stmt = delete(self._model).where(self._model.id == id, self._model.fk_user_id == user_id)
        return stmt

    async def delete(self, model_object_id: int, user_id: int = None):
        stmt = self.construct_delete_stmt(id=model_object_id, user_id=user_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"{self._model.__name__} with the specified id was not found")
        await self._session.commit()
