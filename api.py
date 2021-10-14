import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import models as models


def db_init():
    # conn = None
    try:
        print("Connecting to database...")
        params = dbconfig()
        print(params)
        engine = db.create_engine(f'postgresql://{params["user"]}:{params["password"]}@{params["host"]}:{params["port"]}/{params["database"]}')

        return Session(engine)

        #    connection = engine.connect()
    except BaseException as error:
        print(error)

def db_ins_entry(session, elements):
    try:
        products = [models.Product(url=el.url) for el in elements]
        # merge with db, creates or gets with ids
        products = map(session.merge, products)

        measures = [models.Measure(measure=el.measure, quantity=el.quantity)
                    for el in elements]
        map(session.add, measures)

        collectors = []
        for index, measure in enumerate(measures):
            product = products[index]
            element = elements[index]
            collectors.append(
                models.Collector(
                    product = product,
                    measure1 = measure,
                    name = element["name"]
                    price = element["price"]
                    #this is still in portuguese ffs
                    per_desconto = element["discount"]
                )

        map(session.add, collectors)
        session.commit()
        print("Inserted values in products")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: "+str(error))

db_init()
