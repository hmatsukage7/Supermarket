# Supermarket
## Data Source
### Kaggle
* [Supermarket Sales Data](https://www.kaggle.com/datasets/yapwh1208/supermarket-sales-data?select=annex2.csv)

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
`What is the earliest purchase and the latest purhcase of the supermarket recorded in the dataset?`
```sql
SELECT
  MIN(date) AS earliest_purchase,
  MAX(date) AS latest_purchase
FROM Price
```
`How many vegetables has the supermarket purchased in total?`
```sql
SELECT
  COUNT(*) AS total_purchase
FROM Price
```
`What is the supermarket's total spendage on vegetables?`
```sql
SELECT
  SUM(wholesale_price) AS total_spendage
FROM Price
```
`
