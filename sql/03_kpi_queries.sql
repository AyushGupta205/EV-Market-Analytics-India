-- ==============================================================================
-- EVPulse India: Core Business KPI Metrics Layer
-- Script: 03_kpi_queries.sql
-- Purpose: Defines and calculates primary high-level executive and analytical KPIs.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- KPI 1: High-Level Executive Summary Metrics
-- ------------------------------------------------------------------------------
WITH national_aggregates AS (
    SELECT 
        SUM(electric_vehicles_sold) AS total_ev_registrations,
        SUM(total_vehicles_sold) AS total_automotive_registrations,
        ROUND((CAST(SUM(electric_vehicles_sold) AS REAL) / SUM(total_vehicles_sold)) * 100.0, 2) AS overall_penetration_rate_pct
    FROM fact_state_sales
),
charging_aggregate AS (
    SELECT SUM(operational_pcs) AS total_operational_pcs FROM dim_state
),
entity_counts AS (
    SELECT 
        (SELECT COUNT(*) FROM dim_state) AS total_states,
        (SELECT COUNT(*) FROM dim_maker) AS total_oems,
        (SELECT COUNT(DISTINCT date) FROM dim_date) AS total_months
)
SELECT 
    na.total_ev_registrations,
    na.total_automotive_registrations,
    na.overall_penetration_rate_pct,
    ca.total_operational_pcs,
    ROUND(CAST(na.total_ev_registrations AS REAL) / ca.total_operational_pcs, 1) AS evs_per_charging_station,
    ec.total_states,
    ec.total_oems,
    ec.total_months
FROM national_aggregates na
CROSS JOIN charging_aggregate ca
CROSS JOIN entity_counts ec;

-- ------------------------------------------------------------------------------
-- KPI 2: Fiscal Year Volume, YoY Growth & CAGR
-- ------------------------------------------------------------------------------
WITH yearly_trend AS (
    SELECT 
        d.fiscal_year,
        d.fiscal_year_label,
        SUM(f.electric_vehicles_sold) AS ev_sold,
        SUM(f.total_vehicles_sold) AS total_sold,
        ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) * 100.0, 2) AS penetration_pct
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.fiscal_year, d.fiscal_year_label
),
growth_calc AS (
    SELECT 
        fiscal_year,
        fiscal_year_label,
        ev_sold,
        total_sold,
        penetration_pct,
        LAG(ev_sold) OVER (ORDER BY fiscal_year) AS prev_year_ev_sold,
        ROUND(((CAST(ev_sold AS REAL) - LAG(ev_sold) OVER (ORDER BY fiscal_year)) 
               / LAG(ev_sold) OVER (ORDER BY fiscal_year)) * 100.0, 2) AS yoy_growth_pct
    FROM yearly_trend
)
SELECT 
    fiscal_year_label,
    ev_sold,
    total_sold,
    penetration_pct,
    COALESCE(prev_year_ev_sold, 0) AS prev_year_ev_sold,
    COALESCE(yoy_growth_pct, 0.0) AS yoy_growth_pct
FROM growth_calc;

-- ------------------------------------------------------------------------------
-- KPI 3: Vehicle Category Split (Volume & Share)
-- ------------------------------------------------------------------------------
SELECT 
    c.category_name,
    SUM(f.electric_vehicles_sold) AS total_ev_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales)) * 100.0, 2) AS market_share_pct,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) * 100.0, 2) AS category_penetration_pct
FROM fact_state_sales f
JOIN dim_category c ON f.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_ev_sold DESC;

-- ------------------------------------------------------------------------------
-- KPI 4: Market Leaders in Key Segments
-- ------------------------------------------------------------------------------
-- Leading 2W OEM
SELECT 
    'Leading 2-Wheeler OEM' AS kpi_name,
    m.maker_name AS leader_name,
    SUM(f.electric_vehicles_sold) AS units_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_maker_sales WHERE category_id = 1)) * 100.0, 2) AS segment_share_pct
FROM fact_maker_sales f
JOIN dim_maker m ON f.maker_id = m.maker_id
WHERE f.category_id = 1
GROUP BY m.maker_name
ORDER BY units_sold DESC
LIMIT 1;

-- Leading 4W OEM
SELECT 
    'Leading 4-Wheeler OEM' AS kpi_name,
    m.maker_name AS leader_name,
    SUM(f.electric_vehicles_sold) AS units_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_maker_sales WHERE category_id = 2)) * 100.0, 2) AS segment_share_pct
FROM fact_maker_sales f
JOIN dim_maker m ON f.maker_id = m.maker_id
WHERE f.category_id = 2
GROUP BY m.maker_name
ORDER BY units_sold DESC
LIMIT 1;

-- Leading State by Volume
SELECT 
    'Leading State by EV Volume' AS kpi_name,
    s.state_name AS leader_name,
    SUM(f.electric_vehicles_sold) AS total_ev_registrations,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales)) * 100.0, 2) AS national_volume_share_pct
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name
ORDER BY total_ev_registrations DESC
LIMIT 1;

-- Leading State by Penetration Rate (Minimum 100,000 Total Registrations)
SELECT 
    'Leading State by Penetration Rate' AS kpi_name,
    s.state_name AS leader_name,
    SUM(f.electric_vehicles_sold) AS total_ev_sold,
    SUM(f.total_vehicles_sold) AS total_automotive_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) * 100.0, 2) AS penetration_rate_pct
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name
HAVING SUM(f.total_vehicles_sold) >= 100000
ORDER BY penetration_rate_pct DESC
LIMIT 1;
