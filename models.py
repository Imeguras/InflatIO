# coding: utf-8
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, server_default=text("nextval('products_id_seq'::regclass)"))
    url = Column(String, nullable=False)
    date_created = Column(DateTime(True), nullable=False, server_default=text("now()"))
    product_name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(Float(53), nullable=False)
    per_discount = Column(Float(53))
    measure_value = Column(Float(53), nullable=False)
    measure_unit = Column(Enum('kg', 'l', 'un', name='measure_type'), nullable=False)

