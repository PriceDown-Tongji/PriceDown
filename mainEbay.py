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
pages = int(input("How many pages do you want to analyze? "))

products_names = []
products_prices = []
products_urls = []

# Construct the url
for page in range(1,pages):
    ebay_url = f"https://www.ebay.{countries[selected_country]}/sch/i.html?_nkw={toSearch_product}&_pgn={page}"

    # ebay_url = f"https://www.ebay.{countries[selected_country]}/sch/{toSearch_product}"

    # Request url
    response = requests.get(ebay_url)

    soup = BeautifulSoup(response.text, "html.parser")

    tags = soup.findAll('h3', class_ = 's-item__title')
    prices = soup.findAll('span', class_ = 's-item__price')
    links = soup.find_all('a', class_='s-item__link')
    # Get urls
    urls = [item.get('href') for item in links]
    products_urls = products_urls + urls
    products_urls.pop(0)

    sub_str = "a"

    for i in range(1,len(tags)):
        products_names.append(tags[i].text)

        # Get the price and convert it to float

        res = prices[i].text
        if ('a' in res):
            res = res[:res.index(sub_str) + len(sub_str)].strip("a").replace('EUR','').replace('.','').replace(',','.').strip()
            products_prices.append(float(res))
        else:
            products_prices.append(float(prices[i].text.replace('EUR','').replace('.','').replace(',','.').strip()))

# Put all the results in a csv file
df = pd.DataFrame({"Products":products_names, "Prices": products_prices, "Link": products_urls})
# Sorting results
sorted_df=df.sort_values(by=["Prices"])
sorted_df.to_csv('results.csv')

# Ask user for a feedback
feedback = input("What's your experience with our system:")
