from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Measure(Base):
    __tablename__ = 'measures'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('measures_id_seq'::regclass)"))
    measure = Column(Enum('kg', 'l', 'un', name='measure_type'), nullable=False)
    quantity = Column(Float(53), nullable=False)
    def __repr__ (self):
        return "{ id=%s; measure=%s; quantity=%s; }\n" % (self.id, self.measure, self.quantity)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('product_id_seq'::regclass)"))
    url = Column(Text, nullable=False, unique=True)
    date_created = Column(DateTime(True), server_default=text("now()"))
    enabled = Column(Boolean, server_default=text("true"))
    def __repr__ (self):
        return "{ id=%s; url=%s; date_created=%s; enabled=%s }\n" % (self.id, self.url, self.date_created, self.enabled)


t_standard = Table(
    'standard', metadata,
    Column('collectors_id', Integer),
    Column('products_id', Integer),
    Column('measures_id', Integer),
    Column('measures_measure', Enum('kg', 'l', 'un', name='measure_type')),
    Column('collectors_id_product', Integer),
    Column('products_url', Text),
    Column('products_date_created', DateTime(True)),
    Column('measures_quantity', Float(53)),
    Column('collectors_price', Float(53)),
    Column('products_enabled', Boolean),
    Column('collectors_nome', Text),
    Column('collectors_date_collected', DateTime(True)),
    Column('collectors_per_desconto', Float(53)),
    Column('collectors_marca', Text),
    Column('collectors_categoria', Text),
    Column('collectors_measure', Integer)
)


class Collector(Base):
    __tablename__ = 'collectors'

    id = Column(Integer, primary_key=True, server_default=text("nextval('colectors_id_seq'::regclass)"))
    id_product = Column(ForeignKey('products.id'))
    price = Column(Float(53), server_default=text("0"))
    nome = Column(Text)
    date_collected = Column(DateTime(True), server_default=text("now()"))
    per_desconto = Column(Float(53), server_default=text("0"))
    marca = Column(Text)
    categoria = Column(Text)
    measure = Column(ForeignKey('measures.id'), nullable=False)

    product = relationship('Product')
    measure1 = relationship('Measure')
    def __repr__ (self):
        return "{ id=%s; id_product=%s; price=%s; nome=%s; date_collected=%s; per_desconto=%s; marca=%s; categoria=%s; measure=%s }\n" % (self.id, self.id_product, self.price, self.nome, self.date_collected, self.per_desconto, self.marca, self.categoria, self.measure)