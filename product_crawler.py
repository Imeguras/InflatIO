from selenium import webdriver 
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
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def crawl ():
    driver = webdriver.Chrome(executable_path="./driver")

    
    url = lambda page:'https://www.continente.pt/mercearia/arroz-massa-e-farinha/arroz/?start='+str(page);

    driver.implicitly_wait(10)

    page_increment=0;
    while True:
        driver.get(url(page_increment))
        elements = driver.find_elements_by_css_selector('.ct-tile--description')
        listings = []
        # found nothing, end of page
        if(len(elements)==0):
            break;
        page_increment += len(elements)
        for e in elements:
            listinglink = e.get_attribute('href')
            listings.append(listinglink)
            print('collected: '+listinglink)
    
crawl()

