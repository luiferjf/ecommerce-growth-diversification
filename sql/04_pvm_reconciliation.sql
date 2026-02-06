/*
===============================================================================
SCRIPT NAME:     04_pvm_reconciliation.sql
DESCRIPTION:    Performs the Price-Volume-Mix (PVM) Bridge calculation in SQL.
                Reconciles the 2021 vs 2022 growth drivers.
AUTHOR:         Luis Fernando Jordan
===============================================================================
*/

WITH annual_metrics AS (
    SELECT 
        YEAR(o.order_created_utc) as report_year,
        SUM(oi.quantity) as total_units,
        SUM(oi.line_total) as total_revenue,
        SUM(oi.line_total) / SUM(oi.quantity) as asp
    FROM fact_order_items oi
    JOIN fact_orders o ON oi.order_id = o.order_id
    WHERE o.status_canonical IN ('paid', 'completed')
      AND YEAR(o.order_created_utc) IN (2021, 2022)
    GROUP BY YEAR(o.order_created_utc)
),
comparison AS (
    SELECT 
        y21.total_revenue as rev_21,
        y22.total_revenue as rev_22,
        y21.total_units as units_21,
        y22.total_units as units_22,
        y21.asp as asp_21,
        y22.asp as asp_22
    FROM annual_metrics y21
    JOIN annual_metrics y22 ON y21.report_year = 2021 AND y22.report_year = 2022
)
SELECT 
    '2021 vs 2022' as period,
    rev_21,
    rev_22,
    (rev_22 - rev_21) as total_delta,
    -- Volume Effect: (Vol22 - Vol21) * Price21
    (units_22 - units_21) * asp_21 as volume_impact,
    -- Price Effect: (Price22 - Price21) * Vol22
    (asp_22 - asp_21) * units_22 as price_impact,
    -- Sanity Check (Should be 0)
    ROUND((units_22 - units_21) * asp_21 + (asp_22 - asp_21) * units_22 - (rev_22 - rev_21), 2) as reconciliation_diff
FROM comparison;
