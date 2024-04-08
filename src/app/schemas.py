from typing import Optional

from pydantic import BaseModel


class CurrencyRead(BaseModel):
    id: int
    name: str
    symbol: str


class CurrencyCreate(BaseModel):
    name: str
    symbol: str


class CurrencyUpdate(BaseModel):
    name: str = None
    symbol: str = None


class AccountRead(BaseModel):
    id: int
    name: str
    note: str
    summ: float
    is_savings_account: bool
    image_url: str
    fk_currency_id: int
    fk_user_id: int


class AccountCreate(BaseModel):
    name: str
    note: Optional[str] = None
    summ: float = 0
    is_savings_account: bool = False
    image_url: Optional[str] = None
    fk_currency_id: int


class AccountUpdate(BaseModel):
    name: str = None
    note: str = None
    summ: float = None
    image_url: str = None
    fk_currency_id: int = None


class SavingsAccountRead(BaseModel):
    id: int
    target: float
    fk_account: AccountRead


class SavingsAccountCreate(BaseModel):
    target: float
    fk_account_id: int


class SavingsAccountUpdate(BaseModel):
    target: float


class CategoryRead(BaseModel):
    id: int
    name: str
    image_url: str
    fk_currency_id: int
    fk_user_id: int


class CategoryCreate(BaseModel):
    name: str
    image_url: str
    fk_currency_id: int


class CategoryUpdate(BaseModel):
    name: str
    image_url: str


class SubCategoryRead(BaseModel):
    id: int
    name: str
    fk_category_id: int


class SubCategoryCreate(BaseModel):
    name: str
    fk_category_id: int


class SubCategoryUpdate(BaseModel):
    name: str


class OperationRead(BaseModel):
    id: int
    summ: float
    type: bool
    note: str = None
    fk_account_id: int
    fk_category_id: int
    fk_sub_category_id: int
    fk_user_id: int


class OperationCreate(BaseModel):
    summ: float
    type: bool
    note: str = None
    fk_account_id: int
    fk_category_id: int
    fk_sub_category_id: int
    fk_user_id: int


class OperationUpdate(BaseModel):
    summ: float
    type: bool
    note: str = None
