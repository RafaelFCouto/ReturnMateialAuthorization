from pydantic import BaseModel, UUID4

class SortingCreate(BaseModel):
    details: str
    returnRequestId: UUID4
    employeeId: UUID4

class SortingUpdate(BaseModel):
    details: str
    sortingStatus: str