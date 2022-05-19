#library for web scraping Amazon

#import libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

countries = {
        'UNITED STATES': 'com',
        'UNITED KINGDOM': 'co.uk',
        'CANADA': 'ca',
        'GERMANY': 'de',
        'FRANCE': 'fr',
        'JAPAN': 'co.jp',
        'BRAZIL': 'br',
        'AUSTRIA': 'at',
        'ITALY': 'it',
        'SPAIN': 'es',
        'CHINA': 'cn',
        'MEXICO': 'com.mx',
        'AUSTRALIA': 'com.au',
        'NETHERLANDS': 'nl',
        'INDIA': 'in'
    }

#get the website templates for the different countries
def get_template(country):
    template = 'https://www.amazon.{}/'
    country = country.upper()
    if country not in countries:
        template = 'https://www.amazon.com/'
    else:
        template = template.format(countries[country])
    return template

#get the url for the searched product
def get_url(search_term, template):
    template += "s?k={}"
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page={}'
    return url

#gets the searched term if the input is an url
def get_search_term(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if 'ebay' in url:
        search_term = soup.find('input', class_='gh-tb ui-autocomplete-input')
    elif 'alibaba' in url:
        search_term = soup.find('input', class_='ui-searchbar-keyword')
    elif 'amazon' in url:
        search_term = soup.find('input', id_='twotabsearchtextbox')
    else:
        return 'No word found'
    return search_term.get('value')

#transforms the price into float
def get_float(price, symbol):
    price_float = price.replace('.', '')
    price_float = price_float.replace(',', '.').strip(symbol)
    price_float = float(price_float)
    return price_float

#main function
def scrap_amazon(products_names, products_prices, products_urls, toSearch_product, selected_country, pages):
    #identifies if the input is a url or a word
    if '/' in toSearch_product:
        toSearch_product = get_search_term(toSearch_product)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    template = get_template(selected_country)
    url = get_url(toSearch_product, template)
    names = []
    prices = []
    links = []
    #goes through all the pages
    for page in range(1, pages):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        #extrapolate the information for every single product
        for item in results:
            #tries to get the name, price, url infomations and does not write the info in the dictionary if there are errors
            try:
                price_parent = item.find('span', 'a-price')
                symbol = price_parent.find('span', 'a-price-symbol').text
                price = price_parent.find('span', 'a-offscreen').text
                products_prices.append(get_float(price, symbol))
                name = item.find('span', 'a-size-base-plus a-color-base a-text-normal')
                if not name:
                    name = item.find('span', 'a-size-medium a-color-base a-text-normal')
                products_names.append(name.text)
                items = item.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
                try:
                    products_urls.append(template+items.get('href'))
                except IndexError:
                    products_urls.append('No link available')
            except AttributeError:
                print('Attribute error')
    
   #writes the information on the csv file
    open('web_scrap_amazon.csv', 'w', newline='', encoding ='utf-8')
    df = pd.DataFrame({'Products': names, 'Prices': prices, 'Links': links})
    sorted_df=df.sort_values('Prices', ascending=True, na_position='last')
    sorted_df.to_csv('web_scrap_amazon.csv')
    driver.close()
