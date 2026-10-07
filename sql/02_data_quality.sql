-- ==============================================================================
-- EVPulse India: Data Quality & Referential Integrity Verification
-- Script: 02_data_quality.sql
-- Purpose: Rigorous automated tests verifying row counts, constraints, foreign keys,
--          and cross-table consistency between Python and SQL.
-- ==============================================================================

-- Test 1: Record Counts in Dimensions and Facts
SELECT 'dim_date' AS table_name, COUNT(*) AS row_count, 36 AS expected_count FROM dim_date
UNION ALL
SELECT 'dim_state', COUNT(*), 34 FROM dim_state
UNION ALL
SELECT 'dim_category', COUNT(*), 2 FROM dim_category
UNION ALL
SELECT 'dim_maker', COUNT(*), 26 FROM dim_maker
UNION ALL
SELECT 'fact_state_sales', COUNT(*), 2445 FROM fact_state_sales
UNION ALL
SELECT 'fact_maker_sales', COUNT(*), 816 FROM fact_maker_sales;

-- Test 2: Reconciliation of Nationwide EV Sales Between Fact Tables
-- MUST EQUAL ZERO DISCREPANCY (Both must be exactly 2,066,111 units)
SELECT 
    state_total.ev_sold_state,
    maker_total.ev_sold_maker,
    (state_total.ev_sold_state - maker_total.ev_sold_maker) AS discrepancy
FROM 
    (SELECT SUM(electric_vehicles_sold) AS ev_sold_state FROM fact_state_sales) state_total,
    (SELECT SUM(electric_vehicles_sold) AS ev_sold_maker FROM fact_maker_sales) maker_total;

-- Test 3: Reconciliation by Vehicle Category
SELECT 
    c.category_name,
    COALESCE(s.ev_state, 0) AS ev_state,
    COALESCE(m.ev_maker, 0) AS ev_maker,
    (COALESCE(s.ev_state, 0) - COALESCE(m.ev_maker, 0)) AS diff
FROM dim_category c
LEFT JOIN (
    SELECT category_id, SUM(electric_vehicles_sold) AS ev_state
    FROM fact_state_sales
    GROUP BY category_id
) s ON c.category_id = s.category_id
LEFT JOIN (
    SELECT category_id, SUM(electric_vehicles_sold) AS ev_maker
    FROM fact_maker_sales
    GROUP BY category_id
) m ON c.category_id = m.category_id;

-- Test 4: Check for Null Values Across Crucial Business Columns
SELECT 'fact_state_sales' AS entity, COUNT(*) AS null_violations
FROM fact_state_sales
WHERE date IS NULL OR state_id IS NULL OR category_id IS NULL 
   OR electric_vehicles_sold IS NULL OR total_vehicles_sold IS NULL
UNION ALL
SELECT 'fact_maker_sales', COUNT(*)
FROM fact_maker_sales
WHERE date IS NULL OR maker_id IS NULL OR category_id IS NULL 
   OR electric_vehicles_sold IS NULL;

-- Test 5: Referential Integrity Check (Orphaned Foreign Keys)
SELECT 'Orphan state_id in fact_state_sales' AS test_name, COUNT(*) AS violations
FROM fact_state_sales f
LEFT JOIN dim_state s ON f.state_id = s.state_id
WHERE s.state_id IS NULL
UNION ALL
SELECT 'Orphan date in fact_state_sales', COUNT(*)
FROM fact_state_sales f
LEFT JOIN dim_date d ON f.date = d.date
WHERE d.date IS NULL
UNION ALL
SELECT 'Orphan maker_id in fact_maker_sales', COUNT(*)
FROM fact_maker_sales f
LEFT JOIN dim_maker m ON f.maker_id = m.maker_id
WHERE m.maker_id IS NULL
UNION ALL
SELECT 'Orphan category_id in fact_maker_sales', COUNT(*)
FROM fact_maker_sales f
LEFT JOIN dim_category c ON f.category_id = c.category_id
WHERE c.category_id IS NULL;

-- Test 6: Non-Negative Value Checks and Logical Bounds
SELECT 
    COUNT(CASE WHEN electric_vehicles_sold < 0 THEN 1 END) AS negative_ev_sales,
    COUNT(CASE WHEN total_vehicles_sold < 0 THEN 1 END) AS negative_total_sales,
    COUNT(CASE WHEN non_electric_vehicles_sold < 0 THEN 1 END) AS negative_non_ev_sales,
    COUNT(CASE WHEN ev_penetration_rate_pct < 0.0 OR ev_penetration_rate_pct > 100.0 THEN 1 END) AS invalid_penetration_rate
FROM fact_state_sales;
