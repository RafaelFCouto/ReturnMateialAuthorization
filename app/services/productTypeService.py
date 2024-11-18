from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.productType import ProductType
from utils.generateUUID import GenerateUUID
from typing import List, Dict

class ProductTypeService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllProductTypes(self) -> List[Dict]:
        try:
            productTypes = self.db_session.query(ProductType).all()
            return [productType.as_dict() for productType in productTypes]
        except Exception as e:
            raise Exception(f"Error list Product Types: {e}")

    def getProductTypeById(self, productTypeId:str) -> Dict:
        try:
            productType = self.__getProductTypeByAtt('productTypeId', productTypeId)
            if not productType:
                raise ValueError(f"ProductType with ID '{productTypeId}' not found.")
            return productType.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def getProductTypeBySku(self, sku:str) -> Dict:
        try:
            productType = self.__getProductTypeByAtt('sku', sku)
            if not productType:
                raise ValueError(f"ProductType with SKU '{sku}' not found.")
            return productType.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def createProductType(self, description:str, sku:str)-> ProductType:
        product_type_id = GenerateUUID.generate_uuid()
        productType = ProductType(productTypeId=product_type_id, description=description, sku=sku)
        try:
            self.db_session.add(productType)
            self.db_session.commit()
            return productType
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError(f"SKU '{sku}' already registered.")
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on create ProductType: {e}")

    def updateProductType(self,product_type_id:str, productTypeUpdate: ProductType) -> ProductType:
            try:
                productType = self.__getProductTypeByAtt('productTypeId', product_type_id)

                if not productType:
                    raise ValueError(f"ProductType with ID '{product_type_id}' not found.")

                productType.description = productTypeUpdate.description
                productType.sku = productTypeUpdate.sku
                self.db_session.commit()
                return productType
            except IntegrityError:
                self.db_session.rollback()
                raise ValueError(f"SKU '{productTypeUpdate.sku}' is already in use.")
            except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating ProductType: {e}")

    def deleteProductType(self, product_type_id:str):
        try:
            productType = self.__getProductTypeByAtt('productTypeId', product_type_id)

            if not productType:
                raise ValueError(f"ProductType with ID '{product_type_id}' not found.")

            self.db_session.delete(productType)
            self.db_session.commit()

            return "Product Type Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting ProductType: {e}")

    def __getProductTypeByAtt(self, field:str, value:str) -> ProductType:
        try:
            productType = self.db_session.query(ProductType).filter(getattr(ProductType, field) == value).one()
            return productType
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")