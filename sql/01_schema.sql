-- ==============================================================================
-- EVPulse India: Analytical Data Warehouse Schema (Star Schema)
-- Database Engine: SQLite / PostgreSQL Compatible ANSI SQL DDL
-- Description: Dimensional model for Indian EV registrations, OEM market shares,
--              regional penetration, and public charging infrastructure.
-- ==============================================================================

-- Drop tables if already existing (for clean re-runs)
DROP TABLE IF EXISTS fact_maker_sales;
DROP TABLE IF EXISTS fact_state_sales;
DROP TABLE IF EXISTS dim_maker;
DROP TABLE IF EXISTS dim_state;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_date;

-- ------------------------------------------------------------------------------
-- 1. DIMENSION TABLES
-- ------------------------------------------------------------------------------

-- Date Dimension
CREATE TABLE dim_date (
    date_id                 INTEGER PRIMARY KEY,
    date                    TEXT NOT NULL UNIQUE,       -- Format: YYYY-MM-DD
    fiscal_year             INTEGER NOT NULL,          -- e.g. 2022, 2023, 2024
    fiscal_year_label       TEXT NOT NULL,              -- e.g. 'FY 2022'
    quarter                 TEXT NOT NULL,              -- e.g. 'Q1', 'Q2', 'Q3', 'Q4'
    fiscal_quarter_label    TEXT NOT NULL,              -- e.g. 'FY22-Q1'
    calendar_year           INTEGER NOT NULL,          -- e.g. 2021, 2022, 2023, 2024
    month_num               INTEGER NOT NULL,          -- 1 to 12
    month_name              TEXT NOT NULL,              -- e.g. 'April'
    month_short             TEXT NOT NULL,              -- e.g. 'Apr'
    year_month              TEXT NOT NULL,              -- e.g. '2021-04'
    calendar_quarter        TEXT NOT NULL               -- e.g. 'Q2'
);

-- State Dimension
CREATE TABLE dim_state (
    state_id                INTEGER PRIMARY KEY,
    state_name              TEXT NOT NULL UNIQUE,       -- Standardized state/UT name
    region                  TEXT NOT NULL,              -- North, South, East, West, Central, Northeast, UT
    operational_pcs         INTEGER NOT NULL DEFAULT 0  -- Operational Public Charging Stations (BEE)
);

-- Vehicle Category Dimension
CREATE TABLE dim_category (
    category_id             INTEGER PRIMARY KEY,
    category_name           TEXT NOT NULL UNIQUE,       -- '2-Wheelers', '4-Wheelers'
    description             TEXT
);

-- Manufacturer (OEM) Dimension
CREATE TABLE dim_maker (
    maker_id                INTEGER PRIMARY KEY,
    maker_name              TEXT NOT NULL UNIQUE,       -- Standardized OEM Name
    primary_category        TEXT NOT NULL               -- Primary category of operation
);

-- ------------------------------------------------------------------------------
-- 2. FACT TABLES
-- ------------------------------------------------------------------------------

-- Fact Table 1: State-Level Monthly Vehicle Registrations & Penetration
CREATE TABLE fact_state_sales (
    fact_state_id           INTEGER PRIMARY KEY,
    date                    TEXT NOT NULL,
    state_id                INTEGER NOT NULL,
    category_id             INTEGER NOT NULL,
    electric_vehicles_sold  INTEGER NOT NULL CHECK(electric_vehicles_sold >= 0),
    total_vehicles_sold     INTEGER NOT NULL CHECK(total_vehicles_sold >= 0),
    raw_total_vehicles_sold INTEGER NOT NULL CHECK(raw_total_vehicles_sold >= 0),
    non_electric_vehicles_sold INTEGER NOT NULL CHECK(non_electric_vehicles_sold >= 0),
    ev_penetration_rate_pct REAL NOT NULL CHECK(ev_penetration_rate_pct >= 0.0),
    FOREIGN KEY (date) REFERENCES dim_date(date) ON DELETE RESTRICT,
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES dim_category(category_id) ON DELETE RESTRICT
);

-- Fact Table 2: Manufacturer-Level Monthly EV Sales
CREATE TABLE fact_maker_sales (
    fact_maker_id           INTEGER PRIMARY KEY,
    date                    TEXT NOT NULL,
    maker_id                INTEGER NOT NULL,
    category_id             INTEGER NOT NULL,
    electric_vehicles_sold  INTEGER NOT NULL CHECK(electric_vehicles_sold >= 0),
    FOREIGN KEY (date) REFERENCES dim_date(date) ON DELETE RESTRICT,
    FOREIGN KEY (maker_id) REFERENCES dim_maker(maker_id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES dim_category(category_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------------------------
-- 3. PERFORMANCE INDEXES
-- ------------------------------------------------------------------------------
CREATE INDEX idx_fact_state_date ON fact_state_sales(date);
CREATE INDEX idx_fact_state_state_id ON fact_state_sales(state_id);
CREATE INDEX idx_fact_state_cat_id ON fact_state_sales(category_id);

CREATE INDEX idx_fact_maker_date ON fact_maker_sales(date);
CREATE INDEX idx_fact_maker_maker_id ON fact_maker_sales(maker_id);
CREATE INDEX idx_fact_maker_cat_id ON fact_maker_sales(category_id);

CREATE INDEX idx_dim_date_fy ON dim_date(fiscal_year);
CREATE INDEX idx_dim_state_region ON dim_state(region);
