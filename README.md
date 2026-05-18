# Supermarket
## Data Source
### Kaggle
* [Supermarket Sales Data](https://www.kaggle.com/datasets/yapwh1208/supermarket-sales-data?select=annex2.csv)
## Data Cleaning - Python
import pandas
```python
import pandas as pd
```
read the csv files 
```python
items = pd.read_csv('annex1.csv')
sales = pd.read_csv('annex2.csv')
prices = pd.read_csv('annex3.csv')
```
rename the column names in each dataset
> e.g. 'Item Code' --> 'item_code'
```python
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
```
check for any null values in the dataset
```python
print(items.isna().any().any())
print(prices.isna().any().any())
print(sales.isna().any().any())
```
check for any duplicates in the dataset
```python
print(items.duplicated().any())
print(prices.duplicated().any())
print(sales.duplicated().any())
```
save the modified dataset as a new csv file and rename them for readability
> 'annex1.csv' --> 'Items.csv'

> 'annex2.csv' --> 'Sales.csv'

> 'annex3.csv' --> 'Prices.csv'
```python
items.to_csv('Items.csv', index=False)
prices.to_csv('Prices.csv', index=False)
sales.to_csv('Sales.csv', index=False)
```
## Data Structure
### Tables
`Items`
* `item_code` :
  > *unique id of the vegetable*
* `item_name` :
  > name of the vegetable
* `category_code`:
  > id of vegetable category
* `category_name` :
  > name of vegetable category

`Price`
* `date` :
  > date when the supermarket bought the vegetable
* `item_code` :
  > unique id of the vegetable
* `wholesale_price` :
  > price which supermarket bought the vegetable in RMB

`Sales`
* `date` :
  > date when the customer bought the vegetable from supermarket
* `time` :
  > time when the customer bought the vegetable from supermarket
* `item_code` :
  > unique id of the vegetable
* `quantity_sold` :
  > how much of the vegetable was sold in kg at the time of purchase
* `unit_selling_price` :
  > price which customer bought the vegetable in RMB/kg
* `sale_or_return` :
  > if the vegetable was sold or returned back to the supermarket
* `discount` :
  > if vegetable was on discount at the time of purchase

## SQL
### Questions
`How many different vegetables are sold in this supermarket?`
```sql
SELECT
  COUNT(*) AS total_veg
FROM Items
```
`How many different categories of vegetables are there?`
```sql
SELECT
  COUNT(DISTINCT category_code) AS total_categories
FROM Items
```
`What are the sales of each year?`
```sql
SELECT 
    strftime('%Y', date) AS year,
    ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
FROM Sales
GROUP BY strftime('%Y',date)
ORDER BY year
```
```sql
-- For BigQuery you can use:
EXTRACT(YEAR FROM date)
-- instead of:
strftime('%Y', date)
-- which is used in SQLite
```
`What are the sales of each month?`
```sql
SELECT 
    strftime('%Y-%m', date) AS month,
    ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
FROM Sales
GROUP BY strftime('%Y',date), strftime('%m',date)
ORDER BY month
```
`Which year had the most sales?`
```sql
WITH annual_sales AS (
    SELECT 
        strftime('%Y', date) AS year,
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    GROUP BY strftime('%Y',date)
    ORDER BY year
)

SELECT
    year,
    MAX(sales) AS sales
FROM annual_sales
```
`Which year had the least sales?`
```sql
WITH annual_sales AS (
    SELECT 
        strftime('%Y', date) AS year,
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    GROUP BY strftime('%Y',date)
    ORDER BY year
)

SELECT
    year,
    MIN(sales) AS sales
FROM annual_sales
```
`Which month had the most sales?`
```sql
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', date) AS month,
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    GROUP BY strftime('%Y-%m',date)
    ORDER BY month
)

SELECT
    month,
    MAX(sales) AS sales
FROM monthly_sales
```
`Which month had the least sales?`
```sql
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', date) AS month,
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    GROUP BY strftime('%Y-%m',date)
    ORDER BY month
)

SELECT
    month,
    MIN(sales) AS sales
FROM monthly_sales
```
`What are the annual sales for each category?`
```sql
SELECT
    strftime('%Y',date) as year, 
    category_name, 
    ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
FROM Sales
JOIN Items ON Sales.item_code = Items.item_code
GROUP BY strftime('%Y',date), category_name
```
`What are the monthly sales for each category?`
```sql
SELECT
    strftime('%Y-%m',date) AS month, 
    category_name, 
    ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
FROM Sales
JOIN Items ON Sales.item_code = Items.item_code
GROUP BY strftime('%Y-%m',date), category_name
```
`Which category of vegetables had the most sales each year?`
```sql
WITH annual_category_sales AS (
    SELECT 
        strftime('%Y', date) AS year, 
        category_name, 
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code = Items.item_code
    GROUP BY strftime('%Y', date), category_name
)

SELECT 
    year,
    category_name,
    MAX(sales) AS sales
FROM annual_category_sales
GROUP BY year
ORDER BY year
```
`Which category of vegetables had the least sales each year?`
```sql
WITH annual_category_sales AS (
    SELECT 
        strftime('%Y', date) AS year, 
        category_name, 
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code = Items.item_code
    GROUP BY strftime('%Y', date), category_name
)

SELECT 
    year,
    category_name,
    MIN(sales) AS sales
FROM annual_category_sales
GROUP BY year
ORDER BY year
```
`Which category of vegetables had the most sales each month?`
```sql
WITH monthly_category_sales AS (
    SELECT 
        strftime('%Y-%m', date) AS month, 
        category_name, 
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code = Items.item_code
    GROUP BY strftime('%Y-%m', date), category_name
)

SELECT 
    month,
    category_name,
    MAX(sales) AS sales
FROM monthly_category_sales
GROUP BY month
ORDER BY month
```
`Which category of vegetables had the least sales each month?`
```sql
WITH monthly_category_sales AS (
    SELECT 
        strftime('%Y-%m', date) AS month, 
        category_name, 
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code = Items.item_code
    GROUP BY strftime('%Y-%m', date), category_name
)

SELECT 
    month,
    category_name,
    MIN(sales) AS sales
FROM monthly_category_sales
GROUP BY month
ORDER BY month
```
`What are the total sales of all vegetables?`
```sql
SELECT
    item_name,
    ROUND(SUM(quantity_sold*unit_selling_price),2) AS average_sales
FROM Sales
JOIN Items ON Sales.item_code=Items.item_code
GROUP BY item_name
```
`Which vegetable had the highest sales?`
```sql
WITH total_sales AS (
    SELECT
        item_name,
        SUM(quantity_sold*unit_selling_price) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    GROUP BY item_name
)

SELECT item_name, MAX(sales) AS sales FROM total_sales
```
`Which vegetable had the lowest sales?`
```sql
WITH total_sales AS (
    SELECT
        item_name,
        SUM(quantity_sold*unit_selling_price) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    GROUP BY item_name
)

SELECT item_name, MIN(sales) AS sales FROM total_sales
```
`What are the annual profits for each category?`
```sql

```
`What are the monthly profits for each category?`
