"""
Database Loader and SQL Validation Pipeline for EVPulse India.
Initializes SQLite database, loads Star Schema entities, and runs comprehensive quality checks.
"""
import sys
import sqlite3
from pathlib import Path
import pandas as pd

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))
import config


def init_database():
    """Initializes schema and tables using 01_schema.sql."""
    print("--- Initializing Analytical Warehouse Database ---")
    db_path = config.SQLITE_DB_PATH
    if db_path.exists():
        db_path.unlink()  # Clean rebuild

    conn = sqlite3.connect(db_path)
    with open(config.SQL_DIR / "01_schema.sql", "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print(f"Database schema initialized at {db_path.name}")


def load_processed_data():
    """Loads cleaned CSVs into the Star Schema tables."""
    print("--- Ingesting Processed Entities into Tables ---")
    conn = sqlite3.connect(config.SQLITE_DB_PATH)

    tables = {
        'dim_date': config.PROCESSED_DATE_DIM,
        'dim_state': config.PROCESSED_STATE_DIM,
        'dim_maker': config.PROCESSED_MAKER_DIM,
        'dim_category': config.PROCESSED_CATEGORY_DIM,
        'fact_state_sales': config.PROCESSED_STATE_SALES,
        'fact_maker_sales': config.PROCESSED_MAKER_SALES
    }

    for table_name, csv_path in tables.items():
        df = pd.read_csv(csv_path)
        # Fetch columns of target table in DB
        cols = [c[1] for c in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]
        # Select matching columns
        matching_cols = [c for c in cols if c in df.columns]
        df[matching_cols].to_sql(table_name, conn, if_exists='append', index=False)
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f" Loaded {table_name:18}: {count:6,} rows")

    conn.commit()
    conn.close()


def run_data_quality_tests():
    """Executes data quality queries and validates parity."""
    print("\n--- Running Automated Data Quality Tests ---")
    conn = sqlite3.connect(config.SQLITE_DB_PATH)
    cursor = conn.cursor()

    # 1. Total EV parity
    ev_state = cursor.execute("SELECT SUM(electric_vehicles_sold) FROM fact_state_sales").fetchone()[0]
    ev_maker = cursor.execute("SELECT SUM(electric_vehicles_sold) FROM fact_maker_sales").fetchone()[0]
    print(f"State Fact EV Total : {ev_state:,}")
    print(f"Maker Fact EV Total : {ev_maker:,}")
    assert ev_state == ev_maker == 2066111, f"Mismatch in EV Sales! State: {ev_state}, Maker: {ev_maker}"

    # 2. Check null violations
    null_state = cursor.execute("""
        SELECT COUNT(*) FROM fact_state_sales 
        WHERE date IS NULL OR state_id IS NULL OR category_id IS NULL
    """).fetchone()[0]
    assert null_state == 0, f"Found {null_state} null FKs in fact_state_sales!"

    null_maker = cursor.execute("""
        SELECT COUNT(*) FROM fact_maker_sales 
        WHERE date IS NULL OR maker_id IS NULL OR category_id IS NULL
    """).fetchone()[0]
    assert null_maker == 0, f"Found {null_maker} null FKs in fact_maker_sales!"

    # 3. Foreign key referential integrity
    orphans = cursor.execute("""
        SELECT COUNT(*) FROM fact_state_sales f 
        LEFT JOIN dim_state s ON f.state_id = s.state_id 
        WHERE s.state_id IS NULL
    """).fetchone()[0]
    assert orphans == 0, f"Found {orphans} orphaned records in fact_state_sales!"

    print("All Data Quality & Referential Integrity tests passed with 100% success!")
    conn.close()


def validate_python_vs_sql():
    """Cross-validates key business metrics between Python pandas calculations and SQL queries."""
    print("\n--- Validating Python vs. SQL Metric Alignment (Step 10) ---")
    conn = sqlite3.connect(config.SQLITE_DB_PATH)

    # Metric 1: Total Volume by Fiscal Year
    df_py_state = pd.read_csv(config.PROCESSED_STATE_SALES)
    df_py_date = pd.read_csv(config.PROCESSED_DATE_DIM)
    py_fy = df_py_state.merge(df_py_date, on='date').groupby('fiscal_year')['electric_vehicles_sold'].sum().to_dict()

    sql_fy_res = conn.execute("""
        SELECT d.fiscal_year, SUM(f.electric_vehicles_sold) 
        FROM fact_state_sales f 
        JOIN dim_date d ON f.date = d.date 
        GROUP BY d.fiscal_year
    """).fetchall()
    sql_fy = dict(sql_fy_res)

    print("Fiscal Year Parity Check:")
    for fy in [2022, 2023, 2024]:
        p_val = py_fy[fy]
        s_val = sql_fy[fy]
        print(f" FY {fy}: Python={p_val:,} | SQL={s_val:,} | Match={p_val == s_val}")
        assert p_val == s_val, f"Mismatch in FY {fy}!"

    # Metric 2: Top 5 States
    py_top5_states = df_py_state.groupby('state')['electric_vehicles_sold'].sum().sort_values(ascending=False).head(5)
    sql_top5_states = conn.execute("""
        SELECT s.state_name, SUM(f.electric_vehicles_sold) 
        FROM fact_state_sales f 
        JOIN dim_state s ON f.state_id = s.state_id 
        GROUP BY s.state_name 
        ORDER BY SUM(f.electric_vehicles_sold) DESC 
        LIMIT 5
    """).fetchall()

    print("\nTop 5 States Parity Check:")
    for (s_name, s_val), (p_name, p_val) in zip(sql_top5_states, py_top5_states.items()):
        print(f" {s_name:15}: Python={p_val:,} | SQL={s_val:,} | Match={s_val == p_val and s_name == p_name}")
        assert s_val == p_val and s_name == p_name, f"Mismatch in state {s_name}!"

    # Metric 3: Top 5 Makers
    df_py_maker = pd.read_csv(config.PROCESSED_MAKER_SALES)
    py_top5_makers = df_py_maker.groupby('maker')['electric_vehicles_sold'].sum().sort_values(ascending=False).head(5)
    sql_top5_makers = conn.execute("""
        SELECT m.maker_name, SUM(f.electric_vehicles_sold) 
        FROM fact_maker_sales f 
        JOIN dim_maker m ON f.maker_id = m.maker_id 
        GROUP BY m.maker_name 
        ORDER BY SUM(f.electric_vehicles_sold) DESC 
        LIMIT 5
    """).fetchall()

    print("\nTop 5 Makers Parity Check:")
    for (s_name, s_val), (p_name, p_val) in zip(sql_top5_makers, py_top5_makers.items()):
        print(f" {s_name:20}: Python={p_val:,} | SQL={s_val:,} | Match={s_val == p_val and s_name == p_name}")
        assert s_val == p_val and s_name == p_name, f"Mismatch in maker {s_name}!"

    print("\n>>> Python vs SQL Validation: 100% RECONCILED AND VERIFIED! <<<")
    conn.close()


def test_business_queries_execution():
    """Validates that all queries in 04_business_analysis.sql execute without syntax or engine errors."""
    print("\n--- Validating Execution of all 27 Business Queries ---")
    conn = sqlite3.connect(config.SQLITE_DB_PATH)
    with open(config.SQL_DIR / "04_business_analysis.sql", "r", encoding="utf-8") as f:
        content = f.read()

    # Split by semicolon comments
    raw_queries = content.split(";\n")
    executed_count = 0
    for q in raw_queries:
        clean_q = q.strip()
        # Filter comments-only blocks
        lines = [l for l in clean_q.split("\n") if not l.strip().startswith("--")]
        stmt = "\n".join(lines).strip()
        if stmt:
            try:
                conn.execute(stmt)
                executed_count += 1
            except Exception as e:
                print(f"Error executing statement:\n{stmt[:100]}...\nError: {e}")
                raise e

    print(f"All {executed_count} Analytical Business Queries executed successfully without any errors!")
    conn.close()


if __name__ == '__main__':
    init_database()
    load_processed_data()
    run_data_quality_tests()
    validate_python_vs_sql()
    test_business_queries_execution()
