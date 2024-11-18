from sqlalchemy.dialects.postgresql import UUID, TEXT, TIMESTAMP, INTERVAL
from sqlalchemy import func, Column, Float, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship

class Repair(Base):

    __tablename__ = 'repair'

    repairId = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    repair_start_date = Column(TIMESTAMP, nullable=False)
    repair_finish_date = Column(TIMESTAMP)
    timeSpent =Column(Float)
    details = Column(TEXT())
    defectId = Column(UUID(as_uuid=True), ForeignKey('defect.defectId'), nullable=False)
    employeeId = Column(UUID(as_uuid=True), ForeignKey('employee.employeeId'), nullable=False)

    employee_relation = relationship('Employee', back_populates='repairs')
    defect = relationship('Defect', back_populates='repair', lazy=True)

    def as_dict(self):
        return {
            'repairId': str(self.repairId),
            'repair_start_date': self.repair_start_date,
            'repair_finish_date': self.repair_finish_date,
            'details': self.details,
            'timeSpent': self.timeSpent,
            'defect': self.defect.as_dict(),
            'employee': self.employee_relation.as_dict()
        }