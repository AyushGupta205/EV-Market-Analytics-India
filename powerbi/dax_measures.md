# EVPulse India: Complete DAX Measures Library

This document provides the complete, production-tested DAX (Data Analysis Expressions) measure definitions implemented across the **EVPulse India** Power BI analytical model.

---

## 1. Core Volume Measures

### Total EV Registrations
```dax
Total EV Registrations = 
SUM(fact_state_sales[electric_vehicles_sold])
```

### Total Automotive Registrations (ICE + EV)
```dax
Total Automotive Registrations = 
SUM(fact_state_sales[total_vehicles_sold])
```

### Total ICE Registrations
```dax
Total ICE Registrations = 
SUM(fact_state_sales[non_electric_vehicles_sold])
```

### Total Public Charging Stations (PCS)
```dax
Total Charging Stations = 
SUM(dim_state[operational_pcs])
```

---

## 2. Market Penetration & Adoption Measures

### EV Penetration Rate (%)
$$\text{EV Penetration Rate} = \frac{\text{Total EV Registrations}}{\text{Total Automotive Registrations}} \times 100$$
```dax
EV Penetration Rate % = 
DIVIDE(
    [Total EV Registrations],
    [Total Automotive Registrations],
    0
) * 100
```

### EVs per Public Charging Station (Infrastructure Ratio)
```dax
EVs per Charging Station = 
DIVIDE(
    [Total EV Registrations],
    [Total Charging Stations],
    BLANK()
)
```

---

## 3. Time Intelligence & Growth Measures

### Previous Fiscal Year EV Registrations (PY)
```dax
PY EV Registrations = 
CALCULATE(
    [Total EV Registrations],
    SAMEPERIODLASTYEAR(dim_date[date])
)
```

### Year-over-Year (YoY) Growth (%)
```dax
YoY Growth % = 
VAR CurrentSales = [Total EV Registrations]
VAR PriorSales = [PY EV Registrations]
RETURN
    IF(
        NOT ISBLANK(PriorSales) && PriorSales > 0,
        DIVIDE(CurrentSales - PriorSales, PriorSales, 0) * 100,
        BLANK()
    )
```

### Month-over-Month (MoM) Growth (%)
```dax
MoM Growth % = 
VAR CurrentMonthSales = [Total EV Registrations]
VAR PriorMonthSales = 
    CALCULATE(
        [Total EV Registrations],
        DATEADD(dim_date[date], -1, MONTH)
    )
RETURN
    IF(
        NOT ISBLANK(PriorMonthSales) && PriorMonthSales > 0,
        DIVIDE(CurrentMonthSales - PriorMonthSales, PriorMonthSales, 0) * 100,
        BLANK()
    )
```

### Cumulative Running Total EV Registrations
```dax
Cumulative EV Registrations = 
CALCULATE(
    [Total EV Registrations],
    FILTER(
        ALLSELECTED(dim_date[date]),
        dim_date[date] <= MAX(dim_date[date])
    )
)
```

### 2-Year Compound Annual Growth Rate (CAGR %) (FY22 to FY24)
```dax
2Y CAGR % = 
VAR FY22Sales = CALCULATE([Total EV Registrations], dim_date[fiscal_year] = 2022)
VAR FY24Sales = CALCULATE([Total EV Registrations], dim_date[fiscal_year] = 2024)
RETURN
    IF(
        FY22Sales > 0 && FY24Sales > 0,
        (POWER(DIVIDE(FY24Sales, FY22Sales), 0.5) - 1) * 100,
        BLANK()
    )
```

---

## 4. Market Share & Contribution Measures

### State Volume Contribution (%)
```dax
State Market Share % = 
DIVIDE(
    [Total EV Registrations],
    CALCULATE([Total EV Registrations], ALLSELECTED(dim_state[state_name])),
    0
) * 100
```

### OEM Maker Market Share (%)
```dax
Maker Market Share % = 
DIVIDE(
    SUM(fact_maker_sales[electric_vehicles_sold]),
    CALCULATE(SUM(fact_maker_sales[electric_vehicles_sold]), ALLSELECTED(dim_maker[maker_name])),
    0
) * 100
```

### Vehicle Category Contribution (%)
```dax
Category Contribution % = 
DIVIDE(
    [Total EV Registrations],
    CALCULATE([Total EV Registrations], ALLSELECTED(dim_category[category_name])),
    0
) * 100
```

---

## 5. Ranking & Contextual Measures

### State Rank by EV Volume
```dax
State Rank = 
RANKX(
    ALLSELECTED(dim_state[state_name]),
    [Total EV Registrations],
    ,
    DESC,
    Dense
)
```

### OEM Maker Rank
```dax
Maker Rank = 
RANKX(
    ALLSELECTED(dim_maker[maker_name]),
    SUM(fact_maker_sales[electric_vehicles_sold]),
    ,
    DESC,
    Dense
)
```

### Average Monthly EV Registrations
```dax
Average Monthly EV Registrations = 
AVERAGEX(
    VALUES(dim_date[year_month]),
    [Total EV Registrations]
)
```
