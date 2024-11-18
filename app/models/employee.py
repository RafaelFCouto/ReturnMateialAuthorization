import importlib
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func,Column, String
from database.db import Base
from sqlalchemy.orm import relationship

class Employee(Base):

    __tablename__ = 'employee'

    employeeId = Column(UUID (as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    employeeName = Column(String(255), nullable=False)
    employeeEmail = Column(String(255), nullable=False)
    employeePhone = Column(String(20), nullable=False)
    employeeAddress = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)


    request_approvals = relationship(
        'RequestApproval',
        back_populates='employee',
        primaryjoin="Employee.employeeId == RequestApproval.employeeId",
        lazy=True
    )

    repairs = relationship(
        'Repair',
        back_populates='employee_relation',
        primaryjoin="Employee.employeeId == Repair.employeeId",
        lazy=True
    )

    defects = relationship(
        'Defect',
        back_populates='employee',
        primaryjoin="Employee.employeeId == Defect.employeeId",
        lazy=True
    )

    sortings = relationship(
        'Sorting',
        back_populates='employee',
        primaryjoin="Employee.employeeId == Sorting.employeeId",
        lazy=True
    )

    def as_dict(self):
        return {
            'employeeId': str(self.employeeId),
            'employeeName': self.employeeName,
            'employeeEmail': self.employeeEmail,
            'employeePhone': self.employeePhone,
            'employeeAddress': self.employeeAddress,
            'role': self.role
        }

    def get_request_approval():
        RequestApproval = importlib.import_module('models.requestApproval').RequestApproval
        return RequestApproval

    def get_repair():
        Repair = importlib.import_module('models.repair').Repair
        return Repair