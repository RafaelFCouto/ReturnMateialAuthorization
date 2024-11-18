import importlib
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, Column, String
from database.db import Base
from sqlalchemy.orm import relationship


class Customer(Base):

    __tablename__ = 'customer'

    customerId = Column(UUID (as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    customerName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)

    return_requests = relationship('ReturnRequest', back_populates='customer', lazy=True)

    def as_dict(self):
        return {
            'customerId': str(self.customerId),
            'customerName': self.customerName,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }

    def get_return_request():
        ReturnRequest = importlib.import_module('models.returnRequest').ReturnRequest
        return ReturnRequest