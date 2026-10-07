# EVPulse India: Power BI Data Model Architecture & Report Specification

## 1. Dimensional Model Overview (Star Schema)
The Power BI semantic layer is architected according to Kimball Star Schema principles to ensure optimal VertiPaq compression, lightning-fast DAX evaluation, and predictable filter propagation.

```
                      +------------------+
                      |     dim_date     |
                      +------------------+
                      | PK: date         |
                      |     fiscal_year  |
                      |     quarter      |
                      |     year_month   |
                      +--------+---------+
                               |
               +---------------+---------------+
        1 to * |                               | 1 to *
               v                               v
    +------------------------+      +------------------------+
    |    fact_state_sales    |      |    fact_maker_sales    |
    +------------------------+      +------------------------+
    | FK: date               |      | FK: date               |
    | FK: state_id           |      | FK: maker_id           |
    | FK: category_id        |      | FK: category_id        |
    |  electric_vehicles_sold|      |  electric_vehicles_sold|
    |  total_vehicles_sold   |      +-----------+------------+
    |  penetration_rate_pct  |                  |
    +-----------+------------+                  |
                |                               |
        * to 1  |                       * to 1  |
        +-------+-------+               +-------+-------+
        |               |               |               |
        v               v               v               v
+---------------+ +---------------+ +---------------+ +---------------+
|   dim_state   | |  dim_category | |   dim_maker   | |  dim_category |
+---------------+ +---------------+ +---------------+ +---------------+
| PK: state_id  | | PK: cat_id    | | PK: maker_id  | | PK: cat_id    |
|   state_name  | |   cat_name    | |   maker_name  | |   cat_name    |
|   region      | +---------------+ |   primary_cat | +---------------+
|   pcs_count   |                   +---------------+
+---------------+
```

### Table Relationships & Cardinality
| From Table | From Column | To Table | To Column | Cardinality | Cross Filter Direction | Security / Referential Integrity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_date` | `date` | `fact_state_sales` | `date` | `1 : *` | Single (`dim_date` filters `fact`) | Active |
| `dim_date` | `date` | `fact_maker_sales` | `date` | `1 : *` | Single (`dim_date` filters `fact`) | Active |
| `dim_state` | `state_id` | `fact_state_sales` | `state_id` | `1 : *` | Single (`dim_state` filters `fact`) | Active |
| `dim_maker` | `maker_id` | `fact_maker_sales` | `maker_id` | `1 : *` | Single (`dim_maker` filters `fact`) | Active |
| `dim_category` | `category_id` | `fact_state_sales` | `category_id` | `1 : *` | Single (`dim_category` filters `fact`) | Active |
| `dim_category` | `category_id` | `fact_maker_sales` | `category_id` | `1 : *` | Single (`dim_category` filters `fact`) | Active |

---

## 2. Single-Page Executive Dashboard Architecture (1920 × 1080)

**Report Page Name:** `EVPulse India | Executive Dashboard`  
**Canvas Aspect Ratio:** 16:9 (`1920px` width × `1080px` height)  
**Theme:** `EVPulse Light Theme` (`#F8FAFC` canvas, `#FFFFFF` visual containers, `#E2E8F0` border, `#0F172A` text, `#0D9488` teal primary accent, `#2563EB` blue secondary accent)

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ EVPulse India: Electric Vehicle Market Analytics               Period: FY2022–FY2024   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ FY: All ▼   State: All ▼   Category: All ▼   Manufacturer: All ▼   Reset Filters       │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ Total EVs    │ FY2024 EVs   │ YoY Growth   │ 2W Share     │ 4W Share     │ Charging Stn│
│ 2,066,111    │ 1,019,593    │ +31.5%       │ 92.60%       │ 7.40%        │ 11,664      │
├─────────────────────────────────────────────┬──────────────────────────────┬───────────┤
│                                             │  CATEGORY MIX                │ MARKET    │
│  EV REGISTRATION TREND                      │  2W: 1.91M (92.6%)           │ CONCENTRAT│
│  Monthly line chart (FY22 → FY23 → FY24)    │  4W: 153K (7.4%)             │ 2W: 1,482 │
│                                             │  Horizontal Bar Chart        │ 4W: 4,211 │
├──────────────────────────────┬──────────────┴───────────────┬──────────────┴───────────┤
│ TOP STATES BY REGISTRATIONS  │ STATE EV PENETRATION RATE    │ MANUFACTURER MARKET SHARE│
│ Maharashtra (396K), KA (313K)│ Goa (7.95%), Kerala (5.63%)  │ Ola (489K), Tata (88.9K) │
│ Horizontal Bar Chart (Top 10)│ Horizontal Bar Chart (Top 10)│ Horizontal Bar (Top 10)  │
├──────────────────────────────┴──────────────┬───────────────┴──────────────────────────┤
│ CHARGING INFRASTRUCTURE SCATTER             │ KEY BUSINESS INSIGHTS                    │
│ EV Registrations vs Public Charging Stations│ 1. 2W Dominance: 92.60% volume share     │
│ Bubble chart per state                      │ 2. Geographic Clustering: Top 5 = 55.06% │
│                                             │ 3. 4W Concentration: Tata + M&M = 85.08% │
│                                             │ 4. Infrastructure Disparity: 177 EVs/PCS │
├─────────────────────────────────────────────┴──────────────────────────────────────────┤
│ Data: MoRTH / Vahan Sewa & BEE | Period: FY2022–FY2024 | Analytical Stack: Python·SQL·PowerBI│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Visual Containers & Coordinate Grid

| Container | Visual Type | Coordinates (X, Y, W, H) | Data / Semantic Query Binding |
| :--- | :--- | :--- | :--- |
| **Header Banner** | Textbox / Action | `(24, 15, 1872, 60)` | Dashboard title, subtitle, and metadata |
| **Global Slicers** | Slicer Bar | `(24, 82, 1872, 50)` | `dim_date[fiscal_year]`, `dim_state[state_name]`, `dim_category[category_name]`, `dim_maker[maker_name]` |
| **KPI Cards Strip** | Card / CardVisual | `(24, 140, 1872, 95)` | `[Total EV Registrations]`, `[FY2024 Registrations]`, `[YoY Growth %]`, `[2W Market Share %]`, `[4W Market Share %]`, `[Total Charging Stations]` |
| **EV Trend Chart** | Line Chart | `(24, 245, 924, 260)` | Category: `dim_date[year_month]`, Y: `[Total EV Registrations]` |
| **Category Mix** | Horizontal Bar | `(960, 245, 456, 260)` | Category: `dim_category[category_name]`, Y: `[Total EV Registrations]` |
| **Market Concentration** | KPI Cards | `(1428, 245, 468, 260)` | 2W HHI (`1,482`), 4W HHI (`4,211`), explanatory note |
| **Top States** | Horizontal Bar | `(24, 515, 612, 260)` | Category: `dim_state[state_name]`, Y: `[Total EV Registrations]` (Top 10) |
| **State Penetration**| Horizontal Bar | `(648, 515, 612, 260)` | Category: `dim_state[state_name]`, Y: `[EV Penetration Rate %]` |
| **OEM Market Share** | Horizontal Bar | `(1272, 515, 624, 260)` | Category: `dim_maker[maker_name]`, Y: `[Total EV Registrations]` (Top 10) |
| **Infrastructure** | Scatter Chart | `(24, 785, 750, 235)` | X: `[Total Charging Stations]`, Y: `[Total EV Registrations]`, Category: `dim_state[state_name]` |
| **Insights Panel** | Textbox / Cards | `(786, 785, 1110, 235)`| 4 executive bulletins (Market Structure, Geographic Concentration, 4W Oligopoly, Charging Ratio) |
| **Footer** | Textbox | `(24, 1030, 1872, 35)` | Source attribution, fiscal period, and analytics tools |
