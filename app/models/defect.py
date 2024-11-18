import importlib
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy import func,String,Column, Date, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship

class Defect(Base):

    __tablename__ = 'defect'

    defectId = Column(UUID (as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    defectLevel = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    registration_date = Column(Date, nullable=False)
    defectStatus = Column(TEXT())
    productId = Column(UUID(as_uuid=True), ForeignKey('product.productId'), nullable=False)
    ##detected_by
    employeeId = Column(UUID(as_uuid=True), ForeignKey('employee.employeeId'), nullable=False)

    repair = relationship('Repair', back_populates='defect', lazy=True)
    product = relationship('Product', back_populates='defects', lazy=True)
    employee= relationship('Employee', back_populates='defects', lazy=True)

    def as_dict(self):
        return {
            'defectId': str(self.defectId),
            'defectLevel': self.defectLevel,
            'description': self.description,
            'defectStatus': self.defectStatus,
            'product': self.product.as_dict()
        }

    def get_employee():
        Employee = importlib.import_module('models.employee').Employee
        return Employee

    def get_repair():
        Repair = importlib.import_module('models.repair').Repair
        return Repair