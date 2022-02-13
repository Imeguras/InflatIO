from selenium import webdriver
from selenium.webdriver.common.by import By
import api
from datetime import datetime
from sys import stderr
import traceback


<<<<<<< Updated upstream
driver = webdriver.Chrome()
=======
>>>>>>> Stashed changes

def getTimestamp():
  return datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

f = open("errors.txt",'a')
file2 = open("quantities.txt",'a')
def logError(msg,error):
    s = getTimestamp() + msg + str(error)
    print(s, file=stderr)
    print(s, file=f)
    traceback.print_exc()
    traceback.print_exc(file=f)

def continente_urls(driver):
    driver.get("https://continente.pt");
    # ignores "Ver Todos" & broader category links
    linkNodes = driver.find_elements(By.CSS_SELECTOR, "a:not(.dropdown-toggle):not(.ct-font--opensans-italic).dropdown-link")
    urls = []
    for linkNode in linkNodes:
        link = linkNode.get_attribute('href')
        # if nothing after 4th slash,
        # then it's a category link and not a product listing
        if(link.split("/")[4] != ""):
            urls += [link]
    return urls


<<<<<<< Updated upstream
def crawl (driverUrl):
    db = api.db_init()
=======
def crawl (driver, driverUrl):
>>>>>>> Stashed changes
    # continente specific method
    getUrl = lambda page:driverUrl+'?start='+str(page);
    #extracts the category from the url, this could be done up there but it would require an array or memory to be passed on
    cat_section_url = driverUrl.rsplit("/", 2)[1]
    
    driver.implicitly_wait(10)
    elements = []
    page_increment=0;

    # has break below
    while True:
        driver.get(getUrl(page_increment))

        tiles = driver.find_elements(By.CSS_SELECTOR,'.ct-tile-body')
        driver.implicitly_wait(0)
        # found nothing, end of pages
        if(len(tiles) == 0):
            break
       
        page_increment += len(tiles)
        
        for tile in tiles:
            try :
                nameElement = tile.find_elements(By.CSS_SELECTOR,'.ct-tile--description')
                priceElement = tile.find_elements(By.CSS_SELECTOR,'.ct-price-formatted')
                #Elements because its a sneaky way to prevent a failed search, since it may not exist
                discountElements = tile.find_elements(By.CSS_SELECTOR,'.ct-discount-amount')
                quantityElement = tile.find_elements(By.CSS_SELECTOR,'.ct-tile--quantity')
                brandElement= tile.find_elements(By.CSS_SELECTOR,'.ct-tile--brand')
                categoryElement = cat_section_url
                #Url has been "historically" fetched as a hyperlink from clicking the title
                measureKey = quantityElement.text[-2:]
                
                # # In the website the value can be "emb. 50 gr" OR "emb.50 gr"
                # # see https://www.continente.pt/produto/batata-frita-lisa-yorkeso-ruffles-7390758.html for a bad input
                # # can also be "emb. x gr (peso escorrido x )" 
                # rawQuantity = float(quantityElement.text.split(".")[1].split(" ")[1].replace(',','.'))
                # measures={
                #     "lt":(1,'l'),
                #     " L":(1,'l'),
                #     "dl":(10,'l'),
                #     "cl":(100,'l'),
                #     "ml":(1000,'l'),
                #     "kg":(1,'kg'),
                #     "gr":(1000,'kg'),
                #     "un":(1,'un')
                # }
                # data = {
                #     "url": nameElement.get_attribute('href'),
                #     "name": nameElement.text,
                #     "price": priceElement.text[1:].replace(",","."),
                #     #For this website "Desconto Imediato: " precedes the actual discount and it comes in percentage not the decimal value for analitical purposes
                #     "discount": 0 if len(discountElements)==0 else float(discountElements[0].text[19:-1])/100,
                #     #TODO multithreading theres no way the crawler gonna do a switch/if statement for each element when most of the time its gonna be measure in the right measurment
                #     "measure": measures[measureKey][1],
                #     "quantity": rawQuantity/measures[measureKey][0],
                #     "brand": brandElement.text,
                #     "category": categoryElement
                # }
                # elements.append(data)
                # print('collected: '+ str(data))
            except Exception as e:
                logError("tile error, WIP state")
    api.db_ins_entry(db, elements)

def start():
  return {
    "driver" : webdriver.Chrome(executable_path="./driver"),
    "dbconn": api.db_init()
  }
def crawlUrls(driver, filename="./crawlCache/continenteUrls"):
    urls = continente_urls(driver)
    print("urls fetched")
    with open(filename,'w') as f:
          print("\n".join(urls),file=f)

def crawlCachedUrls(driver):
    with open('crawlCache/continenteUrls') as f:
        urls = f.readlines()
        for url in urls:
            crawl(driver,url)

#main()
#driver.close()
