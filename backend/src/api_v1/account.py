from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.database import get_async_session
from src.models import User
from src.repositories.account import AccountRepository
from src.schemas.account import AccountRead, AccountCreate, AccountUpdate

router = APIRouter(
    prefix="/account",
    tags=["account"]
)


@router.get("/list", response_model=List[AccountRead])
async def account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountRepository(session=session).list(user_id=user.id)


@router.get("/{account_id}", response_model=AccountRead)
async def account_get(
        account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountRepository(session=session).get(user_id=user.id, model_object_id=account_id)


@router.post("/create", status_code=201)
async def account_create(
        account_in: AccountCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountRepository(session=session).add(values=account_in.model_dump(), user_id=user.id)


@router.patch("/update/{account_id}")
async def account_update(
        account_id: int,
        account_in_data: AccountUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountRepository(session=session).update(model_object_id=account_id, user_id=user.id, values=account_in_data.model_dump(exclude_none=True))


@router.delete("/delete/{account_id}")
async def account_delete(
        account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountRepository(session=session).delete(user_id=user.id, model_object_id=account_id)
