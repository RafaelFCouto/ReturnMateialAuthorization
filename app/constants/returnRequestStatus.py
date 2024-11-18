from enum import Enum

class ReturnRequestStatus(Enum):
    AWAITING_ANALYSIS = 'Awaiting Analysis'
    UNDER_REPAIR = 'Under Repair'
    READY_FOR_RETURN = 'Ready for Return'


class ReturnRequestResult(Enum):
    REFUND = 'Refund'
    WIP = 'Work In Progress'
    REPLACEMENT = 'Replacement'
    CANCELLED = 'Cancelled'
    REPAIRED = 'Repaired'