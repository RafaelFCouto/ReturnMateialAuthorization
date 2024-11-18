from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.returnRequestService import returnRequestService
from database.db import get_db
from models.pydantic._return_request import ReturnRequestCreate, ReturnRequestUpdate

returnRequestRouter = APIRouter()


def get_return_request_service(db: Session = Depends(get_db)) -> returnRequestService:
    return returnRequestService(db)

@returnRequestRouter.get('/', response_model=List[Dict])
def get_all_return_requests(status: str = None, result: str = None, service: returnRequestService = Depends(get_return_request_service)):
    try:
        return_requests = service.getAllReturnRequests(status, result)
        if not return_requests:
            raise HTTPException(status_code=404, detail="No return requests found")
        return return_requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.get('/byResult', response_model=List[Dict])
def get_all_return_requests(status: str = None, result: str = None, service: returnRequestService = Depends(get_return_request_service)):
    try:
        print(result)
        return_requests = service.getAllReturnRequests(status, result)
        if not return_requests:
            raise HTTPException(status_code=404, detail="No return requests found")
        return return_requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.get('/byStatus', response_model=List[Dict])
def get_all_return_requests(status: str = None, result: str = None, service: returnRequestService = Depends(get_return_request_service)):
    try:
        return_requests = service.getAllReturnRequests(status,result)
        if not return_requests:
            raise HTTPException(status_code=404, detail="No return requests found")
        return return_requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.get('/byId/{return_request_id}', response_model=Dict)
def get_return_request_by_id(return_request_id: str, service: returnRequestService = Depends(get_return_request_service)):
    try:
        return_request = service.getReturnRequestById(return_request_id)
        if not return_request:
            raise HTTPException(status_code=404, detail="Return request not found")
        return return_request
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.post('/', response_model=Dict, status_code=201)
def create_return_request(return_request: ReturnRequestCreate, service: returnRequestService = Depends(get_return_request_service)):
    try:
        new_return_request = service.createReturnRequest(return_request)
        return new_return_request.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.put('/{return_request_id}', response_model=Dict)
def update_return_request(return_request_id: str, return_request_update: ReturnRequestUpdate, service: returnRequestService = Depends(get_return_request_service)):
    try:
        updated_return_request = service.updateReturnRequest(return_request_id, return_request_update)
        if not updated_return_request:
            raise HTTPException(status_code=404, detail="Return request not found")
        return updated_return_request.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.delete('/{return_request_id}', status_code=204)
def delete_return_request(return_request_id: str, service: returnRequestService = Depends(get_return_request_service)):
    try:
        result = service.deleteReturnRequest(return_request_id)
        if not result:
            raise HTTPException(status_code=404, detail="Return request not found")
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.put('/putStatus/{return_request_id}', response_model=Dict)
def update_return_request_status(return_request_id: str, status: str, service: returnRequestService = Depends(get_return_request_service)):
    try:
        print(status)
        updated_return_request = service.updateReturnRequestStatus(return_request_id, status)
        return updated_return_request.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@returnRequestRouter.put('/putResult/{return_request_id}', response_model=Dict)
def finish_return_request(return_request_id: str, result: str, service: returnRequestService = Depends(get_return_request_service)):
    try:
        finished_return_request = service.finishReturnRequest(return_request_id, result)
        return finished_return_request.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")