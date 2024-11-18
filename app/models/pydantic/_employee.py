from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    employeeName: str
    employeeEmail: str
    employeePhone: str
    employeeAddress: str
    role: str

class EmployeeUpdate(BaseModel):
    employeeName: str
    employeeEmail: str
    employeePhone: str
    employeeAddress: str
    role: str