import sqlalchemy as db
from sqlalchemy.orm import Session
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
        for el in elements:
            session.add(models.Product(
                url=el["url"],
                product_name=el["name"],
                price=el["price"],
                per_discount=el["discount"],
                measure_unit=el["measure"],
                measure_value=el["quantity"]))

        session.commit()
        print("Inserted values in products")
    except BaseException as error:
        print("Error: "+str(error))
