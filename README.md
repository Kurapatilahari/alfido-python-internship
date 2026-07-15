# Task 3: Data Analysis with Pandas

## Goal
Demonstrate data analysis skills using Pandas.

## What This Script Does
- Loads and inspects a CSV dataset (`data/sales_data.csv`)
- Cleans missing/incorrect data (missing quantity, missing price, missing date)
- Applies filtering, grouping, and aggregation
- Explains the resulting insights in plain English
- Saves the cleaned dataset to `data/sales_data_cleaned.csv`

## Setup
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python3 data_analysis.py
```

## Dataset
`data/sales_data.csv` is a small, intentionally messy sales dataset (15 orders)
with a few missing values built in, so the cleaning step has real work to do:
- 2 rows missing `quantity`
- 1 row missing `unit_price`
- 1 row missing `order_date`

## Sample Output (abridged)
```
STEP 1: LOAD & INSPECT
Shape: 15 rows x 7 columns
Missing values per column:
quantity      2
unit_price    1
order_date    1

STEP 2: CLEAN DATA
[OK] Filled 2 missing 'quantity' values with median = 4.0
[OK] Filled 1 missing 'unit_price' values using per-product median
[OK] Dropped 1 row(s) with missing 'order_date'
Cleaned shape: 14 rows x 7 columns

STEP 3: FILTER, GROUP & AGGREGATE
Revenue by region:
        total_revenue  avg_order_value  num_orders
region
West            338.5       112.83               3
East            292.5        73.13               4
South           279.0        69.75               4
North           148.5        49.50               3

STEP 4: INSIGHTS (in simple words)
1. West is the strongest region, bringing in the most total revenue...
2. Widget A is the best-selling product by revenue...
3. Bob Smith is the top-spending customer...
4. Missing values were filled using medians; the row with no order date
   was removed since it can't be trusted for time-based reporting.
```

## Key Concepts Demonstrated
| Concept | Where |
|---|---|
| Loading/inspecting | `load_and_inspect()` — `pd.read_csv`, `.head()`, `.isna().sum()` |
| Cleaning | `clean_data()` — `.fillna()` with median, per-group fill, `.dropna()` |
| Filtering | `analyze_data()` — orders above the average value |
| Grouping/aggregation | `.groupby()` with `.agg()` for region, product, and customer summaries |
| Insights | `print_insights()` — plain-English takeaways from the numbers |
