from bs4 import BeautifulSoup
from selenium import webdriver

def main(search_term):
    driver = webdriver.Chrome(executable_path='/Users/margheritabonfiglio/Downloads/chromedriver')
    records =[]
    url = get_url(search_term)
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

def get_url(search_term):
    template= "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
    search_term= search_term.replace(' ', '+')

    url = template.format(search_term)
    url+='&page()'
    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        price_parent = item.find('span', 'a-price').text
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        rating = item.i.text

    except AttributeError:
        rating = ''

    result = (description, price, rating, url)

    return result
