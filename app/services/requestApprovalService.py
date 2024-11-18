from datetime import datetime
from sqlalchemy.orm import Session
from models.requestApproval import RequestApproval
from typing import List, Dict
from utils.generateUUID import GenerateUUID
from constants.requestApprovalStatus import RequestApprovalStatus
from utils.requestApprovalHelper import RequestApprovalHelper


class RequestApprovalService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllRequestApprovals(self, status:str) -> List[Dict]:
        try:
            query = self.db_session.query(RequestApproval)

            if status:
                query = query.filter(RequestApproval.requestApprovalStatus == status)

            print (query)
            approvals = query.all()
            return [approval.as_dict() for approval in approvals]
        except Exception as e:
            raise Exception(f"Error listing Request Approvals: {e}")

    def getRequestApprovalById(self, requestApprovalId: str) -> Dict:
        try:
            approval = self.__getRequestApprovalByAtt('requestApprovalId', requestApprovalId)
            if not approval:
                raise ValueError(f"Request Approval with ID '{requestApprovalId}' not found.")
            return approval.as_dict()
        except Exception as e:
            raise Exception(f"Error finding Request Approval: {e}")

    def createRequestApproval(self, data: RequestApproval) -> RequestApproval:
        try:
            request_approval_id = GenerateUUID.generate_uuid()
            return_approval_status = RequestApprovalStatus.PENDING.value

            approval = RequestApproval(
                requestApprovalId = request_approval_id,
                requestApprovalStatus=return_approval_status,
                comments=data.comments,
                returnRequestId=data.returnRequestId,
                employeeId=data.employeeId
            )
            self.db_session.add(approval)
            self.db_session.commit()
            return approval
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on creating Request Approval: {e}")

    def updateRequestApproval(self, requestApprovalId: str, approvalUpdate: RequestApproval) -> RequestApproval:
        try:

            if not approvalUpdate.requestApprovalStatus:
                 raise ValueError(f"Request Approval without Approval status.")

            approval = self.__getRequestApprovalByAtt('requestApprovalId', requestApprovalId)

            if not approval:
                raise ValueError(f"Request Approval with ID '{requestApprovalId}' not found.")

            approval.approval_date = datetime.now()
            approval.requestApprovalStatus = RequestApprovalHelper.getRequestApprovalStatus(approvalUpdate.requestApprovalStatus)
            approval.comments = approvalUpdate.comments

            self.db_session.commit()
            return approval
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error updating Request Approval: {e}")

    def deleteRequestApproval(self, requestApprovalId: str):
        try:
            approval = self.__getRequestApprovalByAtt('requestApprovalId', requestApprovalId)

            if not approval:
                raise ValueError(f"Request Approval with ID '{requestApprovalId}' not found.")

            self.db_session.delete(approval)
            self.db_session.commit()

            return "Request Approval Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting Request Approval: {e}")

    def __getRequestApprovalByAtt(self, field: str, value: str) -> RequestApproval:
        try:
            approval = self.db_session.query(RequestApproval).filter(getattr(RequestApproval, field) == value).one()
            return approval
        except Exception as e:
            raise Exception(f"Error finding Request Approval: {e}")