from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.repairService import RepairService
from database.db import get_db
from models.pydantic._repair import RepairCreate, RepairUpdate

repairRouter = APIRouter()

def get_repair_service(db: Session = Depends(get_db)) -> RepairService:
    return RepairService(db)

@repairRouter.get('/', response_model=List[Dict])
def get_all_repairs(service: RepairService = Depends(get_repair_service)):
    try:
        repairs = service.getAllRepairs()
        if not repairs:
            raise HTTPException(status_code=404, detail="No repairs found")
        return repairs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@repairRouter.get('/byId/{repair_id}', response_model=Dict)
def get_repair_by_id(repair_id: str, service: RepairService = Depends(get_repair_service)):
    try:
        repair = service.getRepairById(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail="Repair not found")
        return repair
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@repairRouter.post('/', response_model=Dict, status_code=201)
def create_repair(repair: RepairCreate, service: RepairService = Depends(get_repair_service)):
    try:
        new_repair = service.createRepair(repair)
        return new_repair.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@repairRouter.put('/{repair_id}', response_model=Dict)
def update_repair(repair_id: str, repair_update: RepairUpdate, service: RepairService = Depends(get_repair_service)):
    try:
        updated_repair = service.updateRepair(repair_id, repair_update)
        if not updated_repair:
            raise HTTPException(status_code=404, detail="Repair not found")
        return updated_repair.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@repairRouter.delete('/{repair_id}', status_code=204)
def delete_repair(repair_id: str, service: RepairService = Depends(get_repair_service)):
    try:
        result = service.deleteRepair(repair_id)
        if not result:
            raise HTTPException(status_code=404, detail="Repair not found")
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
