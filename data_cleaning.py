import pandas as pd

#read the csv files
items = pd.read_csv('annex1.csv')
sales = pd.read_csv('annex2.csv')
prices = pd.read_csv('annex3.csv')

# renaming the columns in all table to match standard naming convention for SQL
items.rename(columns={'Item Code': 'item_code', 'Item Name': 'item_name', 
                      'Category Code': 'category_code', 'Category Name': 'category_name'}, 
                      inplace=True)

sales.rename(columns={'Date': 'date', 'Time': 'time', 'Item Code': 'item_code', 
                       'Quantity Sold (kilo)': 'quantity_sold', 
                       'Unit Selling Price (RMB/kg)': 'unit_selling_price', 
                       'Sale or Return': 'sale_or_return', 'Discount (Yes/No)': 'discount'}, inplace=True)

prices.rename(columns={'Date': 'date', 'Item Code': 'item_code', 
                      'Wholesale Price (RMB/kg)': 'wholesale_price'}, 
                      inplace=True)

# check for any null value
print(items.isna().any().any())
print(prices.isna().any().any())
print(sales.isna().any().any())

# check for any duplicates
print(items.duplicated().any())
print(prices.duplicated().any())
print(sales.duplicated().any())

# save each dataset as a new csv file and rename them for readability
# set the index parameter in the to_csv function to prevent a new column of index being created
items.to_csv('Items.csv', index=False)
prices.to_csv('Prices.csv', index=False)
sales.to_csv('Sales.csv', index=False)


