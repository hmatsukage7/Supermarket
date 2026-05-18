# Supermarket
## Data Source
### Kaggle
* [Supermarket Sales Data](https://www.kaggle.com/datasets/yapwh1208/supermarket-sales-data?select=annex2.csv)

## Data Structure
### Tables
`Item`: annex1.csv
* `Item Code` :
  > *unique id of the vegetable*
* `Item Name` :
  > name of the vegetable
* `Category Code`:
  > id of vegetable category
* `Category Name` :
  > name of vegetable category

`Price`: annex2.csv
* `Date` :
  > date when the supermarket bought the vegetable
* `Item Code` :
  > unique id of the vegetable
* `Wholesale Price (RMB/kg)` :
  > price which supermarket bought the vegetable

`Sales`: annex3.csv
* `Date` :
  > date when the customer bought the vegetable from supermarket
* `Time` :
  > time when the customer bought the vegetable from supermarket
* `Item Code` :
  > unique id of the vegetable
* `Quantity Sold (kilo)` :
  > how much of the vegetable was sold in kg at the time of purchase
* `Unit Selling Price (RMB/kg)` :
  > price which customer bought the vegetable per kg
* `Sale or Return` :
  > if the vegetable was sold or returned back to the supermarket
* `Discount (Yes/No)` :
  > if vegetable was on discount at the time of purchase

## SQL
