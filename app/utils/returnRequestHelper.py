from constants.returnRequestStatus import ReturnRequestStatus, ReturnRequestResult

class ReturnRequestHelper:

    def getReturnRequestResult(result: str) -> str:
        match result:
            case 'REFUND':
                return ReturnRequestResult.REFUND.value
            case 'REPAIRED':
                return ReturnRequestResult.REPAIRED.value
            case 'REPLACEMENT':
                return ReturnRequestResult.REPLACEMENT.value
            case 'WIP':
                return ReturnRequestResult.WIP.value
            case 'CANCELLED':
                return ReturnRequestResult.CANCELLED.value
            case _:
                raise ValueError(f"Invalid result: {result}")

    def getReturnRequestStatus(status: str) -> str:
        match status:
            case 'AWAITING_ANALYSIS':
                return ReturnRequestStatus.AWAITING_ANALYSIS.value
            case 'READY_FOR_RETURN':
                print('here on get return request status')
                return ReturnRequestStatus.READY_FOR_RETURN.value
            case 'UNDER_REPAIR':
                return ReturnRequestStatus.UNDER_REPAIR.value
            case _:
                raise ValueError(f"Invalid status: {status}")