from selenium import webdriver
import api

driver = webdriver.Chrome(executable_path="./driver")


def continente_urls():
    driver.get("https://continente.pt");

    # ignores "Ver Todos" & broader category links
    linkNodes = driver.find_elements_by_css_selector("a:not(.dropdown-toggle):not(.ct-font--opensans-italic).dropdown-link")
    urls = []
    for linkNode in linkNodes:
        link = linkNode.get_attribute('href')
        # if nothing after 4th slash,
        # then it's a category link and not a product listing
        if(link.split("/")[4] != ""):
            urls += [link]
    return urls


def crawl (driverUrl):
    # continente specific method
    getUrl = lambda page:driverUrl+'?start='+str(page);

    driver.implicitly_wait(10)
    elements = []
    page_increment=0;

    # has break below
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

            # In the website the value can be "emb. 50 gr" OR "emb.50 gr"
            # see https://www.continente.pt/produto/batata-frita-lisa-yorkeso-ruffles-7390758.html for a bad input
            # can also be "emb. x gr (peso escorrido x )" 
            rawQuantity = float(quantityElement.text.split(".")[1].split(" ")[1].replace(',','.'))
            measures={
                "lt":(1,'l'),
                " L":(1,'l'),
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
                "price": priceElement.text[1:].replace(",","."),
                #For this website "Desconto Imediato: " precedes the actual discount and it comes in percentage not the decimal value for analitical purposes
                "discount": 0 if len(discountElements)==0 else float(discountElements[0].text[19:-1])/100,
                #TODO multithreading theres no way the crawler gonna do a switch/if statement for each element when most of the time its gonna be measure in the right measurment
                "measure": measures[measureKey][1],
                "quantity": rawQuantity/measures[measureKey][0]
            }
            elements.append(data)
            print('collected: '+ str(data))

    api.db_ins_entry(api.db_init(), elements)


def main():
    urls = continente_urls()
    print("urls fetched")
    for url in urls:
        crawl(url)


main()
driver.close()
