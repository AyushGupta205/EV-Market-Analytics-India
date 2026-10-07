-- ==============================================================================
-- EVPulse India: Advanced Business & Strategic SQL Analysis
-- Script: 04_business_analysis.sql
-- Description: 27 Comprehensive Analytical Queries utilizing CTEs, Window Functions
--              (RANK, DENSE_RANK, LAG, LEAD, Cumulative Totals), and Aggregations.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Total Nationwide EV Registrations & Macro Automotive Share
-- ------------------------------------------------------------------------------
SELECT 
    SUM(electric_vehicles_sold) AS total_ev_registrations,
    SUM(total_vehicles_sold) AS total_automotive_registrations,
    SUM(non_electric_vehicles_sold) AS total_ice_registrations,
    ROUND((CAST(SUM(electric_vehicles_sold) AS REAL) / SUM(total_vehicles_sold)) * 100.0, 3) AS national_penetration_rate_pct
FROM fact_state_sales;

-- ------------------------------------------------------------------------------
-- QUERY 2: Fiscal Year Volume & Year-over-Year (YoY) Growth Trajectory
-- ------------------------------------------------------------------------------
WITH yearly_agg AS (
    SELECT 
        d.fiscal_year,
        d.fiscal_year_label,
        SUM(f.electric_vehicles_sold) AS ev_sold,
        SUM(f.total_vehicles_sold) AS total_sold
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.fiscal_year, d.fiscal_year_label
)
SELECT 
    fiscal_year_label,
    ev_sold,
    total_sold,
    ROUND((CAST(ev_sold AS REAL) / total_sold) * 100.0, 2) AS penetration_pct,
    LAG(ev_sold) OVER (ORDER BY fiscal_year) AS prev_year_ev_sold,
    ROUND(((CAST(ev_sold AS REAL) - LAG(ev_sold) OVER (ORDER BY fiscal_year)) 
           / LAG(ev_sold) OVER (ORDER BY fiscal_year)) * 100.0, 2) AS yoy_ev_growth_pct
FROM yearly_agg;

-- ------------------------------------------------------------------------------
-- QUERY 3: Monthly Trajectory with 3-Month Moving Average (Trend Smoothing)
-- ------------------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        d.year_month,
        d.date,
        SUM(f.electric_vehicles_sold) AS monthly_ev_sold
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.year_month, d.date
)
SELECT 
    year_month,
    monthly_ev_sold,
    ROUND(AVG(monthly_ev_sold) OVER (
        ORDER BY date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 1) AS moving_avg_3m,
    LAG(monthly_ev_sold, 1) OVER (ORDER BY date) AS prev_month_ev,
    ROUND(((CAST(monthly_ev_sold AS REAL) - LAG(monthly_ev_sold, 1) OVER (ORDER BY date)) 
           / NULLIF(LAG(monthly_ev_sold, 1) OVER (ORDER BY date), 0)) * 100.0, 2) AS mom_growth_pct
FROM monthly_sales
ORDER BY date;

-- ------------------------------------------------------------------------------
-- QUERY 4: Quarterly Performance and Quarter-on-Quarter (QoQ) Growth
-- ------------------------------------------------------------------------------
WITH quarterly_data AS (
    SELECT 
        d.fiscal_year,
        d.quarter,
        d.fiscal_quarter_label,
        SUM(f.electric_vehicles_sold) AS quarterly_ev_sold
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.fiscal_year, d.quarter, d.fiscal_quarter_label
)
SELECT 
    fiscal_quarter_label,
    quarterly_ev_sold,
    LAG(quarterly_ev_sold) OVER (ORDER BY fiscal_year, quarter) AS prev_quarter_ev,
    ROUND(((CAST(quarterly_ev_sold AS REAL) - LAG(quarterly_ev_sold) OVER (ORDER BY fiscal_year, quarter))
           / LAG(quarterly_ev_sold) OVER (ORDER BY fiscal_year, quarter)) * 100.0, 2) AS qoq_growth_pct
FROM quarterly_data
ORDER BY fiscal_year, quarter;

-- ------------------------------------------------------------------------------
-- QUERY 5: State-Wise Total EV Registrations & National Market Contribution %
-- ------------------------------------------------------------------------------
SELECT 
    s.state_name,
    s.region,
    SUM(f.electric_vehicles_sold) AS state_ev_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales)) * 100.0, 2) AS contribution_to_india_pct
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY state_ev_sold DESC;

-- ------------------------------------------------------------------------------
-- QUERY 6: Top 10 States by EV Registration Volume
-- ------------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(f.electric_vehicles_sold) DESC) AS rank,
    s.state_name,
    s.region,
    SUM(f.electric_vehicles_sold) AS total_ev_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales)) * 100.0, 2) AS market_share_pct
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY rank
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 7: Bottom 10 States / Union Territories by EV Registrations
-- ------------------------------------------------------------------------------
SELECT 
    ROW_NUMBER() OVER (ORDER BY SUM(f.electric_vehicles_sold) ASC) AS rank,
    s.state_name,
    s.region,
    SUM(f.electric_vehicles_sold) AS total_ev_sold
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY total_ev_sold ASC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 8: State EV Penetration Rate Ranking (Adoption Efficiency)
-- ------------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY (CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) DESC) AS penetration_rank,
    s.state_name,
    s.region,
    SUM(f.electric_vehicles_sold) AS ev_sold,
    SUM(f.total_vehicles_sold) AS total_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) * 100.0, 2) AS ev_penetration_rate_pct
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name, s.region
ORDER BY penetration_rank;

-- ------------------------------------------------------------------------------
-- QUERY 9: Regional Aggregations (Macro Zone Analysis)
-- ------------------------------------------------------------------------------
SELECT 
    s.region,
    COUNT(DISTINCT s.state_id) AS total_states_in_region,
    SUM(f.electric_vehicles_sold) AS regional_ev_sold,
    SUM(f.total_vehicles_sold) AS regional_total_vehicles,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales)) * 100.0, 2) AS regional_share_of_india_pct,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) * 100.0, 2) AS regional_penetration_rate_pct
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.region
ORDER BY regional_ev_sold DESC;

-- ------------------------------------------------------------------------------
-- QUERY 10: Cumulative Running Total of Nationwide EV Registrations
-- ------------------------------------------------------------------------------
WITH monthly_trend AS (
    SELECT 
        d.date,
        d.year_month,
        SUM(f.electric_vehicles_sold) AS monthly_sales
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.date, d.year_month
)
SELECT 
    year_month,
    monthly_sales,
    SUM(monthly_sales) OVER (ORDER BY date) AS cumulative_ev_sales,
    ROUND((CAST(SUM(monthly_sales) OVER (ORDER BY date) AS REAL) / 2066111.0) * 100.0, 2) AS cumulative_progress_pct
FROM monthly_trend
ORDER BY date;

-- ------------------------------------------------------------------------------
-- QUERY 11: Fastest-Growing States (FY 2022 to FY 2024 Compound Growth)
-- ------------------------------------------------------------------------------
WITH state_fy AS (
    SELECT 
        s.state_name,
        SUM(CASE WHEN d.fiscal_year = 2022 THEN f.electric_vehicles_sold ELSE 0 END) AS sales_fy22,
        SUM(CASE WHEN d.fiscal_year = 2024 THEN f.electric_vehicles_sold ELSE 0 END) AS sales_fy24
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_state s ON f.state_id = s.state_id
    GROUP BY s.state_name
)
SELECT 
    state_name,
    sales_fy22,
    sales_fy24,
    (sales_fy24 - sales_fy22) AS absolute_volume_increase,
    ROUND(((CAST(sales_fy24 AS REAL) - sales_fy22) / NULLIF(sales_fy22, 0)) * 100.0, 2) AS total_growth_pct,
    ROUND((POWER(CAST(sales_fy24 AS REAL) / NULLIF(sales_fy22, 0), 0.5) - 1.0) * 100.0, 2) AS cagr_2yr_pct
FROM state_fy
WHERE sales_fy22 >= 500  -- Filter for meaningful base volume
ORDER BY cagr_2yr_pct DESC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 12: Top 10 EV Manufacturers Overall (Both Categories Combined)
-- ------------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(f.electric_vehicles_sold) DESC) AS rank,
    m.maker_name,
    m.primary_category,
    SUM(f.electric_vehicles_sold) AS total_units_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_maker_sales)) * 100.0, 2) AS overall_market_share_pct
FROM fact_maker_sales f
JOIN dim_maker m ON f.maker_id = m.maker_id
GROUP BY m.maker_name, m.primary_category
ORDER BY rank
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 13: 2-Wheeler Manufacturer Market Share Breakdown
-- ------------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(f.electric_vehicles_sold) DESC) AS rank_2w,
    m.maker_name,
    SUM(f.electric_vehicles_sold) AS units_sold_2w,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_maker_sales WHERE category_id = 1)) * 100.0, 2) AS market_share_2w_pct
FROM fact_maker_sales f
JOIN dim_maker m ON f.maker_id = m.maker_id
WHERE f.category_id = 1
GROUP BY m.maker_name
ORDER BY rank_2w;

-- ------------------------------------------------------------------------------
-- QUERY 14: 4-Wheeler Manufacturer Market Share Breakdown
-- ------------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(f.electric_vehicles_sold) DESC) AS rank_4w,
    m.maker_name,
    SUM(f.electric_vehicles_sold) AS units_sold_4w,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_maker_sales WHERE category_id = 2)) * 100.0, 2) AS market_share_4w_pct
FROM fact_maker_sales f
JOIN dim_maker m ON f.maker_id = m.maker_id
WHERE f.category_id = 2
GROUP BY m.maker_name
ORDER BY rank_4w;

-- ------------------------------------------------------------------------------
-- QUERY 15: Manufacturer Annual Rank Mobility (DENSE_RANK by Fiscal Year)
-- ------------------------------------------------------------------------------
WITH maker_annual AS (
    SELECT 
        d.fiscal_year_label,
        d.fiscal_year,
        m.maker_name,
        SUM(f.electric_vehicles_sold) AS annual_sales,
        DENSE_RANK() OVER (
            PARTITION BY d.fiscal_year 
            ORDER BY SUM(f.electric_vehicles_sold) DESC
        ) AS yearly_rank
    FROM fact_maker_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_maker m ON f.maker_id = m.maker_id
    GROUP BY d.fiscal_year_label, d.fiscal_year, m.maker_name
)
SELECT 
    maker_name,
    MAX(CASE WHEN fiscal_year = 2022 THEN yearly_rank END) AS rank_fy22,
    MAX(CASE WHEN fiscal_year = 2023 THEN yearly_rank END) AS rank_fy23,
    MAX(CASE WHEN fiscal_year = 2024 THEN yearly_rank END) AS rank_fy24,
    MAX(CASE WHEN fiscal_year = 2024 THEN annual_sales END) AS sales_fy24
FROM maker_annual
GROUP BY maker_name
ORDER BY rank_fy24 ASC
LIMIT 12;

-- ------------------------------------------------------------------------------
-- QUERY 16: Emerging vs Declining 2W OEMs (Share Shift FY22 to FY24)
-- ------------------------------------------------------------------------------
WITH oem_shares AS (
    SELECT 
        m.maker_name,
        SUM(CASE WHEN d.fiscal_year = 2022 THEN f.electric_vehicles_sold ELSE 0 END) AS sales_fy22,
        SUM(CASE WHEN d.fiscal_year = 2024 THEN f.electric_vehicles_sold ELSE 0 END) AS sales_fy24
    FROM fact_maker_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_maker m ON f.maker_id = m.maker_id
    WHERE f.category_id = 1
    GROUP BY m.maker_name
),
totals AS (
    SELECT 
        SUM(CASE WHEN d.fiscal_year = 2022 THEN f.electric_vehicles_sold ELSE 0 END) AS total_2w_fy22,
        SUM(CASE WHEN d.fiscal_year = 2024 THEN f.electric_vehicles_sold ELSE 0 END) AS total_2w_fy24
    FROM fact_maker_sales f
    JOIN dim_date d ON f.date = d.date
    WHERE f.category_id = 1
)
SELECT 
    s.maker_name,
    s.sales_fy22,
    s.sales_fy24,
    ROUND((CAST(s.sales_fy22 AS REAL) / t.total_2w_fy22) * 100.0, 2) AS share_fy22_pct,
    ROUND((CAST(s.sales_fy24 AS REAL) / t.total_2w_fy24) * 100.0, 2) AS share_fy24_pct,
    ROUND(((CAST(s.sales_fy24 AS REAL) / t.total_2w_fy24) - (CAST(s.sales_fy22 AS REAL) / t.total_2w_fy22)) * 100.0, 2) AS share_change_bps_pct
FROM oem_shares s
CROSS JOIN totals t
ORDER BY share_change_bps_pct DESC;

-- ------------------------------------------------------------------------------
-- QUERY 17: Top 3 Manufacturers in Each Category per Fiscal Year
-- ------------------------------------------------------------------------------
WITH ranked_oems AS (
    SELECT 
        d.fiscal_year_label,
        c.category_name,
        m.maker_name,
        SUM(f.electric_vehicles_sold) AS sales,
        ROW_NUMBER() OVER (
            PARTITION BY d.fiscal_year, c.category_name 
            ORDER BY SUM(f.electric_vehicles_sold) DESC
        ) AS cat_rank
    FROM fact_maker_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_category c ON f.category_id = c.category_id
    JOIN dim_maker m ON f.maker_id = m.maker_id
    GROUP BY d.fiscal_year_label, d.fiscal_year, c.category_name, m.maker_name
)
SELECT 
    fiscal_year_label,
    category_name,
    cat_rank,
    maker_name,
    sales
FROM ranked_oems
WHERE cat_rank <= 3
ORDER BY fiscal_year_label, category_name, cat_rank;

-- ------------------------------------------------------------------------------
-- QUERY 18: Category Growth Comparison (2-Wheelers vs 4-Wheelers Across Years)
-- ------------------------------------------------------------------------------
WITH cat_fy AS (
    SELECT 
        d.fiscal_year_label,
        d.fiscal_year,
        c.category_name,
        SUM(f.electric_vehicles_sold) AS ev_sold
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_category c ON f.category_id = c.category_id
    GROUP BY d.fiscal_year_label, d.fiscal_year, c.category_name
)
SELECT 
    fiscal_year_label,
    category_name,
    ev_sold,
    LAG(ev_sold) OVER (PARTITION BY category_name ORDER BY fiscal_year) AS prev_year_ev,
    ROUND(((CAST(ev_sold AS REAL) - LAG(ev_sold) OVER (PARTITION BY category_name ORDER BY fiscal_year))
           / LAG(ev_sold) OVER (PARTITION BY category_name ORDER BY fiscal_year)) * 100.0, 2) AS yoy_growth_pct
FROM cat_fy
ORDER BY category_name, fiscal_year;

-- ------------------------------------------------------------------------------
-- QUERY 19: Monthly EV Category Split Over Time
-- ------------------------------------------------------------------------------
WITH cat_monthly AS (
    SELECT 
        d.date,
        d.year_month,
        SUM(CASE WHEN f.category_id = 1 THEN f.electric_vehicles_sold ELSE 0 END) AS ev_2w,
        SUM(CASE WHEN f.category_id = 2 THEN f.electric_vehicles_sold ELSE 0 END) AS ev_4w,
        SUM(f.electric_vehicles_sold) AS total_ev
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.date, d.year_month
)
SELECT 
    year_month,
    ev_2w,
    ev_4w,
    total_ev,
    ROUND((CAST(ev_2w AS REAL) / total_ev) * 100.0, 2) AS share_2w_pct,
    ROUND((CAST(ev_4w AS REAL) / total_ev) * 100.0, 2) AS share_4w_pct
FROM cat_monthly
ORDER BY date;

-- ------------------------------------------------------------------------------
-- QUERY 20: Top State for Each Vehicle Category
-- ------------------------------------------------------------------------------
WITH state_cat AS (
    SELECT 
        c.category_name,
        s.state_name,
        SUM(f.electric_vehicles_sold) AS cat_sales,
        ROW_NUMBER() OVER (
            PARTITION BY c.category_name 
            ORDER BY SUM(f.electric_vehicles_sold) DESC
        ) AS rnk
    FROM fact_state_sales f
    JOIN dim_category c ON f.category_id = c.category_id
    JOIN dim_state s ON f.state_id = s.state_id
    GROUP BY c.category_name, s.state_name
)
SELECT 
    category_name,
    state_name AS top_state,
    cat_sales,
    ROUND((CAST(cat_sales AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales f2 
           JOIN dim_category c2 ON f2.category_id = c2.category_id 
           WHERE c2.category_name = state_cat.category_name)) * 100.0, 2) AS category_share_pct
FROM state_cat
WHERE rnk = 1;

-- ------------------------------------------------------------------------------
-- QUERY 21: High-Volume vs High-Penetration State Quadrant Classification
-- ------------------------------------------------------------------------------
WITH state_stats AS (
    SELECT 
        s.state_name,
        SUM(f.electric_vehicles_sold) AS ev_sold,
        SUM(f.total_vehicles_sold) AS total_sold,
        ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / SUM(f.total_vehicles_sold)) * 100.0, 2) AS penetration_pct
    FROM fact_state_sales f
    JOIN dim_state s ON f.state_id = s.state_id
    GROUP BY s.state_name
),
medians AS (
    SELECT 
        AVG(ev_sold) AS avg_ev,
        AVG(penetration_pct) AS avg_pen
    FROM state_stats
)
SELECT 
    st.state_name,
    st.ev_sold,
    st.penetration_pct,
    CASE 
        WHEN st.ev_sold >= m.avg_ev AND st.penetration_pct >= m.avg_pen THEN 'Leaders (High Volume, High Penetration)'
        WHEN st.ev_sold >= m.avg_ev AND st.penetration_pct < m.avg_pen THEN 'Scale Drivers (High Volume, Low Penetration)'
        WHEN st.ev_sold < m.avg_ev AND st.penetration_pct >= m.avg_pen THEN 'Niche Adopters (Low Volume, High Penetration)'
        ELSE 'Laggards (Low Volume, Low Penetration)'
    END AS strategic_quadrant
FROM state_stats st
CROSS JOIN medians m
ORDER BY st.ev_sold DESC;

-- ------------------------------------------------------------------------------
-- QUERY 22: Infrastructure Stress Ratio (EV Registrations per Charging Station)
-- ------------------------------------------------------------------------------
SELECT 
    s.state_name,
    s.region,
    s.operational_pcs,
    SUM(f.electric_vehicles_sold) AS total_ev_sold,
    CASE 
        WHEN s.operational_pcs = 0 THEN NULL 
        ELSE ROUND(CAST(SUM(f.electric_vehicles_sold) AS REAL) / s.operational_pcs, 1)
    END AS evs_per_charging_station
FROM fact_state_sales f
JOIN dim_state s ON f.state_id = s.state_id
GROUP BY s.state_name, s.region, s.operational_pcs
HAVING s.operational_pcs > 0
ORDER BY evs_per_charging_station DESC;

-- ------------------------------------------------------------------------------
-- QUERY 23: Top 10 Charging Infrastructure Equipped States
-- ------------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY s.operational_pcs DESC) AS rank,
    s.state_name,
    s.region,
    s.operational_pcs,
    ROUND((CAST(s.operational_pcs AS REAL) / (SELECT SUM(operational_pcs) FROM dim_state)) * 100.0, 2) AS pcs_share_pct,
    SUM(f.electric_vehicles_sold) AS ev_sold
FROM dim_state s
LEFT JOIN fact_state_sales f ON s.state_id = f.state_id
GROUP BY s.state_name, s.region, s.operational_pcs
ORDER BY rank
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 24: Seasonality Index (Monthly Sales Distribution Across Calendar Years)
-- ------------------------------------------------------------------------------
SELECT 
    d.month_name,
    d.month_num,
    SUM(f.electric_vehicles_sold) AS cumulative_monthly_ev_sold,
    ROUND((CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
          (SELECT SUM(electric_vehicles_sold) FROM fact_state_sales)) * 100.0, 2) AS seasonal_share_pct
FROM fact_state_sales f
JOIN dim_date d ON f.date = d.date
GROUP BY d.month_name, d.month_num
ORDER BY d.month_num;

-- ------------------------------------------------------------------------------
-- QUERY 25: Market Concentration: Herfindahl-Hirschman Index (HHI) for OEMs
-- ------------------------------------------------------------------------------
WITH maker_market_shares AS (
    SELECT 
        c.category_name,
        m.maker_name,
        (CAST(SUM(f.electric_vehicles_sold) AS REAL) / 
         SUM(SUM(f.electric_vehicles_sold)) OVER (PARTITION BY c.category_name)) * 100.0 AS market_share_pct
    FROM fact_maker_sales f
    JOIN dim_category c ON f.category_id = c.category_id
    JOIN dim_maker m ON f.maker_id = m.maker_id
    GROUP BY c.category_name, m.maker_name
)
SELECT 
    category_name,
    ROUND(SUM(market_share_pct * market_share_pct), 1) AS hhi_index,
    CASE 
        WHEN SUM(market_share_pct * market_share_pct) > 2500 THEN 'Highly Concentrated Market'
        WHEN SUM(market_share_pct * market_share_pct) BETWEEN 1500 AND 2500 THEN 'Moderately Concentrated Market'
        ELSE 'Competitive / Unconcentrated Market'
    END AS market_structure
FROM maker_market_shares
GROUP BY category_name;

-- ------------------------------------------------------------------------------
-- QUERY 26: Quarterly Market Leader OEM in 2-Wheelers and 4-Wheelers
-- ------------------------------------------------------------------------------
WITH quarterly_ranks AS (
    SELECT 
        d.fiscal_quarter_label,
        d.date,
        c.category_name,
        m.maker_name,
        SUM(f.electric_vehicles_sold) AS sales,
        ROW_NUMBER() OVER (
            PARTITION BY d.fiscal_quarter_label, c.category_name 
            ORDER BY SUM(f.electric_vehicles_sold) DESC
        ) AS q_rnk
    FROM fact_maker_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_category c ON f.category_id = c.category_id
    JOIN dim_maker m ON f.maker_id = m.maker_id
    GROUP BY d.fiscal_quarter_label, d.date, c.category_name, m.maker_name
)
SELECT 
    fiscal_quarter_label,
    category_name,
    maker_name AS leader,
    sales
FROM quarterly_ranks
WHERE q_rnk = 1
ORDER BY date, category_name;

-- ------------------------------------------------------------------------------
-- QUERY 27: Growth Acceleration vs Deceleration Across Top 15 States
-- ------------------------------------------------------------------------------
WITH state_annual AS (
    SELECT 
        s.state_name,
        SUM(CASE WHEN d.fiscal_year = 2022 THEN f.electric_vehicles_sold ELSE 0 END) AS ev_fy22,
        SUM(CASE WHEN d.fiscal_year = 2023 THEN f.electric_vehicles_sold ELSE 0 END) AS ev_fy23,
        SUM(CASE WHEN d.fiscal_year = 2024 THEN f.electric_vehicles_sold ELSE 0 END) AS ev_fy24
    FROM fact_state_sales f
    JOIN dim_date d ON f.date = d.date
    JOIN dim_state s ON f.state_id = s.state_id
    GROUP BY s.state_name
),
growth_rates AS (
    SELECT 
        state_name,
        ev_fy22,
        ev_fy23,
        ev_fy24,
        ROUND(((CAST(ev_fy23 AS REAL) - ev_fy22) / NULLIF(ev_fy22, 0)) * 100.0, 1) AS yoy_fy23_pct,
        ROUND(((CAST(ev_fy24 AS REAL) - ev_fy23) / NULLIF(ev_fy23, 0)) * 100.0, 1) AS yoy_fy24_pct
    FROM state_annual
    WHERE ev_fy22 >= 1000
)
SELECT 
    state_name,
    ev_fy22,
    ev_fy23,
    ev_fy24,
    yoy_fy23_pct,
    yoy_fy24_pct,
    CASE 
        WHEN yoy_fy24_pct > yoy_fy23_pct THEN 'Accelerating Growth'
        WHEN yoy_fy24_pct > 0 THEN 'Decelerating Growth (Still Expanding)'
        ELSE 'Contraction'
    END AS momentum_status
FROM growth_rates
ORDER BY ev_fy24 DESC
LIMIT 15;
