#PiceDown

import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msg
from tkinter import simpledialog
from pandastable import Table
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkintertable import TableCanvas

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

class csv_to_excel:

    def __init__(self, root):

        self.root = root
        self.file_name = ''
        self.f = Frame(self.root,
                       height = 200,
                       width = 300)

        # Place the frame on root window
        self.f.pack()

        # Creating label widgets
        self.message_label = Label(self.f,
                                   text = 'PriceDown',
                                   font = ('Arial', 19,'underline'),
                                   fg = 'Green')
        self.message_label2 = Label(self.f,
                                    text = 'Find a product at the lowest price!',
                                    font = ('Arial', 14,'underline'),
                                    fg = 'Red')

        # Buttons
        self.convert_button = Button(self.f,
                                     text = 'Search a Product',
                                     font = ('Arial', 14),
                                     bg = 'Orange',
                                     fg = 'Black',
                                     command = self.search_product)
        self.display_button = Button(self.f,
                                     text = 'Review',
                                     font = ('Arial', 14),
                                     bg = 'Green',
                                     fg = 'Black',
                                     command = self.review_system)
        self.exit_button = Button(self.f,
                                  text = 'Exit',
                                  font = ('Arial', 14),
                                  bg = 'Red',
                                  fg = 'Black',
                                  command = root.destroy)

        # Placing the widgets using grid manager
        self.message_label.grid(row = 1, column = 1)
        self.message_label2.grid(row = 2, column = 1)
        self.convert_button.grid(row = 3, column = 0,
                                 padx = 0, pady = 15)
        self.display_button.grid(row = 3, column = 1,
                                 padx = 10, pady = 15)
        self.exit_button.grid(row = 3, column = 2,
                              padx = 10, pady = 15)

    def search_product(self):
        # Input from user

        ROOT = tk.Tk()

        ROOT.withdraw()

        # the input dialog
        toSearch_product = simpledialog.askstring(title="Product",
                                 prompt="What's the name of the product?:").replace(" ","+").strip() # Replace space with + for the url composition
        selected_country = simpledialog.askstring(title="Country",
                                 prompt="Enter the name of the country:").upper()
        pages = int(simpledialog.askstring(title="Pages",
                                 prompt="How many pages do you want to scrap?:"))

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

        try:
            self.file_name = 'results.csv'

            df = pd.read_csv(self.file_name)

            # Next - Pandas DF to Excel file on disk
            if(len(df) == 0):
                msg.showinfo('No Rows Selected', 'CSV has no rows')
            else:

                # saves in the current directory
                with pd.ExcelWriter('result.xls') as writer:
                    df.to_excel(writer,'Products found')
                    writer.save()

        except FileNotFoundError as e:
            msg.showerror('Error in opening file', e)

        # Display result
        try:
            self.file_name = 'result.xls'
            df = pd.read_excel(self.file_name)

            if (len(df)== 0):
                msg.showinfo('No records', 'No records')
            else:
                pass

            # Now display the DF in 'Table' object
            # under'pandastable' module
            self.f2 = Frame(self.root, height=200, width=300)
            self.f2.pack(fill=BOTH,expand=1)
            self.table = Table(self.f2, dataframe=df,read_only=True)
            self.table.show()

        except FileNotFoundError as e:
            print(e)
            msg.showerror('Error in opening file',e)

    def review_system(self):

        ROOT = tk.Tk()

        ROOT.withdraw()

        user_review = simpledialog.askstring(title="Feedback",
                                 prompt="How was your experience with our system?:")

        # Print it on a file containing all the reviews
        file1 = open("reviews.txt", "a")  # append mode
        file1.write(user_review)
        file1.close()


# Driver Code
root = Tk()
root.title('PriceDown')

obj = csv_to_excel(root)
root.geometry('800x600')
root.mainloop()
