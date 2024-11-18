from pydantic import BaseModel, UUID4

class RequestApprovalCreate(BaseModel):
    comments: str
    returnRequestId: UUID4
    employeeId: UUID4

class RequestApprovalUpdate(BaseModel):
    comments: str
    requestApprovalStatus: str
