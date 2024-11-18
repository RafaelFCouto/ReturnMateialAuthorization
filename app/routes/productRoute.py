from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.productService import ProductService
from database.db import get_db
from models.pydantic._product import ProductCreate, ProductUpdate

productRouter = APIRouter()

#dependence for service
def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)

@productRouter.get('/', response_model=List[Dict])
def get_all_products(service: ProductService = Depends(get_product_service)):
    try:
        products = service.getAllProducts()
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productRouter.get('/byId/{product_id}', response_model=Dict)
def get_product_by_id(product_id: str, service: ProductService = Depends(get_product_service)):
    try:
        product = service.getProductById(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productRouter.post('/', response_model=Dict, status_code=201)
def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    if not product.productModel or not product.productTypeId:
        raise HTTPException(status_code=400, detail="Fields are required")
    try:
        new_product = service.createProduct(product)
        return new_product.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productRouter.put('/{product_id}', response_model=Dict)
def update_product(product_id: str, product_update: ProductUpdate, service: ProductService = Depends(get_product_service)):
    try:
        updated_product = service.updateProduct(product_id, product_update)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@productRouter.delete('/{product_id}', status_code=204)
def delete_product(product_id: str, service: ProductService = Depends(get_product_service)):
    try:
        deleted = service.deleteProduct(product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"detail": "Product removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")