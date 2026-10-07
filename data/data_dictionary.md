# EVPulse India: Data Dictionary & Data Understanding Specification

## 1. Executive Summary & Provenance
This data dictionary documents the core entities, attributes, business logic, and empirical distributions utilized in the **EVPulse India** Electric Vehicle Analytics Platform.
- **Primary Source:** Ministry of Road Transport and Highways (MoRTH), Government of India – [Vahan Sewa Open Analytics Portal](https://analytics.parivahan.gov.in/).
- **Secondary Source:** Bureau of Energy Efficiency (BEE), Ministry of Power, Government of India (Public Charging Infrastructure Registry).
- **Time Horizon:** April 1, 2021 to March 31, 2024 (36 consecutive months, encompassing Indian Fiscal Years FY 2022, FY 2023, and FY 2024).
- **Geographic Coverage:** 34 Indian States & Union Territories.
- **Total EV Registrations Benchmarked:** 2,066,111 units.
- **Total Automotive Volume Benchmarked:** 57,220,252 units.

---

## 2. Entity Schemas & Attribute Dictionary

### Table 1: `electric_vehicle_sales_by_state.csv`
*Grain: One row per State per Vehicle Category per Month.*
*Total Records: 2,445 rows (out of 2,448 theoretical combinations).*

| Column Name | Data Type (Raw) | Recommended Type | Nullable | Example Value | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date` | `object` (`YYYY-MM-DD`) | `DATE` | No | `2021-04-01` | First day of the reporting month (monthly aggregate grain). Spans `2021-04-01` to `2024-03-01`. |
| `state` | `object` (string) | `VARCHAR(100)` | No | `Maharashtra` | Indian State or Union Territory name (34 distinct administrative territories). |
| `vehicle_category` | `object` (string) | `VARCHAR(50)` | No | `2-Wheelers` | Vehicle classification category: `'2-Wheelers'` or `'4-Wheelers'`. |
| `electric_vehicles_sold` | `int64` | `INTEGER` | No | `2475` | Number of newly registered battery electric vehicles (EVs) in that state, month, and category. |
| `total_vehicles_sold` | `int64` | `INTEGER` | No | `124850` | Total motor vehicles (Internal Combustion Engine + EV) newly registered in that state, month, and category. Must be $\ge \text{electric\_vehicles\_sold}$. |

#### Calculated Metric Definition:
$$\text{EV Penetration Rate (\%)} = \left(\frac{\text{electric\_vehicles\_sold}}{\text{total\_vehicles\_sold}}\right) \times 100$$

---

### Table 2: `electric_vehicle_sales_by_makers.csv`
*Grain: One row per Manufacturer (OEM) per Vehicle Category per Month.*
*Total Records: 816 rows.*

| Column Name | Data Type (Raw) | Recommended Type | Nullable | Example Value | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date` | `object` (`YYYY-MM-DD`) | `DATE` | No | `2022-04-01` | First day of reporting month. Synchronous with state sales table. |
| `vehicle_category` | `object` (string) | `VARCHAR(50)` | No | `2-Wheelers` | Vehicle category (`'2-Wheelers'` or `'4-Wheelers'`). |
| `maker` | `object` (string) | `VARCHAR(100)` | No | `OLA ELECTRIC` | Automotive Original Equipment Manufacturer (OEM) brand name. 26 unique makers (16 in 2W, 10 in 4W). |
| `electric_vehicles_sold` | `int64` | `INTEGER` | No | `12689` | Total EV units registered nationwide by this manufacturer in this category during the month. |

#### Calculated Metric Definition:
$$\text{Maker Market Share (\%)} = \left(\frac{\text{electric\_vehicles\_sold}_{\text{maker, cat, period}}}{\sum_{\text{all makers}} \text{electric\_vehicles\_sold}_{\text{cat, period}}}\right) \times 100$$

---

### Table 3: `dim_date.csv`
*Grain: One row per Month.*
*Total Records: 36 rows.*

| Column Name | Data Type (Raw) | Recommended Type | Nullable | Example Value | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date` | `object` (`YYYY-MM-DD`) | `DATE` | No | `2021-04-01` | Primary key representing the start of each month. |
| `fiscal_year` | `int64` | `INTEGER` | No | `2022` | Indian Fiscal Year running April 1 to March 31. Values: 2022, 2023, 2024. |
| `quarter` | `object` (string) | `VARCHAR(5)` | No | `Q1` | Fiscal Quarter: Q1 (Apr–Jun), Q2 (Jul–Sep), Q3 (Oct–Dec), Q4 (Jan–Mar). |

---

### Table 4: `charging_stations_by_state.csv`
*Grain: One row per State.*
*Total Records: 32 rows.*

| Column Name | Data Type (Raw) | Recommended Type | Nullable | Example Value | Business Definition & Validation Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `State` | `object` (string) | `VARCHAR(100)` | No | `Maharashtra` | State / UT name. Standardized to match sales tables. |
| `No. of Operational PCS` | `int64` | `INTEGER` | No | `3079` | Cumulative operational Public Charging Stations (PCS) registered under BEE / FAME schemes. |

#### Calculated Metric Definition:
$$\text{EVs per Charging Station} = \frac{\text{Total Cumulative 4W + 2W EVs Sold in State}}{\text{Operational PCS in State}}$$

---

## 3. Data Integrity & Reconciliation Audit

1. **Nationwide Reconciliation:**
   - Sum of `electric_vehicles_sold` in `electric_vehicle_sales_by_state`: **2,066,111**
   - Sum of `electric_vehicles_sold` in `electric_vehicle_sales_by_makers`: **2,066,111**
   - Discrepancy: **0 units (100% exact parity)**.
2. **Category Split Parity:**
   - 2-Wheelers: **1,913,168** (92.60% of total Indian EV market volume)
   - 4-Wheelers: **152,943** (7.40% of total Indian EV market volume)
   - Parity verified across state and maker datasets.
3. **Missing Grid Combinations Identified:**
   - Andaman & Nicobar Islands: Missing `2021-06-01`, `4-Wheelers` (Zero registrations during COVID lockdown).
   - Odisha: Missing `2024-03-01` for both `2-Wheelers` and `4-Wheelers` (Reporting lag in central repository).
4. **Charging Station Coverage:**
   - 32 of 34 states have reported operational PCS.
   - Ladakh and Mizoram currently report 0 operational centralized PCS in this registry.

---

## 4. Business Terminology & KPI Glossary
- **Penetration Rate:** Ratio of electric vehicle registrations to total vehicular registrations in a market segment.
- **CAGR (Compound Annual Growth Rate):** $\left(\frac{\text{Sales}_{\text{FY24}}}{\text{Sales}_{\text{FY22}}}\right)^{\frac{1}{2}} - 1$
- **YoY Growth:** Year-over-Year percentage change: $\frac{\text{Sales}_t - \text{Sales}_{t-1}}{\text{Sales}_{t-1}} \times 100$
- **OEM (Original Equipment Manufacturer):** Automotive brand / manufacturer producing the vehicle.
- **PCS (Public Charging Station):** Commercial and public electric charging infrastructure node.
