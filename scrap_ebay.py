# Library for webscraping - Ebay

# Import modules
import requests
from bs4 import BeautifulSoup

# Dictionary to change website url to the corresponding Country
countries = {
    'UNITED STATES': 'com',
    'UNITED KINGDOM': 'co.uk',
    'CANADA': 'ca',
    'GERMANY': 'de',
    'FRANCE': 'fr',
    'JAPAN': 'com',
    'BRAZIL': 'br',
    'AUSTRIA': 'at',
    'ITALY': 'it',
    'SPAIN': 'es',
    'CHINA': 'com',
    'MEXICO': 'com.mx',
    'AUSTRALIA': 'com.au',
    'NETHERLANDS': 'nl',
    'INDIA': 'in'
}

contrystring = {
    'ITALY': 'a',
    'UNITED KINGDOM': 'to',
    'UNITED STATES': 'com',
    'CANADA': 'to',
    'GERMANY': 'bis',
    'FRANCE': 'à',
    'BRAZIL': 'to',
    'AUSTRIA': 'bis',
    'SPAIN': 'a',
    'CHINA': 'to',
    'MEXICO': 'to',
    'AUSTRALIA': 'to',
    'NETHERLANDS': 'to',
    'INDIA': 'to'
}

# Search through ebay
def search_ebay(products_names, products_prices, products_urls, toSearch_product, selected_country, pages):

    # Find if the user input is a link or a name
    if 'ebay.' in toSearch_product:
        # Request url
        response = requests.get(toSearch_product)

        soup = BeautifulSoup(response.text, "html.parser")

        toSearch_product = soup.find('h1', class_ = 'x-item-title__mainTitle').find('span', class_ = 'ux-textspans ux-textspans--BOLD').text

    # Construct the url
    for page in range(1,pages):
        products_urls = []
        ebay_url = f"https://www.ebay.{countries[selected_country]}/sch/i.html?_nkw={toSearch_product}&_pgn={page}"

    # Request url
    response = requests.get(ebay_url)

    soup = BeautifulSoup(response.text, "html.parser")

    tags = soup.findAll('h3', class_ = 's-item__title')
    prices = soup.findAll('span', class_ = 's-item__price')
    links = soup.find_all('a', class_='s-item__link')
    # Get urls
    urls = [item.get('href') for item in links]
    products_urls = products_urls + urls

    sub_str = "a"

    for i in range(1,len(tags)):
        products_names.append(tags[i].text)

        # Get the price and convert it to float

        res = prices[i].text
        if (sub_str in res):
            res = res[:res.index(sub_str) + len(sub_str)].strip(sub_str).replace('EUR','').replace('.','').replace(',','.').strip()
            products_prices.append(float(res))
        else:
            products_prices.append(float(prices[i].text.replace('EUR','').replace('.','').replace(',','.').strip()))
    return products_urls
