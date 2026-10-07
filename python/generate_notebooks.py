"""
Notebook Generator for EVPulse India.
Constructs and validates the 3 project Jupyter notebooks.
"""
import nbformat as nbf
from pathlib import Path

NOTEBOOKS_DIR = Path("d:/EV_Analytics/EVPulse-India/notebooks")
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Notebook 01: Data Understanding
# -------------------------------------------------------------
nb1 = nbf.v4.new_notebook()
nb1.metadata = {
    "language_info": {"name": "python", "version": "3.11"},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
}

nb1.cells = [
    nbf.v4.new_markdown_cell("""# 01. Data Understanding & Source Profiling
## EVPulse India: Electric Vehicle Market Analytics

### Project Provenance & Context
- **Primary Source:** Ministry of Road Transport and Highways (MoRTH), Government of India via the **Vahan Sewa Open Portal**.
- **Secondary Source:** Bureau of Energy Efficiency (BEE), Ministry of Power (Public Charging Stations registry).
- **Temporal Horizon:** April 2021 to March 2024 (36 consecutive months, FY 2022 to FY 2024).
- **Target Entities:** 34 Indian States & UTs, 26 Automotive OEMs, 2 Key Segments (2-Wheelers & 4-Wheelers).
"""),
    nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np

RAW_DIR = "../data/raw"
os.listdir(RAW_DIR)"""),
    nbf.v4.new_markdown_cell("### 1. Inspecting State-Level Sales Dataset"),
    nbf.v4.new_code_cell("""df_state = pd.read_csv(f"{RAW_DIR}/electric_vehicle_sales_by_state.csv")
print("Shape:", df_state.shape)
display(df_state.head())
print("\\nData Types & Null Counts:")
df_state.info()"""),
    nbf.v4.new_markdown_cell("### 2. Inspecting Manufacturer (OEM) Sales Dataset"),
    nbf.v4.new_code_cell("""df_maker = pd.read_csv(f"{RAW_DIR}/electric_vehicle_sales_by_makers.csv")
print("Shape:", df_maker.shape)
display(df_maker.head())
print("\\nData Types & Null Counts:")
df_maker.info()"""),
    nbf.v4.new_markdown_cell("### 3. Inspecting Date Dimension & Charging Stations"),
    nbf.v4.new_code_cell("""df_date = pd.read_csv(f"{RAW_DIR}/dim_date.csv")
df_pcs = pd.read_csv(f"{RAW_DIR}/charging_stations_by_state.csv")
display(df_date.head())
display(df_pcs.head())"""),
    nbf.v4.new_markdown_cell("### 4. Integrity Audit: State vs Maker EV Sales Reconciliation"),
    nbf.v4.new_code_cell("""ev_state_sum = df_state['electric_vehicles_sold'].sum()
ev_maker_sum = df_maker['electric_vehicles_sold'].sum()

print(f"Total EV Sold (State Table): {ev_state_sum:,}")
print(f"Total EV Sold (Maker Table): {ev_maker_sum:,}")
print(f"Discrepancy: {ev_state_sum - ev_maker_sum} units")
assert ev_state_sum == ev_maker_sum == 2066111, "Reconciliation failed!"""),
    nbf.v4.new_markdown_cell("""### 5. Identification of Real-World Data Nuances & Outliers
1. **Missing Grid Records:**
   - Andaman & Nicobar Islands: 2021-06 (4W) missing due to COVID shutdown.
   - Odisha: 2024-03 missing due to central reporting lag.
2. **Data Reporting Anomaly in Kerala (2024-01-01, 4-Wheelers):**
   - Electric vehicles sold: 734
   - Total vehicles reported: 164
   - In internal combustion vs EV reporting, total vehicle sales cannot be lower than electric sales. This requires transparent cleaning and documentation.
""")
]

with open(NOTEBOOKS_DIR / "01_data_understanding.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb1, f)

# -------------------------------------------------------------
# 2. Notebook 02: Data Cleaning
# -------------------------------------------------------------
nb2 = nbf.v4.new_notebook()
nb2.metadata = {
    "language_info": {"name": "python", "version": "3.11"},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
}

nb2.cells = [
    nbf.v4.new_markdown_cell("""# 02. Data Cleaning & Dimensional Modeling Pipeline
## EVPulse India: Transforming Raw Data into a Star Schema

This notebook executes the data cleaning transformations:
1. Standardization of Date hierarchies (Calendar + Indian Fiscal Year/Quarter).
2. Enrichment of State dimension with macro-geographic zones and Public Charging Station counts.
3. Clean OEM naming (e.g. formatting `Mercedes-Benz AG`) and category tagging.
4. Handling the Kerala 2024-01-01 total vehicles anomaly transparently.
5. Exporting validated Star Schema entities to `data/processed/`.
"""),
    nbf.v4.new_code_cell("""import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent / "python"))

import data_cleaning
# Run the complete, tested data cleaning pipeline
data_cleaning.run_pipeline()"""),
    nbf.v4.new_markdown_cell("### Verifying Processed Output Files"),
    nbf.v4.new_code_cell("""import pandas as pd

p_dir = Path("../data/processed")
for f in sorted(p_dir.glob("*.csv")):
    df = pd.read_csv(f)
    print(f"{f.name:25} | Rows: {len(df):6,} | Cols: {len(df.columns):2} | Memory: {df.memory_usage().sum()/1024:.1f} KB")"""),
    nbf.v4.new_markdown_cell("### Sample of Cleaned Star Schema Entities"),
    nbf.v4.new_code_cell("""df_fact_state = pd.read_csv("../data/processed/fact_state_sales.csv")
display(df_fact_state.head())""")
]

with open(NOTEBOOKS_DIR / "02_data_cleaning.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb2, f)

# -------------------------------------------------------------
# 3. Notebook 03: EDA
# -------------------------------------------------------------
nb3 = nbf.v4.new_notebook()
nb3.metadata = {
    "language_info": {"name": "python", "version": "3.11"},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
}

nb3.cells = [
    nbf.v4.new_markdown_cell("""# 03. Exploratory Data Analysis (EDA)
## EVPulse India: Electric Vehicle Market Intelligence

This notebook analyzes the Indian EV market dynamics across four analytical pillars:
1. **Market Scale & Growth Trajectory:** 3-year volume evolution, YoY growth, and CAGR.
2. **Geographical Adoption:** High-volume states vs. high-penetration leaders.
3. **OEM Competitive Landscape:** Concentration, dominance, and category divergence.
4. **Infrastructure Coupling:** Relationship between EV adoption and Public Charging Stations.
"""),
    nbf.v4.new_code_cell("""import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path.cwd().parent / "python"))
import analysis

# Load cleaned entities
dim_date, dim_state, dim_maker, dim_category, fact_state, fact_maker = analysis.load_cleaned_data()
kpis, fy_summary = analysis.generate_market_kpis(dim_date, dim_state, dim_maker, fact_state, fact_maker)
pd.DataFrame(list(kpis.items()), columns=['KPI Metric', 'Value'])"""),
    nbf.v4.new_markdown_cell("### 1. Macro Market Trajectory (FY22 - FY24)"),
    nbf.v4.new_code_cell("""display(fy_summary)
analysis.plot_yearly_growth_and_cagr(fy_summary)
plt.show()"""),
    nbf.v4.new_markdown_cell("### 2. Monthly EV Registration Dynamics by Vehicle Category"),
    nbf.v4.new_code_cell("""analysis.plot_monthly_ev_trend(dim_date, fact_state)
plt.show()"""),
    nbf.v4.new_markdown_cell("### 3. State-Level Analysis: Top Volume vs High Penetration"),
    nbf.v4.new_code_cell("""analysis.plot_top_and_bottom_states(fact_state)
plt.show()
analysis.plot_state_penetration_rates(fact_state)
plt.show()"""),
    nbf.v4.new_markdown_cell("### 4. OEM Competitive Landscape (2W vs 4W)"),
    nbf.v4.new_code_cell("""analysis.plot_oem_market_share(fact_maker)
plt.show()"""),
    nbf.v4.new_markdown_cell("### 5. Charging Infrastructure & EV Adoption"),
    nbf.v4.new_code_cell("""analysis.plot_charging_infrastructure_correlation(dim_state, fact_state)
plt.show()""")
]

with open(NOTEBOOKS_DIR / "03_eda.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb3, f)

print("Successfully generated all 3 Jupyter notebooks!")
