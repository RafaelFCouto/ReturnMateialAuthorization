from constants.sorting import SortingStatus

class SortingStatusHelper:

    def getSortingStatus(status: str) -> str:
        match status:
            case 'REFUND':
                return SortingStatus.REFUND.value
            case 'REPAIR':
                return SortingStatus.REPAIR.value
            case 'REPLACEMENT':
                return SortingStatus.REPLACEMENT.value
            case 'CANCELLED':
                return SortingStatus.CANCELLED.value
            case _:
                raise ValueError(f"Invalid result: {status}")