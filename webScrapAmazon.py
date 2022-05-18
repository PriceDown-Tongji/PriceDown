from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def get_template(country):
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
    template = 'https://www.amazon.{}/'
    country = country.upper()
    template = template.format(countries[country])
    return template

def get_url(search_term, template):
    template+= "s?k={}"
    search_term= search_term.replace(' ', '+')

    url = template.format(search_term)
    url+='&page='
    return url
def get_search_term(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if 'ebay' in url:
        search_term = soup.find('input', class_='gh-tb ui-autocomplete-input')
    elif 'alibaba' in url:
        search_term = soup.find('input', class_='ui-searchbar-keyword')
    else: return 'No word found'
    return search_term.get('value')
def get_float(price):
    price_float = price.replace('.', '')
    price_float = price_float.replace(',', '.')

    return price_float

def main():
    search = input('Are you searching with a link or a word: ')
    if search == 'link':
        url= input('Please input link: ')
        search_term = get_search_term(url)
    else:
        search_term = input('Please input the product you are looking for: ')
    country = input('Please input your country: ')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    template = get_template(country)
    url = get_url(search_term, template)
    names = []
    prices = []
    links = []
    for page in range(1, 6):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            try:
                price_parent = item.find('span', 'a-price')
                price = price_parent.find('span', 'a-offscreen').text
                prices.append(get_float(price))
            except AttributeError:
                prices.append('price not found')
            name = soup.find('span', class_='a-size-medium a-color-base a-text-normal')
            if len(name) == 0:
                name = soup.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            names.append(name.text)

            items = item.find('a', class_= 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            try:
                links.append(template+items.get('href'))
            except IndexError:
                links.append('No link available')


    open('web_scrap_amazon.csv', 'w', newline='', encoding ='utf-8')
    df = pd.DataFrame({'Products': names, 'Prices': prices, 'Links': links})
    sorted_df=df.sort_values('Prices', ascending=True, na_position='last')
    sorted_df.to_csv('web_scrap_amazon.csv')
    driver.close()


main()







