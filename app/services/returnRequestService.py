from sqlalchemy import and_
from sqlalchemy.orm import Session, lazyload
from constants.returnRequestStatus import ReturnRequestResult, ReturnRequestStatus
from models.returnRequest import ReturnRequest
from utils.generateUUID import GenerateUUID
from typing import List, Dict
from utils.returnRequestHelper import ReturnRequestHelper
from datetime import datetime

class returnRequestService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllReturnRequests(self, status:str=None, result:str=None) -> List[Dict]:
        try:
            query = self.db_session.query(ReturnRequest)
            if status and result:
                query = query.filter(and_(ReturnRequest.returnRequestStatus == status, ReturnRequest.returnRequestResult == result))
            elif status:
                query = query.filter(ReturnRequest.returnRequestStatus == status)
            elif result:
                query = query.filter(ReturnRequest.returnRequestResult == result)

            returnRequests = query.options(lazyload(ReturnRequest.product)).all()
            return [returnRequest.as_dict() for returnRequest in returnRequests]
        except Exception as e:
            raise Exception(f"Error list Product Types: {e}")

    def getReturnRequestById(self, returnRequestId:str) -> Dict:
        try:
            returnRequest = self.__getReturnRequestByAtt('returnRequestId', returnRequestId)
            if not returnRequest:
                raise ValueError(f"returnRequest with ID '{returnRequestId}' not found.")
            return returnRequest.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def getReturnRequestByStatus(self, returnRequestStatus:str) -> Dict:
        try:
            returnRequest = self.__getReturnRequestByAtt('returnRequestStatus', returnRequestStatus)
            if not returnRequest:
                raise ValueError(f"returnRequest with Status '{returnRequestStatus}' not found.")
            return returnRequest.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def createReturnRequest(self, data: ReturnRequest )-> ReturnRequest:
        return_request_id = GenerateUUID.generate_uuid()
        return_request_status = ReturnRequestStatus.AWAITING_ANALYSIS.value
        return_request_result = ReturnRequestResult.WIP.value
        request_start_date = datetime.now()
        returnRequest = ReturnRequest(returnRequestId=return_request_id,
                                      returnRequestStatus=return_request_status,
                                      returnRequestResult=return_request_result,
                                      reason=data.reason,
                                      notes=data.notes,
                                      proofDocument=data.proofDocument,
                                      customerId=data.customerId,
                                      productId=data.productId,
                                      request_start_date=request_start_date)
        try:
            self.db_session.add(returnRequest)
            self.db_session.commit()
            return returnRequest
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on create returnRequest: {e}")

    def updateReturnRequest(self,returnRequestId:str, returnRequestUpdate: ReturnRequest) -> ReturnRequest:
            try:
                returnRequest = self.__getReturnRequestByAtt('returnRequestId', returnRequestId)

                if not returnRequest:
                    raise ValueError(f"returnRequest with ID '{returnRequestId}' not found.")

                returnRequest.reason=returnRequestUpdate.reason,
                returnRequest.notes=returnRequestUpdate.notes,
                returnRequest.proofDocument=returnRequestUpdate.proofDocument
                self.db_session.commit()
                return returnRequest
            except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating returnRequest: {e}")

    def updateReturnRequestStatus(self,returnRequestId:str, status:str)-> ReturnRequest:
        try:
            print(returnRequestId)
            print(status)
            returnRequest = self.__getReturnRequestByAtt('returnRequestId', returnRequestId)
            status_update = ReturnRequestHelper.getReturnRequestStatus(status)
            returnRequest.returnRequestStatus = status_update
            self.db_session.commit()
            return returnRequest

        except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating returnRequest: {e}")

    def finishReturnRequest(self,returnRequestId:str, result:str)-> ReturnRequest:
        try:
            returnRequest = self.__getReturnRequestByAtt('returnRequestId', returnRequestId)

            returnRequest.request_finish_date = datetime.now()
            returnRequest.returnRequestResult = ReturnRequestHelper.getReturnRequestResult(result)
            self.db_session.commit()
            return returnRequest

        except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating returnRequest: {e}")

    def deleteReturnRequest(self, returnRequestId:str):
        try:
            returnRequest = self.__getReturnRequestByAtt('returnRequestId', returnRequestId)

            if not returnRequest:
                raise ValueError(f"returnRequest with ID '{returnRequestId}' not found.")

            self.db_session.delete(returnRequest)
            self.db_session.commit()

            return "Return request Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting ReturnRequest: {e}")

    def __getReturnRequestByAtt(self, field:str, value:str) -> ReturnRequest:
        try:
            returnRequest = self.db_session.query(ReturnRequest).filter(getattr(ReturnRequest, field) == value).one()
            return returnRequest
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")