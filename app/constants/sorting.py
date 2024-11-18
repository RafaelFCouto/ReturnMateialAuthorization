from enum import Enum

class SortingStatus(Enum):
    PENDING = 'Pending Sorting'
    REFUND = 'For Refund'
    REPLACEMENT = 'For Replacement'
    CANCELLED = 'Cancelled'
    REPAIR = 'For Repair'
