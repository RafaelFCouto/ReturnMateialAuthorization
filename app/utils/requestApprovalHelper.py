from constants.requestApprovalStatus import RequestApprovalStatus

class RequestApprovalHelper:

    def getRequestApprovalStatus(status: str) -> str:
        match status:
            case 'PENDING':
                return RequestApprovalStatus.PENDING.value
            case 'APPROVED':
                return RequestApprovalStatus.APPROVED.value
            case 'REJECTED':
                return RequestApprovalStatus.REJECTED.value
            case _:
                raise ValueError(f"Invalid result: {status}")