from datetime import datetime
from sqlalchemy.orm import Session
from models.sorting import Sorting
from typing import List, Dict
from constants.sorting import SortingStatus
from utils.sortingHelper import SortingStatusHelper
from utils.generateUUID import GenerateUUID


class SortingService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllSortings(self, status:str) -> List[Dict]:
        try:
            query = self.db_session.query(Sorting)
            if status:
                query = query.filter(Sorting.sortingStatus == status)

            sortings = query.all()
            return [sorting.as_dict() for sorting in sortings]
        except Exception as e:
            raise Exception(f"Error listing Sortings: {e}")

    def getSortingById(self, sortingId: str) -> Dict:
        try:
            sorting = self.__getSortingByAtt('sortingId', sortingId)
            if not sorting:
                raise ValueError(f"Sorting with ID '{sortingId}' not found.")
            return sorting.as_dict()
        except Exception as e:
            raise Exception(f"Error finding Sorting: {e}")

    def createSorting(self, data: Sorting) -> Sorting:
        try:
            sorting_id = GenerateUUID.generate_uuid()
            sorting_status = SortingStatus.PENDING.value
            sorting = Sorting(
                sortingId = sorting_id,
                sortingStatus=sorting_status,
                details=data.details,
                returnRequestId=data.returnRequestId,
                employeeId=data.employeeId
            )
            self.db_session.add(sorting)
            self.db_session.commit()
            return sorting
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on creating Sorting: {e}")

    def updateSorting(self, sortingId: str, sortingUpdate: Sorting) -> Sorting:
        try:
            if not sortingUpdate.sortingStatus:
                raise ValueError(f"Sorting without Status.")

            sorting = self.__getSortingByAtt('sortingId', sortingId)

            if not sorting:
                raise ValueError(f"Sorting with ID '{sortingId}' not found.")

            sorting.sorting_date = datetime.now()
            sorting.sortingStatus = SortingStatusHelper.getSortingStatus(sortingUpdate.sortingStatus)
            sorting.details = sortingUpdate.details

            self.db_session.commit()
            return sorting
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error updating Sorting: {e}")

    def deleteSorting(self, sortingId: str):
        try:
            sorting = self.__getSortingByAtt('sortingId', sortingId)

            if not sorting:
                raise ValueError(f"Sorting with ID '{sortingId}' not found.")

            self.db_session.delete(sorting)
            self.db_session.commit()

            return "Sorting Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting Sorting: {e}")

    def __getSortingByAtt(self, field: str, value: str) -> Sorting:
        try:
            sorting = self.db_session.query(Sorting).filter(getattr(Sorting, field) == value).one()
            return sorting
        except Exception as e:
            raise Exception(f"Error finding Sorting: {e}")