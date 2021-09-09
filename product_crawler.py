from selenium import webdriver 
from config import dbconfig
import api


def crawl ():
    driver = webdriver.Chrome(executable_path="./driver")

    
    getUrl = lambda page:'https://www.continente.pt/mercearia/arroz-massa-e-farinha/arroz/?start='+str(page);
    #TODO calculate latency at the time [its a joke]
    driver.implicitly_wait(10)
    urls = []
    page_increment=0;
    while True:
        driver.get(getUrl(page_increment))

        tiles = driver.find_elements_by_css_selector('.ct-tile-body')
        driver.implicitly_wait(0)
        # found nothing, end of page
        if(len(tiles)==0):
            
            break;
        
       
        page_increment += len(tiles)
        
        for tile in tiles:
            nameElement = tile.find_element_by_css_selector('.ct-tile--description')
            priceElement = tile.find_element_by_css_selector('.ct-price-formatted')
            #Elements because its a sneaky way to prevent a failed search, since it may not exist
            discountElements = tile.find_elements_by_css_selector('.ct-discount-amount')
            quantityElement = tile.find_element_by_css_selector('.ct-tile--quantity')
            #Url has been "historically" fetched as a hyperlink from clicking the title
            measureKey = quantityElement.text[-2:]
            rawQuantity = float(quantityElement.text.split()[1].replace(',','.'))
            measures={
                "lt":(1,'l'),
                "dl":(10,'l'),
                "cl":(100,'l'),
                "ml":(1000,'l'),
                "kg":(1,'kg'),
                "gr":(1000,'kg'),
                "un":(1,'un')
            }
            data = {
                "url": nameElement.get_attribute('href'),
                "name": nameElement.text,
                "price": priceElement.text[1:],
                #For this website "Desconto Imediato: " precedes the actual discount and it comes in percentage not the decimal value for analitical purposes
                "discount": 0 if len(discountElements)==0 else float(discountElements[0].text[19:-1])/100,
                #TODO multithreading theres no way the crawler gonna do a switch/if statement for each element when most of the time its gonna be measure in the right measurment
                "measure": measures[measureKey][1],
                "quantity": rawQuantity/measures[measureKey][0]
            }
            
            #print(data)
            #urls.append(url)
            print('collected: '+ str(data))
    driver.close()
    #api.db_ins_entry(api.db_init(), urls)    
    

crawl()

