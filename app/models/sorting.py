from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy import func,Column, Date, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship

class Sorting(Base):

    __tablename__='sorting'

    sortingId = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    sorting_date = Column(Date)
    sortingStatus = Column(TEXT())
    details = Column(TEXT())
    returnRequestId = Column(UUID(as_uuid=True), ForeignKey('return_request.returnRequestId'), nullable=False)
    employeeId = Column(UUID(as_uuid=True), ForeignKey('employee.employeeId'), nullable=False)

    return_request = relationship('ReturnRequest', back_populates='sorting', lazy=True)
    employee = relationship('Employee', back_populates='sortings')

    def as_dict(self):
        return {
            'sortingId': str(self.sortingId),
            'sorting_date': self.sorting_date,
            'sortingStatus': self.sortingStatus,
            'details': self.details,
            'employee': self.employee.as_dict()
        }

