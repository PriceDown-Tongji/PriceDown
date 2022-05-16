# PirceDown - Ebay

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Dictionary to change website url to the corresponding Country
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

# Input from user
selected_country = input("Insert the country of the website: ").upper()
toSearch_product = input("Insert the name of the product you want to find: ").replace(" ","+").strip() # Replace space with + for the url composition

# Construct the url
ebay_url = f"https://www.ebay.{countries[selected_country]}/sch/{toSearch_product}"

# Request url
response = requests.get(ebay_url)

soup = BeautifulSoup(response.text, "html.parser")

tags = soup.findAll('h3', class_ = 's-item__title')
prices = soup.findAll('span', class_ = 's-item__price')
urls = soup.findAll('a', class_ = 's-item__link')



products_names = []
products_prices = []
products_url = []

for i in range(1,len(tags)):
    products_names.append(tags[i].text)
    products_prices.append(float(prices[i].text.replace('EUR','').replace('.','').replace(',','.').strip()))
    products_url.append(urls[i].text)

print(products_url) # debug

# df = pd.DataFrame(products_names, columns=["Product name"])
df = pd.DataFrame({"Products":products_names, "Prices": products_prices, "Link": products_url})

df.to_csv('results.csv')
