"""
Task 3: Data Analysis with Pandas
-------------------------------------
Goal: Demonstrate data analysis skills using Pandas.

This script demonstrates:
    1. Loading and inspecting a CSV dataset
    2. Cleaning missing / incorrect data
    3. Filtering, grouping, and aggregation
    4. Explaining insights in simple words

Dataset: data/sales_data.csv (a small, intentionally messy sales dataset
containing missing quantities, missing unit prices, and a missing order date)

Author: <Your Name>
"""

import pandas as pd

DATA_PATH = "data/sales_data.csv"
CLEANED_OUTPUT = "data/sales_data_cleaned.csv"


def load_and_inspect(path):
    """Load the CSV and print basic inspection info."""
    df = pd.read_csv(path)
    print("=" * 70)
    print("STEP 1: LOAD & INSPECT")
    print("=" * 70)
    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns\n")
    print("Column info:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nMissing values per column:")
    print(df.isna().sum())
    return df


def clean_data(df):
    """
    Clean the dataset:
        - Fill missing 'quantity' with the median quantity (a sensible default)
        - Fill missing 'unit_price' with the median price for that product
        - Drop rows where 'order_date' is missing (date is essential, can't be guessed)
    """
    print("\n" + "=" * 70)
    print("STEP 2: CLEAN DATA")
    print("=" * 70)

    df = df.copy()

    # Fill missing quantity with the overall median quantity
    median_qty = df["quantity"].median()
    missing_qty = df["quantity"].isna().sum()
    df["quantity"] = df["quantity"].fillna(median_qty)
    print(f"\n[OK] Filled {missing_qty} missing 'quantity' values with median = {median_qty}")

    # Fill missing unit_price using the median price *for that same product*
    missing_price = df["unit_price"].isna().sum()
    df["unit_price"] = df.groupby("product")["unit_price"].transform(
        lambda s: s.fillna(s.median())
    )
    print(f"[OK] Filled {missing_price} missing 'unit_price' values using per-product median")

    # Drop rows with a missing order_date (can't reliably infer a date)
    missing_dates = df["order_date"].isna().sum()
    df = df.dropna(subset=["order_date"])
    print(f"[OK] Dropped {missing_dates} row(s) with missing 'order_date'")

    # Correct data types
    df["quantity"] = df["quantity"].astype(int)
    df["order_date"] = pd.to_datetime(df["order_date"])

    print(f"\nCleaned shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("Missing values remaining:")
    print(df.isna().sum())

    return df


def analyze_data(df):
    """Apply filtering, grouping, and aggregation; return computed insights."""
    print("\n" + "=" * 70)
    print("STEP 3: FILTER, GROUP & AGGREGATE")
    print("=" * 70)

    # Add a computed 'total_amount' column
    df["total_amount"] = df["quantity"] * df["unit_price"]

    # --- Filtering: orders above the average order value ---
    avg_order_value = df["total_amount"].mean()
    big_orders = df[df["total_amount"] > avg_order_value]
    print(f"\nAverage order value: ${avg_order_value:.2f}")
    print(f"Orders above average ({len(big_orders)} of {len(df)}):")
    print(big_orders[["order_id", "customer", "region", "total_amount"]])

    # --- Grouping & aggregation: revenue by region ---
    revenue_by_region = (
        df.groupby("region")["total_amount"]
        .agg(["sum", "mean", "count"])
        .rename(columns={"sum": "total_revenue", "mean": "avg_order_value", "count": "num_orders"})
        .sort_values("total_revenue", ascending=False)
    )
    print("\nRevenue by region:")
    print(revenue_by_region)

    # --- Grouping & aggregation: sales by product ---
    sales_by_product = (
        df.groupby("product")
        .agg(total_qty_sold=("quantity", "sum"), total_revenue=("total_amount", "sum"))
        .sort_values("total_revenue", ascending=False)
    )
    print("\nSales by product:")
    print(sales_by_product)

    # --- Top customer by spend ---
    top_customers = (
        df.groupby("customer")["total_amount"].sum().sort_values(ascending=False).head(3)
    )
    print("\nTop 3 customers by total spend:")
    print(top_customers)

    return df, revenue_by_region, sales_by_product, top_customers


def print_insights(revenue_by_region, sales_by_product, top_customers):
    """Explain the findings in simple, plain-English terms."""
    print("\n" + "=" * 70)
    print("STEP 4: INSIGHTS (in simple words)")
    print("=" * 70)

    top_region = revenue_by_region.index[0]
    top_product = sales_by_product.index[0]
    top_customer = top_customers.index[0]

    print(f"""
1. {top_region} is the strongest region, bringing in the most total revenue.
   This suggests marketing or restocking efforts could focus here first.

2. {top_product} is the best-selling product by revenue. It's worth checking
   that we always have enough stock of this item.

3. {top_customer} is the top-spending customer. Repeat customers like this
   are good candidates for loyalty offers or personalized outreach.

4. Some rows had missing quantity/price, which we filled using sensible
   medians, and one row was missing its order date entirely, so we removed
   it since a sale without a date can't be trusted for time-based reporting.
""")


def main():
    df = load_and_inspect(DATA_PATH)
    clean_df = clean_data(df)
    clean_df, revenue_by_region, sales_by_product, top_customers = analyze_data(clean_df)
    print_insights(revenue_by_region, sales_by_product, top_customers)

    clean_df.to_csv(CLEANED_OUTPUT, index=False)
    print(f"\n[OK] Cleaned dataset saved to {CLEANED_OUTPUT}")
    print("\n[DONE] Data analysis task complete.")


if __name__ == "__main__":
    main()
