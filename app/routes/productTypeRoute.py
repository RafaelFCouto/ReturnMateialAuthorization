from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.productTypeService import ProductTypeService
from database.db import get_db
from models.pydantic._product_type import ProductTypeCreate, ProductTypeUpdate


productTypeRouter = APIRouter()

#dependence for service
def get_product_type_service(db: Session = Depends(get_db)) -> ProductTypeService:
    return ProductTypeService(db)

@productTypeRouter.get('/', response_model=List[Dict])
def get_all_product_types(service: ProductTypeService = Depends(get_product_type_service)):
    try:
        productTypes = service.getAllProductTypes()
        if not productTypes:
            raise HTTPException(status_code=404, detail="Not found")
        return productTypes;
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productTypeRouter.get('/byId/{product_type_id}', response_model=Dict)
def get_product_type_by_id(product_type_id: str, service: ProductTypeService = Depends(get_product_type_service)):
    try:
        product_type = service.getProductTypeById(product_type_id)
        if not product_type:
            raise HTTPException(status_code=404, detail="Product Type not found")
        print(product_type)
        return product_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productTypeRouter.get('/sku/{sku}', response_model=Dict)
def get_product_type_by_sku(sku: str, service: ProductTypeService = Depends(get_product_type_service)):
    try:
        product_type = service.getProductTypeBySku(sku)
        if not product_type:
            raise HTTPException(status_code=404, detail="Product Type not found")
        return product_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productTypeRouter.post('/', response_model=Dict, status_code=201)
def createProductType(product_type:ProductTypeCreate, service: ProductTypeService = Depends(get_product_type_service)):
    if not product_type.description or not product_type.sku:
        raise HTTPException(status_code=400, detail="Description and SKU are required")
    try:
        new_product_type = service.createProductType(product_type.description, product_type.sku)
        return new_product_type.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productTypeRouter.put('/{product_type_id}', response_model=Dict)
def update_product_type(product_type_id: str,product_type: ProductTypeUpdate,  service: ProductTypeService = Depends(get_product_type_service)):
    try:
        updated_product_type = service.updateProductType(product_type_id, product_type)
        if not updated_product_type:
            raise HTTPException(status_code=404, detail="Product Type not found")
        return updated_product_type.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productTypeRouter.delete('/{product_type_id}', status_code=204)
def delete_product_type(product_type_id: str, service: ProductTypeService = Depends(get_product_type_service)):
    try:
        deleted = service.deleteProductType(product_type_id)
        print(deleted)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product Type not found")
        return deleted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

