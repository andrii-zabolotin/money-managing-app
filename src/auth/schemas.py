from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    password: str = Field(min_length=5)


class UserUpdate(schemas.BaseUserUpdate):
    username: str
