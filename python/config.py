"""
Configuration and constants for EVPulse India analytics platform.
"""
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SQL_DIR = BASE_DIR / "sql"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
POWERBI_DIR = BASE_DIR / "powerbi"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Database Configuration
SQLITE_DB_PATH = BASE_DIR / "data" / "evpulse_india.db"

# Raw File Names
RAW_STATE_SALES = RAW_DATA_DIR / "electric_vehicle_sales_by_state.csv"
RAW_MAKER_SALES = RAW_DATA_DIR / "electric_vehicle_sales_by_makers.csv"
RAW_DATE_DIM = RAW_DATA_DIR / "dim_date.csv"
RAW_CHARGING_STATIONS = RAW_DATA_DIR / "charging_stations_by_state.csv"

# Processed File Names
PROCESSED_STATE_SALES = PROCESSED_DATA_DIR / "fact_state_sales.csv"
PROCESSED_MAKER_SALES = PROCESSED_DATA_DIR / "fact_maker_sales.csv"
PROCESSED_DATE_DIM = PROCESSED_DATA_DIR / "dim_date.csv"
PROCESSED_STATE_DIM = PROCESSED_DATA_DIR / "dim_state.csv"
PROCESSED_MAKER_DIM = PROCESSED_DATA_DIR / "dim_maker.csv"
PROCESSED_CATEGORY_DIM = PROCESSED_DATA_DIR / "dim_category.csv"
PROCESSED_CHARGING_DIM = PROCESSED_DATA_DIR / "dim_charging_stations.csv"
