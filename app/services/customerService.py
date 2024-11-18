from sqlalchemy.orm import Session
from models.customer import Customer
from utils.generateUUID import GenerateUUID
from typing import List, Dict


class CustomerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllCustomers(self) -> List[Dict]:
        try:
            Customers = self.db_session.query(Customer).all()
            return [Customer.as_dict() for Customer in Customers]
        except Exception as e:
            raise Exception(f"Error list Product Types: {e}")

    def getCustomerById(self, customerId:str) -> Dict:
        try:
            customer = self.__getCustomerByAtt('customerId', customerId)
            if not customer:
                raise ValueError(f"Customer with ID '{customerId}' not found.")
            return customer.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")


    def getCustomerByEmail(self, email:str) -> Dict:
        try:
            customer = self.__getCustomerByAtt('email', email)
            if not customer:
                raise ValueError(f"Customer with Email '{email}' not found.")
            return customer.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")


    def createCustomer(self, data:Customer)-> Customer:
        customer_id = GenerateUUID.generate_uuid()
        customer = Customer(customerId=customer_id, customerName=data.customerName, email=data.email, phone= data.phone, address=data.address)
        try:
            self.db_session.add(customer)
            self.db_session.commit()
            return customer
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on create Customer: {e}")

    def updateCustomer(self,customer_id:str, customerUpdate: Customer) -> Customer:
            try:
                customer = self.__getCustomerByAtt('customerId', customer_id)

                if not customer:
                    raise ValueError(f"Customer with ID '{customer_id}' not found.")

                customer.customerName = customerUpdate.customerName
                customer.email = customerUpdate.email
                customer.phone = customerUpdate.phone
                customer.address = customerUpdate.address

                self.db_session.commit()
                return customer
            except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating Customer: {e}")

    def deleteCustomer(self, customer_id:str):
        try:
            customer = self.__getCustomerByAtt('customerId', customer_id)

            if not customer:
                raise ValueError(f"Customer with ID '{customer_id}' not found.")

            self.db_session.delete(customer)
            self.db_session.commit()

            return "Customer Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting Customer: {e}")

    def __getCustomerByAtt(self, field:str, value:str) -> Customer:
        try:
            customer = self.db_session.query(Customer).filter(getattr(Customer, field) == value).one()
            return customer
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")