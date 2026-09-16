SELECT
    quarter_date,
    year,
    quarter,
    hpi,
    house_sales,
    housing_stock_NZDm,
    residential_investment_NZDm,

    -- 前年同期比（YoY）
    LAG(hpi, 4) OVER (ORDER BY quarter_date) AS hpi_prev_year,

    ROUND(
        (hpi - LAG(hpi, 4) OVER (ORDER BY quarter_date))
        / LAG(hpi, 4) OVER (ORDER BY quarter_date) * 100,
        1
    ) AS hpi_yoy_pct,

    -- 4四半期移動平均
    ROUND(AVG(hpi) OVER (
        ORDER BY quarter_date
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ), 1) AS hpi_rolling_4q,

    -- 売買件数YoY
    ROUND(
        (house_sales - LAG(house_sales, 4) OVER (ORDER BY quarter_date))
        / LAG(house_sales, 4) OVER (ORDER BY quarter_date) * 100,
        1
    ) AS sales_yoy_pct

FROM {{ ref('stg_housing') }}
ORDER BY quarter_date