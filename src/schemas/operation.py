from typing import Optional

from pydantic import BaseModel


class OperationRead(BaseModel):
    id: int
    summ: float
    type: bool
    note: Optional[str] = None
    fk_account_id: int
    fk_category_id: int
    fk_sub_category_id: Optional[int] = None
    fk_user_id: int


class OperationCreate(BaseModel):
    summ: float
    type: bool
    note: Optional[str] = None
    fk_account_id: int
    fk_category_id: int
    fk_sub_category_id: Optional[int] = None


class OperationUpdate(BaseModel):
    summ: float = None
    type: bool = None
    note: Optional[str] = None
