from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.dependencies import UOWDep
from src.database import get_async_session
from src.models import *

from src.auth.auth import current_user
from src.repositories.savings_account import SavingsAccountRepository
from src.schemas.savings_account import *
from src.services.savings_account import SavingsAccountService

router = APIRouter(
    prefix="/account/savings",
    tags=["savings-account"]
)


@router.get("/list", response_model=List[SavingsAccountRead])
async def savings_account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SavingsAccountRepository(session=session).list(user_id=user.id)


@router.get("/{savings_account_id}", response_model=SavingsAccountRead)
async def savings_account_get(
        savings_account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SavingsAccountRepository(session=session).get(model_object_id=savings_account_id, user_id=user.id)


@router.post("/create", status_code=201)
async def savings_account_create(
        savings_account_in: SavingsAccountCreate,
        uow: UOWDep,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SavingsAccountService().add(account_in=savings_account_in, user_id=user.id, uow=uow)


@router.patch("/update/{savings_account_id}")
async def update_savings_account(
        savings_account_in_data: SavingsAccountManage,
        savings_account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await SavingsAccountRepository(session=session).update(
        values=savings_account_in_data.model_dump(),
        model_object_id=savings_account_id
    )


@router.delete("/delete/{savings_account_id}", status_code=204)
async def delete_savings_account(
        uow: UOWDep,
        savings_account_id: int,
        user: User = Depends(current_user),
):
    await SavingsAccountService().delete(uow=uow, object_id=savings_account_id, user_id=user.id)
