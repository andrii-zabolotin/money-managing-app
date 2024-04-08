from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.app.schemas import *
from src.database import get_async_session
from src.models import *

from src.auth.auth import current_user, current_superuser

from typing import List

currency_router = APIRouter()
account_router = APIRouter()
savings_account_router = APIRouter()
category_router = APIRouter()
sub_category_router = APIRouter()


@currency_router.get("/list", response_model=List[CurrencyRead])
async def currency_list(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Currency)
    result = await session.execute(stmt)
    return result.scalars().all()


@currency_router.get("/list/{currency_id}", response_model=CurrencyRead)
async def currency_list(currency_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Currency).where(Currency.id == currency_id)
    result = await session.execute(stmt)
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="currency not found")
    return currency


@currency_router.post("/create")
async def create_currency(
        currency_in: CurrencyCreate,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session),
):
    stmt = insert(Currency).values(**currency_in.model_dump())
    try:
        await session.execute(stmt)
        await session.commit()
        return JSONResponse({"message": "Currency successfully created!"}, status_code=201)
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"Integrity error occurred.")


@currency_router.patch("/update/{currency_id}")
async def account_update(
        currency_id: int,
        currency_in_data: CurrencyUpdate,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    stmt = select(Currency).where(Currency.id == currency_id)
    result = await session.execute(stmt)
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    update_data = currency_in_data.model_dump(exclude_unset=True)
    stmt = update(Currency).where(Currency.id == currency_id).values(update_data)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Currency successfully updated!"}, status_code=200)


@currency_router.delete("/delete/{currency_id}")
async def currency_delete(
        currency_id: int,
        user: User = Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Currency).where(Currency.id == currency_id)
    result = await session.execute(stmt)
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail=f"Currency not found!")
    stmt = delete(Currency).where(Currency.id ==currency_id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Currency successfully deleted!"})


@account_router.get("/list", response_model=List[AccountRead])
async def account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account).where(Account.fk_user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()


@account_router.get("/{account_id}", response_model=AccountRead)
async def account(
        account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account).where(Account.fk_user_id == user.id, Account.id == account_id)
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@account_router.post("/create")
async def account_create(
        account_in: AccountCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    stmt = insert(Account).values(fk_user_id=user.id, **account_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Account successfully created!"}, status_code=201)


@account_router.patch("/update/{account_id}")
async def account_update(
        account_id: int,
        account_in_data: AccountUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    stmt = select(Account).where(Account.id == account_id)
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    update_data = account_in_data.model_dump(exclude_unset=True)
    stmt = update(Account).where(Account.id == account_id).values(update_data)
    result = await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Account successfully updated!"}, status_code=200)


@account_router.delete("/delete/{account_id}")
async def account_delete(
        account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Account).where(Account.id == account_id)
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account not found!")
    stmt = delete(Account).where(Account.id ==account_id)
    response = await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Account successfully deleted!"})


@savings_account_router.get("/list", response_model=List[SavingsAccountRead])
async def savings_account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SavingsAccount).join(Account).filter(Account.fk_user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()


@savings_account_router.get("/{savings_account_id}", response_model=SavingsAccountRead)
async def savings_account_list(
        savings_account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SavingsAccount).join(Account).filter(Account.fk_user_id == user.id).where(SavingsAccount.id == savings_account_id)
    result = await session.execute(stmt)
    savings_account = result.scalar_one_or_none()
    if not savings_account:
        raise HTTPException(status_code=404, detail="Category not found")
    return savings_account


@savings_account_router.post("/create")
async def savings_account_create(
        savings_account_in: SavingsAccountCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    account_in_id = savings_account_in.fk_account_id
    stmt = select(Account).where(Account.id == account_in_id)
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account not found!")
    if not account.is_savings_account:
        raise HTTPException(status_code=404, detail=f"Account variable 'is_savings_account' = False")
    stmt = insert(SavingsAccount).values(**savings_account_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Savings-account successfully created!"})


@savings_account_router.patch("/update/{savings_account_id}")
async def update_savings_account(
        savings_account_in_data: SavingsAccountUpdate,
        savings_account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SavingsAccount).join(Account).filter(Account.fk_user_id == user.id).where(SavingsAccount.id == savings_account_id)
    result = await session.execute(stmt)
    savings_account = result.scalar_one_or_none()
    if not savings_account:
        raise HTTPException(status_code=404, detail="Savings-account not found")
    stmt = update(SavingsAccount).where(SavingsAccount.id == savings_account_id).values(**savings_account_in_data.model_dump(exclude_unset=True))
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Savings-account successfully updated!"}, status_code=200)


@savings_account_router.delete("/delete/{savings_account_id}")
async def update_savings_account(
        savings_account_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SavingsAccount).join(Account).filter(Account.fk_user_id == user.id).where(SavingsAccount.id == savings_account_id)
    result = await session.execute(stmt)
    savings_account = result.scalar_one_or_none()
    if not savings_account:
        raise HTTPException(status_code=404, detail="Savings-account not found")
    stmt = delete(SavingsAccount).where(SavingsAccount.id == savings_account_id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Savings-account successfully deleted!"}, status_code=200)


@category_router.get("/list", response_model=List[CategoryRead])
async def category_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Category).where(Category.fk_user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()


@category_router.get("/{category_id}", response_model=CategoryRead)
async def category_list(
        category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Category).where(Category.fk_user_id == user.id, Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.post("/create")
async def category_create(
        category_in: CategoryCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Category).values(fk_user_id=user.id, **category_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Category successfully created!"})


@category_router.patch("/update/{category_id}")
async def category_update(
        category_id: int,
        category_in_data: CategoryUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    stmt = update(Category).where(Category.id == category_id).values(**category_in_data.model_dump(exclude_unset=True))
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Category successfully updated!"}, status_code=200)


@category_router.delete("/delete/{category_id}")
async def category_delete(
        category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    stmt = delete(Category).where(Category.id == category_id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Category successfully deleted!"})


@sub_category_router.get("/list", response_model=List[SubCategoryRead])
async def sub_category_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SubCategory).join(Category).filter(Category.fk_user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()


@sub_category_router.get("/{sub_category_id}", response_model=SubCategoryRead)
async def sub_category_list(
        sub_category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SubCategory).join(Category).filter(Category.fk_user_id == user.id).where(SubCategory.id == sub_category_id)
    result = await session.execute(stmt)
    sub_category = result.scalar_one_or_none()
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub-category not found")
    return sub_category


@sub_category_router.post("/create")
async def sub_category_create(
        sub_category_in: SubCategoryCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(SubCategory).values(**sub_category_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Sub-category successfully created!"})


@sub_category_router.patch("/update/{sub_category_id}")
async def sub_category_update(
        sub_category_id: int,
        sub_category_in_data: SubCategoryUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SubCategory).where(SubCategory.id == sub_category_id)
    result = await session.execute(stmt)
    sub_category = result.scalar_one_or_none()
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub-category not found")
    stmt = update(SubCategory).where(SubCategory.id == sub_category_id).values(**sub_category_in_data.model_dump(exclude_unset=True))
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({"message": "Sub-category successfully updated!"}, status_code=200)


@sub_category_router.delete("/delete/{sub_category_id}")
async def sub_category_update(
        sub_category_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(SubCategory).where(SubCategory.id == sub_category_id)
    result = await session.execute(stmt)
    sub_category = result.scalar_one_or_none()
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub-category not found")
    stmt = delete(SubCategory).where(SubCategory.id == sub_category_id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Sub-category successfully deleted!"})
