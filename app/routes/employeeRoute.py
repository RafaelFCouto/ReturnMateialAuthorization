from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.employeeService import employeeService
from database.db import get_db
from models.pydantic._employee import EmployeeCreate, EmployeeUpdate

employeeRouter = APIRouter()

def get_employee_service(db: Session = Depends(get_db)) -> employeeService:
    return employeeService(db)

@employeeRouter.get('/', response_model=List[Dict])
def get_all_employees(service: employeeService = Depends(get_employee_service)):
    try:
        employees = service.getAllEmployees()
        if not employees:
            raise HTTPException(status_code=404, detail="No employees found")
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@employeeRouter.get('/byId/{employee_id}', response_model=Dict)
def get_employee_by_id(employee_id: str, service: employeeService = Depends(get_employee_service)):
    try:
        employee = service.getEmployeeById(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@employeeRouter.get('/email/{email}', response_model=Dict)
def get_employee_by_email(email: str, service: employeeService = Depends(get_employee_service)):
    try:
        employee = service.getEmployeeByEmail(email)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@employeeRouter.post('/', response_model=Dict, status_code=201)
def create_employee(employee: EmployeeCreate, service: employeeService = Depends(get_employee_service)):
    try:
        if not employee.employeeName or not employee.employeeEmail:
            raise HTTPException(status_code=400, detail="Employee name and email are required")
        new_employee = service.createEmployee(employee)
        return new_employee.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@employeeRouter.put('/{employee_id}', response_model=Dict)
def update_employee(employee_id: str, employee: EmployeeUpdate, service: employeeService = Depends(get_employee_service)):
    try:
        updated_employee = service.updateEmployee(employee_id, employee)
        if not updated_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return updated_employee.as_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@employeeRouter.delete('/{employee_id}', status_code=204)
def delete_employee(employee_id: str, service: employeeService = Depends(get_employee_service)):
    try:
        result = service.deleteEmployee(employee_id)
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")