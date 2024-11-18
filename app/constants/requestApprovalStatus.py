from enum import Enum

class RequestApprovalStatus(Enum):
    PENDING = 'Approval Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
