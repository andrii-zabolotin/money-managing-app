from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_superuser
from src.database import get_async_session
from src.models import User
from src.repositories.currency import CurrencyRepository
from src.schemas.currency import CurrencyCreate, CurrencyRead, CurrencyUpdate
router = APIRouter(
    prefix="/currency",
    tags=["currency"]
)


@router.get("/list", response_model=List[CurrencyRead])
async def currency_list(
    session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyRepository(session=session).list()


@router.get("/{currency_id}", response_model=CurrencyRead)
async def currency_get(
        currency_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyRepository(session=session).get(model_object_id=currency_id)


@router.post("/create", status_code=201)
async def currency_create(
        currency_in: CurrencyCreate,
        session = Depends(get_async_session)
):
    return await CurrencyRepository(session=session).add(values=currency_in.model_dump())


@router.patch("/update/{currency_id}")
async def currency_update(
        currency_id: int,
        currency_in_data: CurrencyUpdate,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyRepository(session=session).update(model_object_id=currency_id, values=currency_in_data.model_dump(exclude_none=True))


@router.delete("/delete/{currency_id}")
async def currency_delete(
        currency_id: int,
        # user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyRepository(session=session).delete(model_object_id=currency_id)
