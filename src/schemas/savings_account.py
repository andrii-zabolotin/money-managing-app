from pydantic import BaseModel

from src.schemas.account import AccountRead, AccountCreate


class SavingsAccountRead(BaseModel):
    id: int
    target: float
    fk_account_id: int


class SavingsAccountManage(BaseModel):
    target: float


class SavingsAccountCreate(BaseModel):
    account: AccountCreate
    target: float
