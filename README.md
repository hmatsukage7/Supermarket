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
check the datatypes of each table's columns
```python
print(items.info())
print(sales.info())
print(prices.info())
```
`items.info()`

<p align='center'>
<img src='https://i.imgur.com/fYDfKI1.png', alt="items info">

`sales.info()`

<p align='center'>
<img src='https://i.imgur.com/iz1418S.png', width=56% alt="sales info">

`prices.info()`

<p align='center'>
<img src='https://i.imgur.com/bYfWaTS.png', width=56% alt="prices info">


rename the column names in each dataset
> e.g. 'Item Code' --> 'item_code'

```python
# first check the column names
print(f"items_colunm_names: {items.columns.to_list()}")
print(f"saless_colunm_names: {sales.columns.to_list()}")
print(f"prices_colunm_names: {prices.columns.to_list()}")
```
<p align='center'>
<img src='https://i.imgur.com/jzvhVdx.png', alt="column names">


```python
items.columns = items.columns.str.lower().str.replace(' ','_')

sales.columns = sales.columns.str.split('(').str[0]
sales.columns = sales.columns.str.strip().str.lower().str.replace(' ','_')

prices.columns = prices.columns.str.split('(').str[0]
prices.columns = prices.columns.str.strip().str.lower().str.replace(' ','_')
```
<p align='center'>
<img src='https://i.imgur.com/VoDhato.png', alt="cleaned_column_names">


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
the `dataset.zip` file contains the original csv files

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
| Total Vegetables |
| :--------------: |
| 251              |

`How many different categories of vegetables are there?`
```sql
SELECT
  COUNT(DISTINCT category_code) AS total_categories
FROM Items
```
| Total Categories |
| :--------------: |
| 6                |

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
-- instead of:
strftime('%Y', date)
-- which is used in SQLite
-- for BigQuery use:
EXTRACT (YEAR, date)
-- for MySQL use:
YEAR(date)
```
| Year | Sales |
| :--: | :---: |
| 2020 | 669529.27 |
| 2021 | 1100362.65 |
| 2022 | 1036772.4 |
| 2023 | 563102.15 |

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
| Year | Sales |
| :--: | :---: |
| 2021 | 1100362.65 |

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

| Year | Sales |
| :--: | :---: |
| 2023 | 563102.15 |

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
| Year | Sales |
| :--: | :---: |
| 2021-02 | 178817.9 |

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
| Month | Sales |
| :--: | :---: |
| 2022-06 | 52933.36 |

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

`Which category had the most sales each year?`
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
| Year | Category | Sales |
| :--: | :------: | :---: |
| 2020 | Flower/LeafÂ Vegetables | 234438.6 |
| 2021 | Flower/LeafÂ Vegetables | 364896.96 |
| 2022 | Flower/LeafÂ Vegetables | 308505.47 |
| 2023 | Flower/LeafÂ Vegetables | 171228.76 |

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
| Year | Category | Sales |
| :--: | :------: | :---: |
| 2020 | Solanum | 34601.35 |
| 2021 | Solanum | 63201.07 |
| 2022 | Solanum | 58942.91 |
| 2023 | Solanum | 34378.93 |

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
`What are the total sales for all vegetables?`
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
        ROUND(SUM(quantity_sold*unit_selling_price),2) AS sales
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    GROUP BY item_name
)

SELECT item_name, MAX(sales) AS sales FROM total_sales
```
| Vegetable | Sales |
| :-------: | :---: |
| Broccoli | 269880.96 |

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
| Vegetable | Sales |
| :-------: | :---: |
| Needle Mushroom (Bag) | 3.5 |

`What is the net profit of the supermarket?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date, 
        item_name, 
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
)

SELECT
    ROUND(SUM(profit),2) AS net_profit 
FROM price_cost
```
| Net Profit |
| :--------: |
| 1243652.28 |

`What are the annual profits?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date AS date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
)

SELECT
    strftime('%Y', date) AS year,
    ROUND(SUM(profit),2) AS profit
FROM price_cost
GROUP BY strftime('%Y', date)
```
| Year | Profit |
| :--: | :----: |
| 2020 | 248392.67 |
| 2021 | 389863.53 |
| 2022 | 398194.89 |
| 2023 | 207201.2 |

`What are the monthly profits?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date AS date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
)

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(SUM(profit),2) AS profit
FROM price_cost
GROUP BY strftime('%Y-%m', date)
```
`Which year did the supermarket make the most profit?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date AS date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
),
annual_profit AS (
    SELECT
        strftime('%Y', date) AS year,
        ROUND(SUM(profit),2) AS profit
    FROM price_cost
    GROUP BY strftime('%Y', date)
),

monthly_profit AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        ROUND(SUM(profit),2) AS profit
    FROM price_cost
    GROUP BY strftime('%Y-%m', date)
)

SELECT
    year,
    MAX(profit) AS profit
FROM annual_profit
```
| Year | Profit |
| :--: | :----: |
| 2022 |398194.89 |

`Which month did the supermarket make the most profit?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date AS date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
),
annual_profit AS (
    SELECT
        strftime('%Y', date) AS year,
        ROUND(SUM(profit),2) AS profit
    FROM price_cost
    GROUP BY strftime('%Y', date)
),

monthly_profit AS (
    SELECT
        strftime('%Y-%m', date) AS month,
        ROUND(SUM(profit),2) AS profit
    FROM price_cost
    GROUP BY strftime('%Y-%m', date)
)

SELECT
    month,
    MAX(profit) AS profit
FROM monthly_profit
```
`What are the profits of each vegetable?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date, 
        item_name,
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
)

SELECT
    item_name,
    SUM(profit) AS profit
FROM price_cost
GROUP BY item_name
```
`What are the profits of each category?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
)

SELECT
    category_name,
    SUM(profit) AS profit
FROM price_cost
GROUP BY category_name
```
`How many of vegetables made a profit and how many did not?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
),
veg_profit AS (
    SELECT 
        item_name,
        SUM(profit) AS profit
    FROM price_cost
    GROUP BY item_name
)

SELECT 
    SUM(CASE WHEN profit >= 0 THEN 1 ELSE 0 END) AS count_profit,
    SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS count_loss
FROM veg_profit
```
`How many categories made a profit and how many did not?`
```sql
WITH price_cost AS (
    SELECT
        Sales.date, 
        item_name, 
        category_name,
        quantity_sold, 
        unit_selling_price, 
        wholesale_price,
        quantity_sold*unit_selling_price AS sales,
        quantity_sold*wholesale_price AS costs,
        quantity_sold*unit_selling_price-quantity_sold*wholesale_price AS profit
    FROM Sales
    JOIN Items ON Sales.item_code=Items.item_code
    LEFT JOIN Prices ON Sales.item_code=Prices.item_code AND Sales.date=Prices.date
),
category_profit AS (
    SELECT 
        category_name,
        SUM(profit) AS profit
    FROM price_cost
    GROUP BY category_name
)

SELECT 
    SUM(CASE WHEN profit >= 0 THEN 1 ELSE 0 END) AS count_profit,
    SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS count_loss
FROM category_profit
```
