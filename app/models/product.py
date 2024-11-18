import importlib
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy import func,Column, String, Float, Date, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship

class Product(Base):

    __tablename__ = 'product'

    productId = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    productModel = Column(String(255), nullable=False)
    description = Column(TEXT())
    manufacture_date = Column(Date)
    price = Column(Float)
    productTypeId = Column(UUID(as_uuid=True), ForeignKey('product_type.productTypeId'), nullable=False)

    product_type = relationship('ProductType', back_populates='products', lazy=True)
    defects = relationship('Defect', back_populates='product', lazy=True)
    return_requests = relationship('ReturnRequest', back_populates='product', lazy=True)

    def as_dict(self):
        return {
            'productId': str(self.productId),
            'productModel': self.productModel,
            'description': self.description,
            'manufacture_date': self.manufacture_date,
            'price': self.price,
            'productType': {
                'productTypeId': str(self.product_type.productTypeId),
                'description': self.product_type.description,
                'sku': self.product_type.sku,
            }
        }


    def get_product_type():
        ProductType = importlib.import_module('models.productType').ProductType
        return ProductType

    def get_defects():
        Defect = importlib.import_module('models.defect').Defect
        return Defect

    def get_return_requests():
        ReturnRequest = importlib.import_module('models.returnRequest').ReturnRequest
        return ReturnRequest