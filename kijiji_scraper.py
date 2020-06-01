from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

I_DONT_WANT_IT = ['entourage', 'Entourage', 'Rondo', 'rondo', 
            'cube', 'Cube', 'MPV', 'mpv', 'Montana', 'montana'
            'Voyager', 'voyager', 'Oldsmobile', 'oldsmobile', 'RAM', 
            'ram', 'Ram', 'Durango', 'Dakota', 'dakota', 'Suzuki', 
            'suzuki', 'Sienna', 'sienna', 'corolla', 'Corolla',
            'Previa', 'previa', 'Routan', 'routan', 'rav4', 'RAV4',
            'odyssey', 'Odyssey', 'Rio', 'Accent', 'Cruze',
            'cruze', 'escalade', 'Escalade', 'Malibu', 'malibu',
            'Sierra', 'sierra', 'Silverado', 'freestar', 'Freestar',
            'CRV', 'crv', 'caravan', 'Caravan', 'Patriot', 'GMC',
            'MDX', 'RDX', 'Cobalt', 'Cavalier', 'Journey', 'Quest',
            'Tribute', 'Yaris', 'yaris', 'Equinox', 'Elantra',
            'Versa', 'Escape', 'Veracruz', 'Sonata', 'STS', 
            'Grand', 'Yukon', 'HHR', 'Pathfinder', 'F150', 'CR-V',
            'Camry', 'accent', 'patriot', 'E350', 'E250', 'silverado',
            'deville', 'Deville', 'Uplander', 'uplander', 'Suburban',
            'Liberty', 'minivan', 'Rogue', 'Edge', 'Santa Fe',
            'Fusion', 'Traverse', 'Buick', 'Prius', 'Sunfire']
            
IDONTWANTOMETER = 0


a_url = 'https://www.kijiji.ca/b-cars-trucks/alberta/new__used/page-'
b_url = '/c174l9003a49?price-type=fixed&price=1500__8000&for-sale-by=ownr'

filename = "kijiji_scrape.csv"
f = open(filename, "w+")
header = "BRAND, PRICE, LOCATION, DETAILS, LINK \n"
f.write(header)


for i in range(1,10):
    my_url = a_url + str(i) + b_url

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class":"info-container"})

    for container in containers:
        brand_container = container.findAll("div", {"class":"title"})
        brand = brand_container[0].text.strip()
        

        for model in I_DONT_WANT_IT:
            if model in brand:
                IDONTWANTOMETER = 1
        if IDONTWANTOMETER == 1:
            print('found match ' + brand + ', skipping...')
            IDONTWANTOMETER = 0
            continue

        price_container = container.findAll("div", {"class":"price"})
        price = price_container[0].text.strip()

        link_container = brand_container[0].a["href"]
        link = "https://www.kijiji.ca" + link_container

        details_container = container.findAll("div", {"class":"details"})
        details = details_container[0].text.replace('\n','').replace(' ','')

        location_container = container.findAll("div", {"class":"location"})
        location = location_container[0].text.replace('\n', '').replace(' ','')

    
        print("BRAND: " + brand)
        print("PRICE: " + price)
        print("DETAILS: " + details)
        print("LOCATION: " + location)
        print("LINK: " + link)
        print('\n')

        f.write(brand.replace('\n', '').replace(',', '|') + ',' + price.replace(',','.') + ',' + details.replace(',','.') + ',' + location + ',' + link + '\n')

    f.write('\n')

f.close()