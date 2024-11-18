from pydantic import BaseModel, UUID4

class RepairCreate(BaseModel):
    details: str
    defectId: UUID4
    employeeId: UUID4

class RepairUpdate(BaseModel):
    details: str

