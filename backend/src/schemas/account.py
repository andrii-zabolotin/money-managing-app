from typing import Optional

from pydantic import BaseModel


class AccountRead(BaseModel):
    id: int
    name: str
    note: str
    summ: float
    is_savings_account: bool
    image_url: Optional[str] = None
    fk_currency_id: int
    fk_user_id: int


class AccountCreate(BaseModel):
    name: str
    note: Optional[str] = None
    summ: float = 0
    image_url: Optional[str] = None
    fk_currency_id: int


class AccountUpdate(BaseModel):
    name: str = None
    note: str = None
    summ: float = None
    image_url: str = None
    fk_currency_id: int = None
