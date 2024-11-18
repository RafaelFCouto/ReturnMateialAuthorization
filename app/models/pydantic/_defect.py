from pydantic import UUID4, BaseModel
from typing import Optional

class DefectCreate(BaseModel):
    defectLevel: str
    description: str
    productId: UUID4
    employeeId: UUID4


class DefectUpdate(BaseModel):
    defectLevel: str
    description: str
    defectStatus: Optional[str]=None
    productId: UUID4
    employeeId: UUID4