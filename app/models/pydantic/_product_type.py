from pydantic import BaseModel

class ProductTypeCreate(BaseModel):
    description: str
    sku: str

class ProductTypeUpdate(BaseModel):
    description: str
    sku: str