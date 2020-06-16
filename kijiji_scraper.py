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
            'Versa', 'Escape', 'Veracruz', 'Sonata', 'STS', 'F-150', 
            'Grand', 'Yukon', 'HHR', 'Pathfinder', 'F150', 'CR-V',
            'Camry', 'accent', 'patriot', 'E350', 'E250', 'silverado',
            'deville', 'Deville', 'Uplander', 'uplander', 'Suburban',
            'Liberty', 'minivan', 'Rogue', 'Edge', 'Santa Fe', 'grand',
            'Fusion', 'Traverse', 'Buick', 'Prius', 'Sunfire', 
            'Highlander', '4Runner', 'Tacoma', 'Sebring', 'f150',
            'ELANTRA', 'spectra', 'compass', 'Spectra']
            
IDONTWANTOMETER = 0

I_REALLY_WANT_IT = ['335', 'Evo', 'evo', 'G35S', 'g35', 'G35',
                    'Aristo', 'jdm', 'JDM', 'Jdm', 'S4', 's4',
                    '535', '540', '550', '545', 'e36', 'E36',
                    'STI', 'sti', 'STi', 'Supra', '335i', '335xi',
                    '535i', '535xi', 'MazdaSpeed', 'MAZDASPEED',
                    'Mazdaspeed3', 'Mazdaspeed6', 'MazdaSpeed3',
                    'MazdaSpeed6', 'WRX', 'TT', 'skyline', 'GTI',
                    'Skyline', 'Mustang', '350z', 'LS400', 'LS430',
                    'IS250', 'IS350', 'is350', 'is250', 'ls430',
                    'GLI', '20th Anniversary', '20th anniversary',
                    'GT-S', 'GTS', 'Saab', '240sx', '540i', '545i',
                    '550i', 'wrx', '530i', '530', 'Type S', 'type S',
                    'type-s', 'Type-S', 'Genesis', 'Legacy', 'legacy',
                    'type s', 'gts']

IWANTOMETER = 0

a_url = 'https://www.kijiji.ca/b-cars-trucks/alberta/new__used/page-'
b_url = '/c174l9003a49?price-type=fixed&price=1500__8000&for-sale-by=ownr'


# main file containing most ads
filename = "kijiji_scrape.csv"
f = open(filename, "w+")
header = "BRAND, PRICE, DETAILS, LOCATION, LINK \n"
f.write(header)

# secondary file containing the ones matching I_REALLY_WANT_IT
secondary = "peak_interest.csv"
s = open(secondary, "w+")
s.write(header)


for i in range(1,15):
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
        # skip the models that I don't want
        if IDONTWANTOMETER == 1:
            print('Found bad match ' + brand + ', skipping... \n')
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

        for model in I_REALLY_WANT_IT:
            if model in brand:
                IWANTOMETER = 1
        if IWANTOMETER == 1:
            s.write(brand.replace('\n', '').replace(',', '|') + ',' + price.replace(',','.') + ',' + details.replace(',','.') + ',' + location + ',' + link + '\n')
            print('Found good match ' + brand + ', adding to peak_interest... \n')
            IWANTOMETER = 0
        else:
            f.write(brand.replace('\n', '').replace(',', '|') + ',' + price.replace(',','.') + ',' + details.replace(',','.') + ',' + location + ',' + link + '\n')

    s.write('\n')
    f.write('\n')

f.close()
s.close()