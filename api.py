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


def db_ins_entry(conn, urlList):
    try:
        cur = conn.cursor()
        values = ", ".join(list(map(lambda url: "('"+url+"')",urlList)))
        cur.execute('Insert into products (url) Values '+values+' on conflict do nothing;')
        conn.commit()
        print("Inserted values in products")
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error: "+str(error))
    

