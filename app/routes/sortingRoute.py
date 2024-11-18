from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.sortingService import SortingService
from database.db import get_db
from models.pydantic._sorting import SortingCreate, SortingUpdate

sortingRouter = APIRouter()

def get_sorting_service(db: Session = Depends(get_db)) -> SortingService:
    return SortingService(db)

@sortingRouter.get('/', response_model=List[Dict])
def get_all_sortings(status: str = None, service: SortingService = Depends(get_sorting_service)):
    try:
        sortings = service.getAllSortings(status)
        if not sortings:
            raise HTTPException(status_code=404, detail="No sortings found")
        return sortings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@sortingRouter.get('/byStatus', response_model=List[Dict])
def get_all_sortings(status: str = None, service: SortingService = Depends(get_sorting_service)):
    try:
        sortings = service.getAllSortings(status)
        if not sortings:
            raise HTTPException(status_code=404, detail="No sortings found")
        return sortings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@sortingRouter.get('/byId/{sorting_id}', response_model=Dict)
def get_sorting_by_id(sorting_id: str, service: SortingService = Depends(get_sorting_service)):
    try:
        sorting = service.getSortingById(sorting_id)
        if not sorting:
            raise HTTPException(status_code=404, detail="Sorting not found")
        return sorting
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@sortingRouter.post('/', response_model=Dict, status_code=201)
def create_sorting(sorting: SortingCreate, service: SortingService = Depends(get_sorting_service)):
    try:
        new_sorting = service.createSorting(sorting)
        return new_sorting.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@sortingRouter.put('/{sorting_id}', response_model=Dict)
def update_sorting(sorting_id: str, sorting_update: SortingUpdate, service: SortingService = Depends(get_sorting_service)):
    try:
        updated_sorting = service.updateSorting(sorting_id, sorting_update)
        if not updated_sorting:
            raise HTTPException(status_code=404, detail="Sorting not found")
        return updated_sorting.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@sortingRouter.delete('/{sorting_id}', status_code=204)
def delete_sorting(sorting_id: str, service: SortingService = Depends(get_sorting_service)):
    try:
        result = service.deleteSorting(sorting_id)
        if not result:
            raise HTTPException(status_code=404, detail="Sorting not found")
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")