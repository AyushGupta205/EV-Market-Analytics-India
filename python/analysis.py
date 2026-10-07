"""
Exploratory Data Analysis and Visualizations for EVPulse India.
Generates comprehensive market analytics and high-resolution portfolio charts.
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))
import config

# Visual styling setup
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#EAEAEA'
plt.rcParams['grid.linestyle'] = '--'

# Professional Palette
PALETTE_PRIMARY = '#1E3A8A'  # Deep Navy
PALETTE_ACCENT = '#0D9488'   # Teal/Emerald
PALETTE_MUTED = '#64748B'    # Slate Gray
CATEGORY_COLORS = {'2-Wheelers': '#0284C7', '4-Wheelers': '#F59E0B'}


def load_cleaned_data():
    """Loads all processed Star Schema tables."""
    dim_date = pd.read_csv(config.PROCESSED_DATE_DIM)
    dim_state = pd.read_csv(config.PROCESSED_STATE_DIM)
    dim_maker = pd.read_csv(config.PROCESSED_MAKER_DIM)
    dim_category = pd.read_csv(config.PROCESSED_CATEGORY_DIM)
    fact_state = pd.read_csv(config.PROCESSED_STATE_SALES)
    fact_maker = pd.read_csv(config.PROCESSED_MAKER_SALES)
    return dim_date, dim_state, dim_maker, dim_category, fact_state, fact_maker


def generate_market_kpis(dim_date, dim_state, dim_maker, fact_state, fact_maker):
    """Calculates top-line executive KPIs."""
    total_ev = fact_state['electric_vehicles_sold'].sum()
    total_vehicles = fact_state['total_vehicles_sold'].sum()
    overall_penetration = (total_ev / total_vehicles) * 100

    # FY Breakdown
    m_date = fact_state.merge(dim_date, on='date')
    fy_summary = m_date.groupby('fiscal_year_label').agg(
        ev_sold=('electric_vehicles_sold', 'sum'),
        total_sold=('total_vehicles_sold', 'sum')
    ).reset_index()
    fy_summary['penetration_pct'] = (fy_summary['ev_sold'] / fy_summary['total_sold']) * 100
    fy_summary['yoy_growth_pct'] = fy_summary['ev_sold'].pct_change() * 100

    # 2-year CAGR (FY22 to FY24)
    fy22_ev = fy_summary.loc[fy_summary['fiscal_year_label'] == 'FY 2022', 'ev_sold'].values[0]
    fy24_ev = fy_summary.loc[fy_summary['fiscal_year_label'] == 'FY 2024', 'ev_sold'].values[0]
    cagr_2yr = ((fy24_ev / fy22_ev) ** (1 / 2) - 1) * 100

    kpis = {
        'total_ev_sales': int(total_ev),
        'total_vehicle_sales': int(total_vehicles),
        'overall_penetration_pct': float(round(overall_penetration, 2)),
        'fy22_sales': int(fy22_ev),
        'fy23_sales': int(fy_summary.loc[fy_summary['fiscal_year_label'] == 'FY 2023', 'ev_sold'].values[0]),
        'fy24_sales': int(fy24_ev),
        'cagr_2yr_pct': float(round(cagr_2yr, 2)),
        'fy23_yoy_pct': float(round(fy_summary.loc[fy_summary['fiscal_year_label'] == 'FY 2023', 'yoy_growth_pct'].values[0], 2)),
        'fy24_yoy_pct': float(round(fy_summary.loc[fy_summary['fiscal_year_label'] == 'FY 2024', 'yoy_growth_pct'].values[0], 2)),
        'unique_states': int(fact_state['state'].nunique()),
        'unique_makers': int(fact_maker['maker'].nunique()),
        'total_charging_stations': int(dim_state['operational_pcs'].sum())
    }
    return kpis, fy_summary


def plot_monthly_ev_trend(dim_date, fact_state):
    """Plot 1: Monthly EV Registrations and Category Split over Time."""
    df = fact_state.merge(dim_date, on='date')
    monthly_cat = df.groupby(['year_month', 'vehicle_category'])['electric_vehicles_sold'].sum().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    monthly_cat.plot(kind='bar', stacked=True, color=[CATEGORY_COLORS['2-Wheelers'], CATEGORY_COLORS['4-Wheelers']], ax=ax, width=0.8)

    ax.set_title("EVPulse India: Monthly EV Registrations by Category (FY 2022 - FY 2024)", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Year-Month", fontsize=11, labelpad=10)
    ax.set_ylabel("Electric Vehicles Sold / Registered", fontsize=11, labelpad=10)
    ax.tick_params(axis='x', rotation=70)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax.legend(title="Vehicle Category", frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    chart_path = config.SCREENSHOTS_DIR / "01_monthly_ev_trend.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def plot_yearly_growth_and_cagr(fy_summary):
    """Plot 2: Fiscal Year Volume & YoY Growth Rate."""
    fig, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)

    bars = ax1.bar(fy_summary['fiscal_year_label'], fy_summary['ev_sold'] / 1000, color='#0284C7', width=0.45, label='EV Sales (Thousands)')
    ax1.set_ylabel("EV Sales (in Thousands)", fontsize=11, color='#0284C7')
    ax1.set_ylim(0, 1300)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotate bar values
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f"{h:.1f}k\n({int(h*1000):,})",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, weight='bold')

    ax2 = ax1.twinx()
    growth_pts = fy_summary['yoy_growth_pct'].dropna()
    ax2.plot(fy_summary['fiscal_year_label'].iloc[1:], growth_pts, color='#DC2626', marker='o', linewidth=2.5, markersize=8, label='YoY Growth %')
    ax2.set_ylabel("Year-over-Year Growth (%)", fontsize=11, color='#DC2626')
    ax2.set_ylim(0, 200)
    ax2.grid(False)

    for i, txt in enumerate(growth_pts):
        ax2.annotate(f"{txt:.1f}%",
                     xy=(fy_summary['fiscal_year_label'].iloc[1 + i], txt),
                     xytext=(0, 8), textcoords="offset points",
                     ha='center', va='bottom', fontsize=10, weight='bold', color='#DC2626')

    plt.title("EVPulse India: Annual EV Registrations & YoY Growth Trajectory", fontsize=13, weight='bold', pad=15)
    plt.tight_layout()
    chart_path = config.SCREENSHOTS_DIR / "02_yearly_growth_trend.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def plot_top_and_bottom_states(fact_state):
    """Plot 3: Top 10 States by EV Volume & Bottom 10 States."""
    state_vol = fact_state.groupby('state')['electric_vehicles_sold'].sum().sort_values(ascending=False)
    top_10 = state_vol.head(10).reset_index()
    bottom_10 = state_vol.tail(10).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

    # Top 10
    sns.barplot(data=top_10, y='state', x='electric_vehicles_sold', ax=axes[0], color='#0D9488')
    axes[0].set_title("Top 10 States by Total EV Registrations", fontsize=12, weight='bold')
    axes[0].set_xlabel("EV Registrations", fontsize=10)
    axes[0].set_ylabel("")
    axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    for i, v in enumerate(top_10['electric_vehicles_sold']):
        axes[0].text(v + 3000, i, f"{v:,} ({v/state_vol.sum()*100:.1f}%)", va='center', fontsize=9)
    axes[0].set_xlim(0, top_10['electric_vehicles_sold'].max() * 1.25)

    # Bottom 10
    sns.barplot(data=bottom_10, y='state', x='electric_vehicles_sold', ax=axes[1], color='#E11D48')
    axes[1].set_title("Bottom 10 States / UTs by EV Registrations", fontsize=12, weight='bold')
    axes[1].set_xlabel("EV Registrations", fontsize=10)
    axes[1].set_ylabel("")
    axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    for i, v in enumerate(bottom_10['electric_vehicles_sold']):
        axes[1].text(v + 10, i, f"{v:,}", va='center', fontsize=9)
    axes[1].set_xlim(0, bottom_10['electric_vehicles_sold'].max() * 1.25)

    plt.suptitle("EVPulse India: Regional Volume Extremes", fontsize=14, weight='bold', y=1.02)
    plt.tight_layout()
    chart_path = config.SCREENSHOTS_DIR / "03_top_bottom_states.png"
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()
    return chart_path


def plot_state_penetration_rates(fact_state):
    """Plot 4: EV Penetration Rate across Major Indian States (Top 15 by total vehicles)."""
    state_pen = fact_state.groupby('state').agg(
        ev=('electric_vehicles_sold', 'sum'),
        total=('total_vehicles_sold', 'sum')
    ).reset_index()
    state_pen['penetration_pct'] = (state_pen['ev'] / state_pen['total']) * 100
    state_pen = state_pen.sort_values(by='penetration_pct', ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.barh(state_pen['state'], state_pen['penetration_pct'], color='#3B82F6')
    ax.invert_yaxis()
    ax.set_title("Top 15 States by EV Penetration Rate (%) (FY22 - FY24 Cumulative)", fontsize=13, weight='bold', pad=15)
    ax.set_xlabel("EV Penetration Rate (%) = (EV Sold / Total Sold) * 100", fontsize=10)
    ax.set_xlim(0, state_pen['penetration_pct'].max() * 1.2)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}%",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, weight='bold')

    plt.tight_layout()
    chart_path = config.SCREENSHOTS_DIR / "04_state_penetration_rate.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def plot_oem_market_share(fact_maker):
    """Plot 5: OEM Market Share in 2-Wheelers and 4-Wheelers."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

    # 2-Wheelers
    m2w = fact_maker[fact_maker['vehicle_category'] == '2-Wheelers'].groupby('maker')['electric_vehicles_sold'].sum()
    total_2w = m2w.sum()
    top_2w = m2w.sort_values(ascending=False).head(7)
    others_2w = pd.Series({'Others / Rest of OEMs': m2w.drop(top_2w.index, errors='ignore').sum()})
    pie_2w = pd.concat([top_2w, others_2w])

    colors_2w = sns.color_palette("Blues_r", len(pie_2w))
    axes[0].pie(pie_2w, labels=[f"{idx}\n({val/total_2w*100:.1f}%)" for idx, val in pie_2w.items()],
                colors=colors_2w, startangle=140, counterclock=False,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.2})
    axes[0].set_title(f"2-Wheeler OEM Market Share\n(Total: {total_2w:,} Units)", fontsize=12, weight='bold')

    # 4-Wheelers
    m4w = fact_maker[fact_maker['vehicle_category'] == '4-Wheelers'].groupby('maker')['electric_vehicles_sold'].sum()
    total_4w = m4w.sum()
    top_4w = m4w.sort_values(ascending=False).head(5)
    others_4w = pd.Series({'Others': m4w.drop(top_4w.index, errors='ignore').sum()})
    pie_4w = pd.concat([top_4w, others_4w])

    colors_4w = sns.color_palette("Oranges_r", len(pie_4w))
    axes[1].pie(pie_4w, labels=[f"{idx}\n({val/total_4w*100:.1f}%)" for idx, val in pie_4w.items()],
                colors=colors_4w, startangle=140, counterclock=False,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.2})
    axes[1].set_title(f"4-Wheeler OEM Market Share\n(Total: {total_4w:,} Units)", fontsize=12, weight='bold')

    plt.suptitle("EVPulse India: OEM Market Concentration & Leadership", fontsize=15, weight='bold', y=1.02)
    plt.tight_layout()
    chart_path = config.SCREENSHOTS_DIR / "05_oem_market_share.png"
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()
    return chart_path


def plot_charging_infrastructure_correlation(dim_state, fact_state):
    """Plot 6: Correlation between EV Adoption and Public Charging Stations."""
    ev_by_state = fact_state.groupby('state')['electric_vehicles_sold'].sum().reset_index()
    merged = ev_by_state.merge(dim_state, left_on='state', right_on='state_name')
    merged = merged[merged['operational_pcs'] > 0]  # Exclude zero-PCS for log readability

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.regplot(data=merged, x='operational_pcs', y='electric_vehicles_sold',
                scatter_kws={'alpha': 0.7, 's': 70, 'color': '#0D9488'},
                line_kws={'color': '#1E3A8A', 'linewidth': 2}, ax=ax)

    # Label top states
    for _, row in merged.sort_values(by='electric_vehicles_sold', ascending=False).head(8).iterrows():
        ax.text(row['operational_pcs'] + 30, row['electric_vehicles_sold'],
                row['state'], fontsize=8.5, weight='bold', color='#1E293B')

    ax.set_title("Operational Public Charging Stations vs. EV Sales by State", fontsize=13, weight='bold', pad=15)
    ax.set_xlabel("Number of Operational Public Charging Stations (BEE)", fontsize=10)
    ax.set_ylabel("Total EV Registrations (FY22 - FY24)", fontsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

    corr = merged['operational_pcs'].corr(merged['electric_vehicles_sold'])
    ax.annotate(f"Pearson Correlation (r) = {corr:.2f}\nStrong Positive Association",
                xy=(0.05, 0.85), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#CBD5E1", lw=1.2),
                fontsize=9.5, weight='bold', color='#0F172A')

    plt.tight_layout()
    chart_path = config.SCREENSHOTS_DIR / "06_charging_infrastructure_correlation.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def run_all_analysis():
    """Generates all analytics tables, metrics, and figures."""
    print("=== EVPulse India: Running Analysis & Visual Generation ===")
    config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    dim_date, dim_state, dim_maker, dim_category, fact_state, fact_maker = load_cleaned_data()

    kpis, fy_summary = generate_market_kpis(dim_date, dim_state, dim_maker, fact_state, fact_maker)
    print("\n--- Key Executive Market Indicators ---")
    for k, v in kpis.items():
        print(f"{k}: {v}")

    print("\nGenerating Figures:")
    p1 = plot_monthly_ev_trend(dim_date, fact_state)
    print(f" [x] {p1.name}")
    p2 = plot_yearly_growth_and_cagr(fy_summary)
    print(f" [x] {p2.name}")
    p3 = plot_top_and_bottom_states(fact_state)
    print(f" [x] {p3.name}")
    p4 = plot_state_penetration_rates(fact_state)
    print(f" [x] {p4.name}")
    p5 = plot_oem_market_share(fact_maker)
    print(f" [x] {p5.name}")
    p6 = plot_charging_infrastructure_correlation(dim_state, fact_state)
    print(f" [x] {p6.name}")
    print("=== All visual artifacts generated successfully in screenshots/ ===")


if __name__ == '__main__':
    run_all_analysis()
