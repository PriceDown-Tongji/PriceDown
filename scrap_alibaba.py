import sys
import codecs
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup


#Dictionary to change website url to the corresponding url
COUNTRIES={"italy": "italian","germany": "german","france": "french","netherlands":"dutch","japan": "japanese","spain": "spanish", "china": "chinese",
            "russia":"russian","korea": "korean","indonesia": "indonesian", "thailandia": "thai"}

#input from user
def search():
    country= input("Please choose the country for the search: ").lower()
    product_name= str(input("What product are you searching? "))
    elements=int(input("How many elements do you want?(MAX 50) "))
    sorting=int(input("How do you want to sort the search?\n0 No sorting\n1 Lowest\n2 Highest\n"))

    #initial contruct of the url
    if country=="china":
        template= "https://chinese.alibaba.com/trade/search?&language=zh&fsb=y&IndexArea=product_en&CatId=&SearchText="
    elif  country not in COUNTRIES:
        template="https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText="
    else:
        template="https://"+ COUNTRIES[country]+".alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText="
    product_name=product_name.replace(" ","+")

    #list for the elements of the products
    products_name=[]
    products_prices=[]
    products_url=[]
    page=0

    f=open("html_file2.txt","w")
    i=0
    while i< elements:
        page_number="&page="+str(page)+"&f0=y"
        url= template+product_name+page_number
        print(url)
        #request to url
        html_text=requests.get(url).text
        data = re.search(r"window\.__page__data__config = (\{.*\})", html_text).group(1)
        data = json.loads(data)

        # uncomment to print html file:
        f.write(json.dumps(data, indent=4))

        #appending the elements of the products to the lists
        for offer in data["props"]["offerResultData"]["offerList"]:
            #products_name.append(offer[])
            products_name.append(offer["information"]["puretitle"])
            price=offer["promotionInfoVO"]["originalPriceTo"]
            products_prices.append(float(price))
            products_url.append(offer["information"]["productUrl"])
            print(offer["information"]["puretitle"])
            i+=1
            if i>=elements:
                break
        page+=1

    #csv file and sorting the csv file
    df = pd.DataFrame({"Products":products_name, "Prices": products_prices, "Url":products_url})
    final_df=df
    if sorting==1:
        final_df=df.sort_values(by=["Prices"])
    if sorting ==2:
        final_df=df.sort_values(by=["Prices"], ascending=False)
    final_df.to_csv('result.csv', index=False, encoding='utf-8-sig')


def link():
    link=input()
    if "alibaba" not in link:
        return 0
    link=link.split("/")[4]
    link=link.split("_")[0]
    link=link.replace("-"," ")
    print(link)
