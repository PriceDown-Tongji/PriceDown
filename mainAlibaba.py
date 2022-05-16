import csv
import requests
import re
import json

import pandas as pd
country= input("Please choose the country for the search:")
product_name= str(input("What product are you searching?"))

template="https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText="
product_name=product_name.replace(" ","+")
pages=input("How many pages of search do you want?")
products_name=[]
products_prices=[]
products_url=[]
f=open("html_file2.txt","a")
for i in range(1,int(pages)+1):
    page="&page="+str(i)+"&f0=y"
    url= template+product_name+page
    html_text=requests.get(url).text

    data = re.search(r"window\.__page__data__config = (\{.*\})", html_text).group(1)
    data = json.loads(data)
    f.write(json.dumps(data, indent=4))

    # uncomment to print all data:
    print(i)
    for offer in data["props"]["offerResultData"]["offerList"]:
        #products_name.append(offer[])
        products_name.append(offer["information"]["puretitle"])
        #price=offer["tradePrice"]["price"]
        price=offer["tradePrice"]["price"].split("$")
        print(price)
        print(offer["information"]["productUrl"])
        if len(price)>=3 :
            products_prices.append(float(price[2]))
        else:
            products_prices.append(float(price[1]))
        #products_prices.append(price)
        products_url.append(offer["information"]["productUrl"])
        #print("{:<20} {}".format(offer["tradePrice"]["price"], offer["information"]["puretitle"]))

    df = pd.DataFrame({"Products":products_name, "Prices": products_prices, "Url":products_url})
    df.to_csv('result.csv')

    """with open('result.csv', 'w') as csvfile:
        fieldnames = ['Prices', 'Product','Url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Prices': products_prices, 'Product': products_name,'Url':products_url})
    f=open("database.txt","w")

    for i in range(len(products_name)):
        f.write(products_name[i])
        f.write(" ")
        f.write(products_prices[i])
        f.write(" ")
        f.write(products_url[i])
        f.write("\n")"""