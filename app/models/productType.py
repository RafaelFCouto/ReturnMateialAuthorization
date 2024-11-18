import importlib
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func,Column, String
from database.db import Base
from sqlalchemy.orm import relationship

class ProductType(Base):

    __tablename__ = 'product_type'

    productTypeId = Column(UUID (as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    description = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=False, unique=True)

    products = relationship('Product', back_populates='product_type', lazy=True)

    def as_dict(self):
        return {
            'productTypeId': str(self.productTypeId),
            'description': self.description,
            'sku': self.sku
        }


    def get_product():
        Product = importlib.import_module('models.repair').Product
        return Product
