from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.defectService import defectService
from database.db import get_db
from models.pydantic._defect import DefectCreate, DefectUpdate

defectRouter = APIRouter()

def get_defect_service(db: Session = Depends(get_db)) -> defectService:
    return defectService(db)

@defectRouter.get('/', response_model=List[Dict])
def get_all_defects(status: str = None, service: defectService = Depends(get_defect_service)):
    try:
        print('here - route')
        defects = service.getAllDefects(status)
        if not defects:
            raise HTTPException(status_code=404, detail="No defects found")
        return defects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@defectRouter.get('/byId/{defect_id}', response_model=Dict)
def get_defect_by_id(defect_id: str, service: defectService = Depends(get_defect_service)):
    try:
        defect = service.getDefectById(defect_id)
        if not defect:
            raise HTTPException(status_code=404, detail="Defect not found")
        return defect
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@defectRouter.get('/byStatus', response_model=List[Dict])
def get_all_defects(status: str = None, service: defectService = Depends(get_defect_service)):
    try:
        print('here - route')
        defects = service.getAllDefects(status)
        if not defects:
            raise HTTPException(status_code=404, detail="No defects found")
        return defects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@defectRouter.post('/', response_model=Dict, status_code=201)
def create_defect(defect: DefectCreate, service: defectService = Depends(get_defect_service)):
    try:
        new_defect = service.createDefect(defect)
        return new_defect.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@defectRouter.put('/{defect_id}', response_model=Dict)
def update_defect(defect_id: str, defect_update: DefectUpdate, service: defectService = Depends(get_defect_service)):
    try:
        updated_defect = service.updateDefect(defect_id, defect_update)
        if not updated_defect:
            raise HTTPException(status_code=404, detail="Defect not found")
        return updated_defect.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@defectRouter.delete('/{defect_id}', status_code=204)
def delete_defect(defect_id: str, service: defectService = Depends(get_defect_service)):
    try:
        result = service.deleteDefect(defect_id)
        if not result:
            raise HTTPException(status_code=404, detail="Defect not found")
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
