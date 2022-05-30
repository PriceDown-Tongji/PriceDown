import codecs
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup


#Dictionary to change website url to the corresponding url
COUNTRIES_ALIBABA={"ITALY": "italian",
          "GERMANY": "german",
          "FRANCE": "french",
          "NETHERLANDS":"dutch",
          "JAPAN": "japanese",
          "SPAIN": "spanish", 
          "CHINA": "chinese",
          "RUSSIA":"russian",
          "KOREA": "korean",
          "INDONESIA": "indonesian",
          "THAILANDIA": "thai"}

#input from user
def search_alibaba(products_names, products_prices, products_urls, toSearch_product, selected_country, pages):
    
    # Find if the user input is a link or a name
    if "alibaba." in toSearch_product:
        response = requests.get(toSearch_product)

        soup = BeautifulSoup(response.text, "html.parser")

        toSearch_product = soup.find('h1', class_ = 'module-pdp-title').text

    #initial contruct of the url
    if selected_country=="china":
        template= "https://chinese.alibaba.com/trade/search?&language=zh&fsb=y&IndexArea=product_en&CatId=&SearchText="
    elif  selected_country not in COUNTRIES_ALIBABA:
        template="https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText="
    else:
        template="https://"+ COUNTRIES_ALIBABA[selected_country]+".alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText="
    
    toSearch_product=toSearch_product.replace(" ","+")
    products_urls.append(0)
    #construction of url according to pade
    for i in range(pages): 
        page_number="&page="+str(i)+"&f0=y"
        url= template+toSearch_product+page_number
        #request to url
        html_text=requests.get(url).text
        try:
            data = re.search(r"window\.__page__data__config = (\{.*\})", html_text).group(1)
            data = json.loads(data)
        #appending the elements of the products to the lists
            for offer in data["props"]["offerResultData"]["offerList"]:
                products_names.append(offer["information"]["puretitle"])
                price=offer["promotionInfoVO"]["originalPriceTo"]
                products_prices.append(float(price))
                products_urls.append(offer["information"]["productUrl"])
        except:
            print(f"There are only {i+1} pages")
            break
