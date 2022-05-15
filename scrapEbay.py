# PirceDown - Ebay
import requests
from bs4 import BeautifulSoup
import pandas as pd

ebay_url = 'https://www.ebay.com/sch/crime+books'
response = requests.get(ebay_url)

soup = BeautifulSoup(response.text, "html.parser")

tags = soup.findAll('h3', class_ = 's-item__title')
prices = soup.findAll('span', class_ = 's-item__price')
urls = soup.findAll(class_ = 's-item__link')



products_names = []
products_prices = []
products_url = []

for i in range(1,len(tags)):
    products_names.append(tags[i].text)
    products_prices.append(prices[i].text)
    products_url.append(urls[i].text)

print(products_url)

df = pd.DataFrame(products_names, columns=["Product name"])
df.to_csv('results.csv')
