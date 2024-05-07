from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import get_async_session
from src.models import User
from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryRead,CategoryUpdate, CategoryCreate

router = APIRouter(
    prefix="/category",
    tags=["category"]
)


@router.get("/list", response_model=List[CategoryRead])
async def category_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryRepository(session=session).list(user_id=user.id)


@router.get("/{category_id}", response_model=CategoryRead)
async def category_get(
        category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryRepository(session=session).get(user_id=user.id, model_object_id=category_id)


@router.post("/create", status_code=201)
async def category_create(
        category_in: CategoryCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryRepository(session=session).add(values=category_in.model_dump(), user_id=user.id)


@router.patch("/update/{category_id}")
async def category_update(
        category_id: int,
        category_in_data: CategoryUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryRepository(session=session).update(model_object_id=category_id, user_id=user.id, values=category_in_data.model_dump(exclude_none=True))


@router.delete("/delete/{category_id}")
async def category_delete(
        category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryRepository(session=session).delete(user_id=user.id, model_object_id=category_id)
