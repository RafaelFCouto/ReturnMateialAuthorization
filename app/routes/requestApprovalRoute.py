from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.requestApprovalService import RequestApprovalService
from database.db import get_db
from models.pydantic._request_approval import RequestApprovalCreate, RequestApprovalUpdate

requestApprovalRouter = APIRouter()

def get_request_approval_service(db: Session = Depends(get_db)) -> RequestApprovalService:
    return RequestApprovalService(db)

@requestApprovalRouter.get('/', response_model=List[Dict])
def get_all_request_approvals(status: str = None, service: RequestApprovalService = Depends(get_request_approval_service)):
    try:
        approvals = service.getAllRequestApprovals(status)
        if not approvals:
            raise HTTPException(status_code=404, detail="No request approvals found")
        return approvals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@requestApprovalRouter.get('/byStatus', response_model=List[Dict])
def get_all_request_approvals_byStatus(status: str = None, service: RequestApprovalService = Depends(get_request_approval_service)):
    try:
        print(status)
        approvals = service.getAllRequestApprovals(status)
        if not approvals:
            raise HTTPException(status_code=404, detail="No request approvals found")
        return approvals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@requestApprovalRouter.get('/byId/{request_approval_id}', response_model=Dict)
def get_request_approval_by_id(request_approval_id: str, service: RequestApprovalService = Depends(get_request_approval_service)):
    try:
        approval = service.getRequestApprovalById(request_approval_id)
        if not approval:
            raise HTTPException(status_code=404, detail="Request approval not found")
        return approval
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@requestApprovalRouter.post('/', response_model=Dict, status_code=201)
def create_request_approval(request_approval: RequestApprovalCreate, service: RequestApprovalService = Depends(get_request_approval_service)):
    try:
        new_approval = service.createRequestApproval(request_approval)
        return new_approval.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@requestApprovalRouter.put('/{request_approval_id}', response_model=Dict)
def update_request_approval(request_approval_id: str, request_approval_update: RequestApprovalUpdate, service: RequestApprovalService = Depends(get_request_approval_service)):
    try:
        updated_approval = service.updateRequestApproval(request_approval_id, request_approval_update)
        if not updated_approval:
            raise HTTPException(status_code=404, detail="Request approval not found")
        return updated_approval.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@requestApprovalRouter.delete('/{request_approval_id}', status_code=204)
def delete_request_approval(request_approval_id: str, service: RequestApprovalService = Depends(get_request_approval_service)):
    try:
        result = service.deleteRequestApproval(request_approval_id)
        if not result:
            raise HTTPException(status_code=404, detail="Request approval not found")
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")