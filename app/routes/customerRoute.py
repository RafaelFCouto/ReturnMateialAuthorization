from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.customerService import CustomerService
from database.db import get_db
from models.pydantic._customer import CustomerCreate, CustomerUpdate

customerRouter = APIRouter()

def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)

@customerRouter.get('/', response_model=List[Dict])
def get_all_customers(service: CustomerService = Depends(get_customer_service)):
    try:
        customers = service.getAllCustomers()
        if not customers:
            raise HTTPException(status_code=404, detail="No customers found")
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@customerRouter.get('/byId/{customer_id}', response_model=Dict)
def get_customer_by_id(customer_id: str, service: CustomerService = Depends(get_customer_service)):
    try:
        customer = service.getCustomerById(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@customerRouter.get('/email/{email}', response_model=Dict)
def get_customer_by_email(email: str, service: CustomerService = Depends(get_customer_service)):
    try:
        customer = service.getCustomerByEmail(email)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@customerRouter.post('/', response_model=Dict, status_code=201)
def create_customer(customer: CustomerCreate, service: CustomerService = Depends(get_customer_service)):
    try:
        if not customer.customerName or not customer.email:
            raise HTTPException(status_code=400, detail="Customer name and email are required")
        new_customer = service.createCustomer(customer)
        return new_customer.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@customerRouter.put('/{customer_id}', response_model=Dict)
def update_customer(customer_id: str, customer: CustomerUpdate, service: CustomerService = Depends(get_customer_service)):
    try:
        updated_customer = service.updateCustomer(customer_id, customer)
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated_customer.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@customerRouter.delete('/{customer_id}', status_code=204)
def delete_customer(customer_id: str, service: CustomerService = Depends(get_customer_service)):
    try:
        result = service.deleteCustomer(customer_id)
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")