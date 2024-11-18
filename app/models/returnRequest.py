import importlib
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy import func, Column, Date, ForeignKey, Enum
from database.db import Base
from sqlalchemy.orm import relationship
from constants.returnRequestStatus import ReturnRequestStatus, ReturnRequestResult

class ReturnRequest(Base):

    __tablename__ = 'return_request'

    returnRequestId = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    request_start_date = Column(Date)
    request_finish_date = Column(Date)
    returnRequestStatus= Column(TEXT())
    returnRequestResult = Column(TEXT())
    reason = Column(TEXT())
    notes = Column(TEXT())
    proofDocument = Column(TEXT())
    customerId = Column(UUID(as_uuid=True), ForeignKey('customer.customerId'), nullable=False)
    productId = Column(UUID(as_uuid=True), ForeignKey('product.productId'), nullable=False)

    customer = relationship('Customer', back_populates='return_requests', lazy=True)
    product = relationship('Product', back_populates='return_requests', lazy=True)
    request_approvals = relationship('RequestApproval', back_populates='return_request', lazy=True)
    sorting = relationship('Sorting', back_populates='return_request', lazy=True)

    def as_dict(self):
        return {
            'returnRequestId': str(self.returnRequestId),
            'request_start_date': self.request_start_date,
            'request_finish_date': self.request_finish_date,
            'returnRequestStatus': self.returnRequestStatus,
            'returnRequestResult': self.returnRequestResult,
            'reason': self.reason,
            'notes': self.notes,
            'proofDocument': self.proofDocument,
            'product': self.product.as_dict(),
            'customer': self.customer.as_dict()
        }
    def get_request_approvals():
        RequestApproval = importlib.import_module('models.requestApproval').RequestApproval
        return RequestApproval





