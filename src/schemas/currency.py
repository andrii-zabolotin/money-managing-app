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
