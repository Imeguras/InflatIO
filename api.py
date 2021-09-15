import psycopg2
from config import dbconfig
def db_init():
    conn = None
    try:
        print("Connecting to database...")
        params = dbconfig()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print("Database version: ")
        print(db_version)
        cur.close()
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
def collectors_format(collector, id):
    return "', '".join("('"+str(id[0])+collector["name"]+str(collector["price"])+str(collector["discount"])+")"

def db_ins_entry(conn, elements):
    try:
        cur = conn.cursor()
        links = ", ".join(list(map(lambda info: "('"+info["url"]+"')",elements)))
        cur.execute('Insert into products (url) Values'+links+' on conflict do nothing RETURNING id;')
        #A list that stores the response given by sql after filling the first table, this returns the id's of url's incremented and designated by product_id_seq
        Aydis = cur.fetchall()
        print(Aydis)
        extracted = ", ".join(list(map(collectors_format, elements, Aydis)))
        print(extracted)
        #TODO change ***everything*** from portuguese to english unless its not open to the public 
        cur.execute('insert into collectors(id_product,nome,price,per_desconto) values '+  extracted)
        #cur.execute('Insert into products (product_id, name, price, discount) Values('+extracted+')')
        conn.commit()
        
        print("Inserted values in products")
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error: "+str(error))
    

def db_terminate(conn):
    try:
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
