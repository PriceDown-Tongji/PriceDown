# PriceDown

# This is the main function script

import pandas as pd
from tkinter import *
from tkinter import messagebox as msg
from tkinter import simpledialog
from pandastable import Table
from scrap_ebay import search_ebay
from scrap_amazon import search_amazon
import tkinter as tk
# from tkintertable import TableCanvas
# from tkinter import filedialog

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

        # Lists to store the data obtained from websites
        products_names = []
        products_prices = []
        products_urls = []

        if 'amazon' in toSearch_product:
            # Call amazon web scraping function
            search_amazon(products_names, products_prices, products_urls, toSearch_product, selected_country, pages):
            print("Amazon")
        elif 'ebay' in toSearch_product:
            # Call ebay web scraping function
            products_urls = search_ebay(products_names, products_prices, products_urls, toSearch_product, selected_country, pages)
        elif 'alibaba' in toSearch_product:
            # Call alibaba web scraping function
            print("Amazon")
        else:
            # Search the product name through all websites
            products_urls = search_ebay(products_names, products_prices, products_urls, toSearch_product, selected_country, pages)

        products_urls.pop(0) # First element is empty

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
