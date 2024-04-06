from pydantic import BaseModel


class CurrencyRead(BaseModel):
    name: str
