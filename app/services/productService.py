from sqlalchemy.orm import Session
from models.product import Product
from utils.generateUUID import GenerateUUID
from typing import List, Dict

class ProductService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllProducts(self) -> List[Dict]:
        try:
            products = self.db_session.query(Product).all()
            return [product.as_dict() for product in products]
        except Exception as e:
            raise Exception(f"Error list Product Types: {e}")

    def getProductById(self, productId:str) -> Dict:
        try:
            product = self.__getProductByAtt('productId', productId)
            if not product:
                raise ValueError(f"Product with ID '{productId}' not found.")
            return product.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def createProduct(self, data: Product)-> Product:
        product_id = GenerateUUID.generate_uuid()
        product = Product(productId=product_id,
                          description=data.description,
                          productModel = data.productModel,
                          manufacture_date=data.manufacture_date,
                          price = data.price,
                          productTypeId = data.productTypeId)
        try:
            self.db_session.add(product)
            self.db_session.commit()

            return product
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on create Product: {e}")

    def updateProduct(self,product_id:str, productUpdate: Product) -> Product:
            try:
                product = self.__getProductByAtt('productId', product_id)

                if not product:
                    raise ValueError(f"Product with ID '{product_id}' not found.")

                product.productModel = productUpdate.productModel
                product.description = productUpdate.description
                product.manufacture_date = productUpdate.manufacture_date
                product.price = productUpdate.price
                product.productTypeId = productUpdate.productTypeId

                self.db_session.commit()
                return product

            except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating Product: {e}")

    def deleteProduct(self, product_id:str):
        try:
            product = self.__getProductByAtt('productId', product_id)

            if not Product:
                raise ValueError(f"Product with ID '{product_id}' not found.")

            self.db_session.delete(product)
            self.db_session.commit()

            return "Product Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting Product: {e}")

    def __getProductByAtt(self, field:str, value:str) -> Product:
        try:
            product = self.db_session.query(Product).filter(getattr(Product, field) == value).one()
            return product
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")