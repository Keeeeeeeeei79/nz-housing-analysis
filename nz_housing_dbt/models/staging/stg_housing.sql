SELECT
    CAST(date AS DATE)                            AS quarter_date,
    EXTRACT(year FROM CAST(date AS DATE))         AS year,
    EXTRACT(quarter FROM CAST(date AS DATE))      AS quarter,
    CAST(house_sales AS INTEGER)                  AS house_sales,
    CAST(hpi AS INTEGER)                          AS hpi,
    CAST(housing_stock_NZDm AS INTEGER)           AS housing_stock_NZDm,
    CAST(housing_stock_NZDm AS INTEGER) * 1000000 AS housing_stock_dollars,
    CAST(residential_investment_NZDm AS INTEGER)  AS residential_investment_NZDm
FROM {{ source('raw', 'raw_housing') }}