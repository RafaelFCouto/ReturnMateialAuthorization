from pydantic import BaseModel, UUID4
from datetime import date

class ProductCreate(BaseModel):
    description: str
    productModel: str
    manufacture_date: date
    price: float
    productTypeId: UUID4

class ProductUpdate(BaseModel):
    description: str
    productModel: str
    manufacture_date: date
    price: float
    productTypeId: str