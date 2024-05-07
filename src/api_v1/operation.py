from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import get_async_session
from src.models import User
from src.repositories.operation import OperationRepository
from src.schemas.operation import OperationRead, OperationCreate, OperationUpdate

router = APIRouter(
    prefix="/operation",
    tags=["operation"]
)


@router.get("/list", response_model=List[OperationRead])
async def operation_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await OperationRepository(session=session).list(user_id=user.id)


@router.get("/{operation_id}", response_model=OperationRead)
async def operation_get(
        operation_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await OperationRepository(session=session).get(user_id=user.id, model_object_id=operation_id)


@router.post("/create", status_code=201)
async def operation_create(
        operation_in: OperationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await OperationRepository(session=session).add(values=operation_in.model_dump(), user_id=user.id)


@router.patch("/update/{operation_id}")
async def operation_update(
        operation_id: int,
        operation_in_data: OperationUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await OperationRepository(session=session).update(model_object_id=operation_id, user_id=user.id, values=operation_in_data.model_dump(exclude_none=True))


@router.delete("/delete/{operation_id}")
async def operation_delete(
        operation_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await OperationRepository(session=session).delete(user_id=user.id, model_object_id=operation_id)
