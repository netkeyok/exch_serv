from sqlalchemy import Column, String, Float, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from db_connections.pg_conf import Base
from sqlalchemy.dialects.postgresql import ARRAY  # импортировать тип данных ARRAY для работы со списками


# определить класс QuantityPolicy для модели SQLAlchemy
class QuantityPolicy(Base):
    __tablename__ = "quantity_policy"
    id = Column(String, primary_key=True)
    multiline = Column(Boolean)
    packing_ids = Column(ARRAY(String))  # использовать тип данных ARRAY для хранения списка строк


# определить класс Packing для модели SQLAlchemy
class Packing(Base):
    __tablename__ = "packing"
    id = Column(String, primary_key=True)
    name = Column(String)
    self_weight = Column(Float)
    self_volume = Column(Float)
    units_quantity = Column(Float)
    barcode = Column(String)
    barcodes = Column(ARRAY(String))  # использовать тип данных ARRAY для хранения списка строк
    marking = Column(String)


# определить класс Product для модели SQLAlchemy
class Product(Base):
    __tablename__ = "product"
    id = Column(String, primary_key=True)
    name = Column(String)
    barcode = Column(String)
    base_packing_id = Column(String, ForeignKey("packing.id"))
    base_packing = relationship("Packing", backref="products")  # добавить аргумент backref для обратной связи
    marking = Column(String)
    quantity_policy_id = Column(String, ForeignKey("quantity_policy.id"))
    quantity_policy = relationship("QuantityPolicy", backref="products")  # добавить аргумент backref для обратной связи
    packings = relationship("Packing", secondary="product_packing",
                            back_populates="products")  # добавить аргумент back_populates для синхронизации связи


# определить ассоциативную таблицу для связи многие-ко-многим между продуктом и упаковкой
product_packing = Table(
    "product_packing",
    Base.metadata,
    Column("product_id", String, ForeignKey("product.id")),
    Column("packing_id", String, ForeignKey("packing.id"))
)

# добавить атрибут products в класс Packing для синхронизации связи
Packing.products = relationship("Product", secondary="product_packing", back_populates="packings")
