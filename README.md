# Python ETL Projects

A collection of beginner Data Engineering projects built while learning Python, Pandas, and ETL concepts.

## Projects

### 01 — Core Python ETL

A simple ETL pipeline built using Python's built-in CSV module.

**Skills practiced:**

* CSV reading and writing
* Python dictionaries
* Functions
* Error handling with `try/except`
* Data validation
* Data aggregation
* Basic ETL design

**Pipeline:**

```text
CSV → Extract → Clean → Transform → Aggregate → CSV
```

### 02 — Pandas ETL

An ETL pipeline using Pandas for data cleaning, transformation, aggregation, and analysis.

**Skills practiced:**

* Pandas
* Data cleaning
* `pd.to_numeric()`
* `dropna()`
* Calculated columns
* `groupby()`
* `agg()`
* Filtering
* `to_csv()`
* Reusable transformation functions

**Pipeline:**

```text
CSV → Extract → Clean → Transform → Analyze → Load
```

## Learning Progression

The projects demonstrate my progression from implementing ETL using core Python to using Pandas for more efficient data transformation and analysis.

## Technologies

* Python
* Pandas
* CSV
* GitHub

## Next Steps

Planned learning and projects:

1. SQL + Python integration
2. PostgreSQL
3. Data pipelines
4. Cloud fundamentals
5. End-to-end Data Engineering project

# Python ETL Sales Pipeline

A beginner-level Data Engineering project using Python and Pandas to build a simple ETL pipeline from raw sales data.

## Project Overview

This project reads sales data from a CSV file, cleans invalid records, performs transformations and aggregations using Pandas, identifies the top customer, and saves the results into CSV files.

## ETL Pipeline

```text
sales.csv
    ↓
Extract
    ↓
Clean invalid data
    ↓
Transform
    ↓
Aggregate customer sales
    ↓
Analyze top customer
    ↓
Load results
    ↓
customer_sales.csv
top_customer.csv
```

## Technologies Used

* Python
* Pandas
* CSV
* GitHub

## Data Cleaning

The input data contains an invalid value in the `quantity` column.

Pandas is used to convert the column to numeric values:

```python
df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)
```

Invalid values are converted to `NaN` and removed:

```python
df = df.dropna(subset=["quantity"]).copy()
```

## Transformations

The pipeline:

1. Reads the sales CSV.
2. Converts quantity to numeric.
3. Removes invalid records.
4. Calculates `total_amount`.
5. Groups sales by customer.
6. Calculates total sales and order count.
7. Filters customers with sales greater than 300.
8. Identifies the customer(s) with the highest sales.
9. Writes the transformed data to CSV files.

## Output Files

### `customer_sales.csv`

Contains customer-level aggregated sales:

* `customer_id`
* `total_sales`
* `total_orders`

### `top_customer.csv`

Contains the customer(s) with the highest total sales after transformation.

## Key Pandas Concepts Practiced

* `pd.read_csv()`
* `pd.to_numeric()`
* `dropna()`
* Creating calculated columns
* `groupby()`
* `agg()`
* `reset_index()`
* `query()`
* Boolean filtering
* `to_csv()`
* Functions
* Basic ETL design

## What I Learned

This project helped me practice the basic structure of a Data Engineering workflow:

**Extract → Transform → Analyze → Load**

It also introduced practical data-quality handling and reusable transformation functions using Pandas.
