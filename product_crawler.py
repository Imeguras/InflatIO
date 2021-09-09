from selenium import webdriver 
from config import dbconfig
import api
def crawl ():
    driver = webdriver.Chrome(executable_path="./driver")

    
    getUrl = lambda page:'https://www.continente.pt/mercearia/arroz-massa-e-farinha/arroz/?start='+str(page);

    driver.implicitly_wait(10)
    urls = []
    page_increment=0;
    while True:
        driver.get(getUrl(page_increment))
        elements = driver.find_elements_by_css_selector('.ct-tile--description')
       
        # found nothing, end of page
        if(len(elements)==0):
            break;
        page_increment += len(elements)
        for e in elements:
            url = e.get_attribute('href')
            urls.append(url)
            print('collected: '+url)
    driver.close()
    api.db_ins_entry(api.db_init(), urls)    
    

crawl()

