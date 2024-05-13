from pydantic import BaseModel


class SubCategoryRead(BaseModel):
    id: int
    name: str
    fk_category_id: int


class SubCategoryCreate(BaseModel):
    name: str
    fk_category_id: int


class SubCategoryUpdate(BaseModel):
    name: str
