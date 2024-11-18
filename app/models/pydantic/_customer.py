from pydantic import BaseModel

class CustomerCreate(BaseModel):
    customerName: str
    email: str
    phone: str
    address: str

class CustomerUpdate(BaseModel):
    customerName: str
    email: str
    phone: str
    address: str
