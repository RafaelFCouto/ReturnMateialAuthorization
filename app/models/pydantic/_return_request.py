from pydantic import BaseModel, UUID4


class ReturnRequestCreate(BaseModel):
    reason: str
    notes: str
    proofDocument: str
    customerId: UUID4
    productId: UUID4

class ReturnRequestUpdate(BaseModel):
    reason: str
    notes: str
    proofDocument: str
