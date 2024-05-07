from typing import Optional

from pydantic import BaseModel


class CategoryRead(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    fk_currency_id: int
    fk_user_id: int


class CategoryCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
    fk_currency_id: int


class CategoryUpdate(BaseModel):
    name: str = None
    image_url: Optional[str] = None
