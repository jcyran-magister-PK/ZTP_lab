from pydantic import BaseModel, ConfigDict


class ForbiddenNames(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Category(BaseModel):
    id: int
    name: str
    min_price: float
    max_price: float

    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    id: int
    name: str
    category: Category
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    category_id: int
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)
