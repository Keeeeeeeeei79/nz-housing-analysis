"""Load cleaned data into DuckDB and run SQL analysis."""
import duckdb
import pandas as pd
from pathlib import Path

con = duckdb.connect("housing.duckdb")

# CSVをDuckDBに読み込む
con.execute("""
    CREATE OR REPLACE TABLE stg_housing AS
    SELECT * FROM read_csv_auto('data/clean/hm10_clean.csv')
""")

# 確認
print(con.execute("SELECT COUNT(*) FROM stg_housing").fetchone())
print(con.execute("SELECT * FROM stg_housing LIMIT 5").df())

# staging モデルを作る
con.execute("""
    CREATE OR REPLACE TABLE stg_housing_clean AS
""" + open('sql/stg_housing.sql').read())

print("staging model created")
print(con.execute("""
    SELECT quarter_date, year, quarter, hpi, house_sales
    FROM stg_housing_clean
    LIMIT 5
""").df().to_string())

# marts モデル
con.execute("""
    CREATE OR REPLACE TABLE mart_housing_kpi AS
""" + open('sql/mart_housing_kpi.sql').read())

print("marts model created")
print(con.execute("""
    SELECT quarter_date, hpi, hpi_yoy_pct, hpi_rolling_4q, sales_yoy_pct
    FROM mart_housing_kpi
    WHERE year >= 2020
    ORDER BY quarter_date
""").df().to_string())