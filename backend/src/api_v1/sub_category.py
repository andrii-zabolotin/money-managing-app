from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import *

from src.auth.auth import current_user
from src.repositories.sub_category import SubCategoryRepository

from src.schemas.sub_category import *

router = APIRouter(
    prefix="/sub-category",
    tags=["sub-category"]
)


@router.get("/list", response_model=List[SubCategoryRead])
async def sub_category_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SubCategoryRepository(session=session).list(user_id=user.id)


@router.get("/{sub_category_id}", response_model=SubCategoryRead)
async def sub_category_get(
        sub_category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SubCategoryRepository(session=session).get(model_object_id=sub_category_id, user_id=user.id)


@router.post("/create", status_code=201)
async def sub_category_create(
        sub_category_in: SubCategoryCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SubCategoryRepository(session=session).add(values=sub_category_in.model_dump(), user_id=user.id)


@router.patch("/update/{sub_category_id}")
async def update_sub_category(
        sub_category_in_data: SubCategoryUpdate,
        sub_category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SubCategoryRepository(session=session).update(
        user_id=user.id,
        values=sub_category_in_data.model_dump(),
        model_object_id=sub_category_id
    )


@router.delete("/delete/{sub_category_id}", status_code=204)
async def delete_sub_category(
        sub_category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SubCategoryRepository(session=session).delete(model_object_id=sub_category_id, user_id=user.id)
