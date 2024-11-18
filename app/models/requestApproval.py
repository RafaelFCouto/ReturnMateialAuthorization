from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy import func, Column, Date, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship
import importlib

class RequestApproval(Base):

    __tablename__ = 'request_approval'

    requestApprovalId = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    approval_date = Column(Date)
    requestApprovalStatus = Column(TEXT())
    comments = Column(TEXT())
    returnRequestId = Column(UUID(as_uuid=True), ForeignKey('return_request.returnRequestId'), nullable=False)
    employeeId = Column(UUID(as_uuid=True), ForeignKey('employee.employeeId'), nullable=False)

    return_request = relationship('ReturnRequest', back_populates='request_approvals', lazy=True)
    employee = relationship('Employee', back_populates='request_approvals')

    def as_dict(self):
        return {
            'requestApprovalId': str(self.requestApprovalId),
            'approval_date': self.approval_date,
            'comments': self.comments,
            'requestAprovalStatus': self.requestApprovalStatus,
            'returnRequest': {
                'returnRequestId': str(self.return_request.returnRequestId),
                'request_start_date': self.return_request.request_start_date,
                'request_finish_date': self.return_request.request_finish_date,
                'returnRequestStatus': self.return_request.returnRequestStatus,
                'reason': self.return_request.reason,
                'notes': self.return_request.notes,
                'proofDocument': self.return_request.proofDocument,
                'product':{
                    'productId': str(self.return_request.product.productId),
                    'productModel': self.return_request.product.productModel,
                    'description': self.return_request.product.description,
                    'manufacture_date': self.return_request.product.manufacture_date,
                    'price': self.return_request.product.price,
                    'productType': {
                        'productTypeId': str(self.return_request.product.product_type.productTypeId),
                        'description': self.return_request.product.product_type.description,
                        'sku': self.return_request.product.product_type.sku,
                    }
                }
            }
        }

    def get_employee():
        Employee = importlib.import_module('models.employee').Employee
        return Employee

    def get_return_request():
        ReturnRequest = importlib.import_module('models.returnRequest').ReturnRequest
        return ReturnRequest






