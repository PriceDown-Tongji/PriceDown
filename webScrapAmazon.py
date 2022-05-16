from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def get_url(search_term):
    template= "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
    search_term= search_term.replace(' ', '+')

    url = template.format(search_term)
    url+='&page()'
    return url


def main(search_term):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = get_url(search_term)
    names = []
    prices = []
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        name = soup.findAll('span', class_='a-size-medium a-color-base a-text-normal')
        price = soup.findAll('span', class_='a-price')
        for i in range(1, len(name)):
            names.append(name[i].text)
            prices.append(price[i].text)
    driver.close()

    open('web_scrap_amazon.csv', 'w', newline='', encoding ='utf-8')
    df = pd.DataFrame({'names': names,
                   'prices': prices})
    df.to_csv('web_scrap_amazon.csv')


main("")



