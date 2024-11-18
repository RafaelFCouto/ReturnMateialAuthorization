from sqlalchemy.orm import Session
from models.employee import Employee
from utils.generateUUID import GenerateUUID
from typing import List, Dict


class employeeService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllEmployees(self) -> List[Dict]:
        try:
            employees = self.db_session.query(Employee).all()
            return [employee.as_dict() for employee in employees]
        except Exception as e:
            raise Exception(f"Error list Product Types: {e}")

    def getEmployeeById(self, employeeId:str) -> Dict:
        try:
            employee = self.__getEmployeeByAtt('employeeId', employeeId)
            if not employee:
                raise ValueError(f"employee with ID '{employeeId}' not found.")
            return employee.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def getEmployeeByEmail(self, email:str) -> Dict:
        try:
            employee = self.__getEmployeeByAtt('employeeEmail', email)
            if not employee:
                raise ValueError(f"employee with Email '{email}' not found.")
            return employee.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def createEmployee(self, data:Employee)-> Employee:
        employee_id = GenerateUUID.generate_uuid()
        employee = Employee(employeeId=employee_id,
                            employeeName=data.employeeName,
                            employeeEmail=data.employeeEmail,
                            employeePhone= data.employeePhone,
                            employeeAddress=data.employeeAddress,
                            role=data.role)
        try:
            self.db_session.add(employee)
            self.db_session.commit()
            return employee
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on create employee: {e}")

    def updateEmployee(self,employee_id:str, employeeUpdate: Employee) -> Employee:
            try:
                employee = self.__getEmployeeByAtt('employeeId', employee_id)

                if not employee:
                    raise ValueError(f"employee with ID '{employee_id}' not found.")

                employee.employeeName = employeeUpdate.employeeName
                employee.employeeEmail = employeeUpdate.employeeEmail
                employee.employeePhone = employeeUpdate.employeePhone
                employee.employeeAddress = employeeUpdate.employeeAddress
                employee.role = employeeUpdate.role

                self.db_session.commit()
                return employee
            except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating employee: {e}")

    def deleteEmployee(self, employee_id:str):
        try:
            employee = self.__getEmployeeByAtt('employeeId', employee_id)

            if not employee:
                raise ValueError(f"employee with ID '{employee_id}' not found.")

            self.db_session.delete(employee)
            self.db_session.commit()

            return "employee Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting employee: {e}")

    def __getEmployeeByAtt(self, field:str, value:str) -> Employee:
        try:
            employee = self.db_session.query(Employee).filter(getattr(Employee, field) == value).one()
            return employee
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")