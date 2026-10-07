"""
High-Resolution Dashboard Page Visualizer for EVPulse India.
Generates 5 executive-grade Power BI dashboard pages adhering strictly to Light Theme specifications.
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))
import config

# Color Palette: Executive Light Theme
BG_CANVAS = "#F8FAFC"      # Slate 50
CARD_BG = "#FFFFFF"        # Pure White
BORDER_COLOR = "#E2E8F0"   # Slate 200
TEXT_MAIN = "#0F172A"      # Slate 900
TEXT_MUTED = "#64748B"     # Slate 500
TEAL_PRIMARY = "#0D9488"   # Teal 600 (EV Green/Teal)
TEAL_LIGHT = "#CCFBF1"     # Teal 100
BLUE_SECONDARY = "#2563EB" # Blue 600
BLUE_LIGHT = "#DBEAFE"     # Blue 100
AMBER_ACCENT = "#F59E0B"   # Amber 500
GRAY_TRACK = "#F1F5F9"     # Slate 100

plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'


def draw_header_and_nav(ax, active_tab="Overview"):
    """Renders top header, branding, navigation bar, and filter bar."""
    # Top Banner Background
    ax.add_patch(patches.Rectangle((0, 0.91), 1, 0.09, facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=1))
    
    # Title & Subtitle
    ax.text(0.02, 0.965, "EVPulse India", fontsize=15, weight='bold', color=TEXT_MAIN, zorder=2)
    ax.text(0.095, 0.965, "|  Electric Vehicle Market Analytics (FY 2022 – FY 2024)", fontsize=11, color=TEXT_MUTED, zorder=2)
    ax.text(0.02, 0.925, "Real-world MoRTH (Vahan Sewa) & BEE Public Charging Infrastructure Intelligence", fontsize=8.5, color=TEXT_MUTED, zorder=2)

    # Navigation Tabs
    tabs = ["Overview", "State Performance", "Manufacturer Analysis", "Vehicle Category", "Trends & Infrastructure"]
    start_x = 0.44
    tab_width = 0.105
    for i, tab in enumerate(tabs):
        tx = start_x + (i * tab_width)
        is_active = (tab.lower() in active_tab.lower() or active_tab.lower() in tab.lower())
        
        btn_bg = TEAL_LIGHT if is_active else "#F8FAFC"
        btn_txt = TEAL_PRIMARY if is_active else TEXT_MUTED
        btn_edge = TEAL_PRIMARY if is_active else BORDER_COLOR
        font_wt = 'bold' if is_active else 'normal'

        ax.add_patch(patches.FancyBboxPatch((tx, 0.932), tab_width - 0.012, 0.045,
                                           boxstyle="round,pad=0.006,rounding_size=0.008",
                                           facecolor=btn_bg, edgecolor=btn_edge, linewidth=1.2 if is_active else 0.8, zorder=2))
        ax.text(tx + (tab_width - 0.012) / 2, 0.952, tab, fontsize=8, weight=font_wt, color=btn_txt, ha='center', va='center', zorder=3)

    # Slicer / Filter Bar
    ax.add_patch(patches.Rectangle((0, 0.855), 1, 0.048, facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=0.8, zorder=1))
    ax.text(0.02, 0.878, "Global Filters:", fontsize=8.5, weight='bold', color=TEXT_MUTED, zorder=2)

    slicers = [("Fiscal Year:", "All (FY22–FY24)"), ("Region:", "All India (34 States)"),
               ("Vehicle Category:", "All (2W & 4W)"), ("Manufacturer:", "All OEMs (26)")]
    sx = 0.11
    for label, val in slicers:
        ax.text(sx, 0.878, label, fontsize=8, color=TEXT_MUTED, zorder=2)
        sw = 0.14
        ax.add_patch(patches.FancyBboxPatch((sx + 0.055, 0.862), sw, 0.032,
                                           boxstyle="round,pad=0.003,rounding_size=0.005",
                                           facecolor=GRAY_TRACK, edgecolor=BORDER_COLOR, linewidth=0.8, zorder=2))
        ax.text(sx + 0.062, 0.877, val, fontsize=7.5, color=TEXT_MAIN, weight='semibold', zorder=3)
        ax.text(sx + 0.055 + sw - 0.012, 0.876, "▼", fontsize=6, color=TEXT_MUTED, zorder=3)
        sx += sw + 0.075


def draw_card(ax, x, y, w, h, title, value, subtext="", badge="", badge_color=TEAL_PRIMARY):
    """Draws a subtle rounded KPI card."""
    ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(x + 0.015, y + h - 0.028, title.upper(), fontsize=7.5, weight='bold', color=TEXT_MUTED, zorder=3)
    ax.text(x + 0.015, y + h - 0.068, value, fontsize=17, weight='bold', color=TEXT_MAIN, zorder=3)
    if subtext:
        ax.text(x + 0.015, y + 0.02, subtext, fontsize=7.5, color=TEXT_MUTED, zorder=3)
    if badge:
        bw = len(badge) * 0.0065 + 0.025
        bx = x + w - bw - 0.015
        by = y + h - 0.038
        bg_c = TEAL_LIGHT if badge_color == TEAL_PRIMARY else BLUE_LIGHT
        ax.add_patch(patches.FancyBboxPatch((bx, by), bw, 0.025, boxstyle="round,pad=0.003,rounding_size=0.005",
                                           facecolor=bg_c, edgecolor="none", zorder=3))
        ax.text(bx + bw / 2, by + 0.012, badge, fontsize=7, weight='bold', color=badge_color, ha='center', va='center', zorder=4)


# -------------------------------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -------------------------------------------------------------------------------------------------
def generate_page1():
    fig = plt.figure(figsize=(16, 9), dpi=200, facecolor=BG_CANVAS)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_CANVAS)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    draw_header_and_nav(ax, active_tab="Overview")

    # 6 Premium KPI Cards
    draw_card(ax, 0.02, 0.725, 0.145, 0.115, "Total EV Registrations", "2,066,111", "36 Months Cumulative", "+93.9% CAGR", TEAL_PRIMARY)
    draw_card(ax, 0.18, 0.725, 0.145, 0.115, "YoY Growth (FY24)", "+31.50%", "1,019,593 in FY24", "+244k YoY", TEAL_PRIMARY)
    draw_card(ax, 0.34, 0.725, 0.145, 0.115, "2W Market Share", "92.60%", "1,913,168 Units", "Primary Driver", BLUE_SECONDARY)
    draw_card(ax, 0.50, 0.725, 0.145, 0.115, "4W Market Share", "7.40%", "152,943 Units", "Emerging 4W", AMBER_ACCENT)
    draw_card(ax, 0.66, 0.725, 0.145, 0.115, "Leading State", "Maharashtra", "396,045 EV Sold", "19.2% Share", TEAL_PRIMARY)
    draw_card(ax, 0.82, 0.725, 0.155, 0.115, "Public Charging Stations", "11,664", "BEE Operational PCS", "177 EVs/PCS", BLUE_SECONDARY)

    # Visual 1 (Left Middle): Monthly EV Registration Trend
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.32), 0.62, 0.385, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.035, 0.675, "Monthly EV Registrations Trend (FY 2022 – FY 2024)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.035, 0.655, "Sequential monthly sales trajectory across 2-Wheelers and 4-Wheelers", fontsize=8, color=TEXT_MUTED, zorder=3)

    # Sub-axes for monthly chart
    sub_ax1 = fig.add_axes([0.05, 0.36, 0.57, 0.27])
    df_state = pd.read_csv(config.PROCESSED_STATE_SALES)
    df_date = pd.read_csv(config.PROCESSED_DATE_DIM)
    m = df_state.merge(df_date, on='date').groupby(['year_month', 'vehicle_category'])['electric_vehicles_sold'].sum().unstack().fillna(0)
    
    sub_ax1.fill_between(range(len(m)), m['2-Wheelers'], color=TEAL_PRIMARY, alpha=0.25, label='2-Wheelers (92.6%)')
    sub_ax1.plot(range(len(m)), m['2-Wheelers'], color=TEAL_PRIMARY, linewidth=2.2)
    sub_ax1.plot(range(len(m)), m['4-Wheelers'], color=AMBER_ACCENT, linewidth=1.8, label='4-Wheelers (7.4%)')
    sub_ax1.set_facecolor(CARD_BG)
    sub_ax1.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.7, alpha=0.8)
    sub_ax1.set_xticks(range(0, len(m), 4))
    sub_ax1.set_xticklabels([m.index[i] for i in range(0, len(m), 4)], fontsize=7.5, color=TEXT_MUTED)
    sub_ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f'{int(v/1000)}k'))
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax1.legend(loc='upper left', frameon=False, fontsize=8)
    for spine in sub_ax1.spines.values():
        spine.set_color(BORDER_COLOR)

    # Visual 2 (Right Middle): EV Category Comparison
    ax.add_patch(patches.FancyBboxPatch((0.66, 0.32), 0.315, 0.385, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.675, 0.675, "EV Volume by Category", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.675, 0.655, "Volume split and segment penetration rates", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax2 = fig.add_axes([0.69, 0.37, 0.26, 0.25])
    cats = ['2-Wheelers', '4-Wheelers']
    vols = [1913168, 152943]
    colors = [TEAL_PRIMARY, AMBER_ACCENT]
    bars = sub_ax2.barh(cats, [v/1000 for v in vols], color=colors, height=0.45)
    sub_ax2.set_facecolor(CARD_BG)
    sub_ax2.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
    sub_ax2.set_xlabel("Volume (in Thousands)", fontsize=8, color=TEXT_MUTED)
    for b, val, pct in zip(bars, vols, ['92.6%', '7.4%']):
        sub_ax2.text(b.get_width() + 40, b.get_y() + b.get_height()/2, f"{val:,}\n({pct})", va='center', fontsize=7.5, weight='bold', color=TEXT_MAIN)
    sub_ax2.set_xlim(0, 2350)
    for spine in sub_ax2.spines.values():
        spine.set_color(BORDER_COLOR)

    # Bottom Left: Top 10 States by EV Registrations
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.02), 0.46, 0.28, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.035, 0.268, "Top 10 States by EV Registrations", fontsize=10, weight='bold', color=TEXT_MAIN, zorder=3)
    
    sub_ax3 = fig.add_axes([0.05, 0.045, 0.41, 0.20])
    top_states = df_state.groupby('state')['electric_vehicles_sold'].sum().sort_values(ascending=False).head(10)
    sub_ax3.barh(top_states.index[::-1], top_states.values[::-1] / 1000, color=TEAL_PRIMARY, height=0.6)
    sub_ax3.set_facecolor(CARD_BG)
    sub_ax3.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=7)
    sub_ax3.set_xlabel("EV Registrations (Thousands)", fontsize=7.5, color=TEXT_MUTED)
    for spine in sub_ax3.spines.values():
        spine.set_color(BORDER_COLOR)

    # Bottom Right 1: FY-wise EV Growth
    ax.add_patch(patches.FancyBboxPatch((0.50, 0.02), 0.26, 0.28, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.515, 0.268, "Annual EV Growth (FY22 – FY24)", fontsize=10, weight='bold', color=TEXT_MAIN, zorder=3)

    sub_ax4 = fig.add_axes([0.53, 0.05, 0.21, 0.19])
    fys = ['FY 2022', 'FY 2023', 'FY 2024']
    fy_vols = [271150, 775368, 1019593]
    b4 = sub_ax4.bar(fys, [v/1000 for v in fy_vols], color=BLUE_SECONDARY, width=0.5)
    sub_ax4.set_facecolor(CARD_BG)
    sub_ax4.grid(axis='y', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax4.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax4.set_ylabel("Sales (Thousands)", fontsize=7.5, color=TEXT_MUTED)
    sub_ax4.set_ylim(0, 1250)
    for b, val, gr in zip(b4, fy_vols, ['Base', '+186.0%', '+31.5%']):
        sub_ax4.text(b.get_x() + b.get_width()/2, b.get_height() + 25, f"{int(val/1000)}k\n({gr})", ha='center', fontsize=7, weight='bold', color=TEXT_MAIN)
    for spine in sub_ax4.spines.values():
        spine.set_color(BORDER_COLOR)

    # Bottom Right 2: Executive Insight Callout Box
    ax.add_patch(patches.FancyBboxPatch((0.78, 0.02), 0.195, 0.28, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.795, 0.268, "EXECUTIVE INSIGHT", fontsize=9, weight='bold', color=TEAL_PRIMARY, zorder=3)
    insight_text = (
        "• Market Momentum: EV sales surpassed the 1M milestone in FY2024 (1,019,593 units), representing a 93.9% 2-year CAGR.\n\n"
        "• Segment Reality: 2-Wheelers represent 92.6% of adoption with 4.39% penetration, while 4-Wheelers (1.12% penetration) remain infrastructure-constrained.\n\n"
        "• Geographic Scale: Top 5 states generate 55.06% of nationwide registrations, led by Maharashtra (396k units)."
    )
    ax.text(0.795, 0.125, insight_text, fontsize=7.2, color=TEXT_MAIN, zorder=3, wrap=True, va='center')

    save_path = config.SCREENSHOTS_DIR / "page1_executive_overview.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path


# -------------------------------------------------------------------------------------------------
# PAGE 2: STATE-LEVEL MARKET ANALYSIS
# -------------------------------------------------------------------------------------------------
def generate_page2():
    fig = plt.figure(figsize=(16, 9), dpi=200, facecolor=BG_CANVAS)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_CANVAS)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    draw_header_and_nav(ax, active_tab="State Performance")

    # 4 KPI Cards
    draw_card(ax, 0.02, 0.725, 0.22, 0.115, "Total EV Registrations", "2,066,111", "34 States & Territories", "100% Volume", TEAL_PRIMARY)
    draw_card(ax, 0.26, 0.725, 0.22, 0.115, "Top Volume State", "Maharashtra (396,045)", "19.17% National Share", "Rank #1", TEAL_PRIMARY)
    draw_card(ax, 0.50, 0.725, 0.22, 0.115, "Top 5 States Contribution", "55.06%", "1,140,857 Combined Units", "High Concentration", BLUE_SECONDARY)
    draw_card(ax, 0.74, 0.725, 0.24, 0.115, "Avg Registrations / State", "60,768", "Median: 12,878 Units", "Wide Disparity", AMBER_ACCENT)

    # Left: State EV Registration Ranking (Top 15 States)
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.02), 0.46, 0.685, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.035, 0.675, "State EV Registration Ranking (Top 15 States)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.035, 0.655, "Volume, national share %, and EV penetration rate comparison", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax1 = fig.add_axes([0.05, 0.05, 0.41, 0.58])
    df_state = pd.read_csv(config.PROCESSED_STATE_SALES)
    st_agg = df_state.groupby('state').agg(
        ev=('electric_vehicles_sold', 'sum'),
        tot=('total_vehicles_sold', 'sum')
    ).reset_index()
    st_agg['pen'] = (st_agg['ev'] / st_agg['tot']) * 100
    st_agg['share'] = (st_agg['ev'] / 2066111) * 100
    top15 = st_agg.sort_values(by='ev', ascending=False).head(15)

    bars = sub_ax1.barh(top15['state'][::-1], top15['ev'][::-1] / 1000, color=TEAL_PRIMARY, height=0.6)
    sub_ax1.set_facecolor(CARD_BG)
    sub_ax1.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax1.set_xlabel("EV Registrations (Thousands)", fontsize=8, color=TEXT_MUTED)
    for b, pen, sh in zip(bars, top15['pen'][::-1], top15['share'][::-1]):
        sub_ax1.text(b.get_width() + 4, b.get_y() + b.get_height()/2, f"{b.get_width():.0f}k ({sh:.1f}% sh | {pen:.1f}% pen)",
                     va='center', fontsize=6.8, weight='bold', color=TEXT_MAIN)
    sub_ax1.set_xlim(0, 480)
    for spine in sub_ax1.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right Top: Strategic Quadrant Scatter (EV Volume vs Penetration Rate)
    ax.add_patch(patches.FancyBboxPatch((0.50, 0.36), 0.48, 0.345, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.515, 0.675, "Strategic Quadrant: EV Registrations vs. Penetration Rate (%)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.515, 0.655, "Identifies high-volume scale drivers vs high-adoption density test markets", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax2 = fig.add_axes([0.54, 0.40, 0.42, 0.23])
    sub_ax2.scatter(st_agg['ev'] / 1000, st_agg['pen'], color=BLUE_SECONDARY, s=st_agg['tot']/100000 + 40, alpha=0.7, edgecolors='white', linewidth=1)
    sub_ax2.axvline(60.7, color=BORDER_COLOR, linestyle='--', linewidth=1)
    sub_ax2.axhline(3.61, color=BORDER_COLOR, linestyle='--', linewidth=1)
    sub_ax2.set_facecolor(CARD_BG)
    sub_ax2.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.7, alpha=0.6)
    sub_ax2.set_xlabel("EV Registrations (Thousands)", fontsize=7.5, color=TEXT_MUTED)
    sub_ax2.set_ylabel("EV Penetration Rate (%)", fontsize=7.5, color=TEXT_MUTED)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=7)

    # Highlight key states
    key_states = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Goa', 'Delhi', 'Kerala', 'Gujarat', 'Uttar Pradesh']
    for _, r in st_agg[st_agg['state'].isin(key_states)].iterrows():
        sub_ax2.annotate(r['state'], (r['ev']/1000, r['pen']), textcoords="offset points", xytext=(4, 4), fontsize=6.8, weight='bold', color=TEXT_MAIN)
    for spine in sub_ax2.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right Bottom: Regional Contribution Matrix
    ax.add_patch(patches.FancyBboxPatch((0.50, 0.02), 0.48, 0.32, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.515, 0.308, "Regional Performance Breakdown (Macro Zones)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.515, 0.288, "Aggregates states by geographical zones with national share %", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax3 = fig.add_axes([0.54, 0.05, 0.42, 0.21])
    dim_st = pd.read_csv(config.PROCESSED_STATE_DIM)
    reg_df = df_state.merge(dim_st, on='state_id').groupby('region').agg(
        ev=('electric_vehicles_sold', 'sum'),
        tot=('total_vehicles_sold', 'sum')
    ).reset_index()
    reg_df['pen'] = (reg_df['ev'] / reg_df['tot']) * 100
    reg_df['sh'] = (reg_df['ev'] / 2066111) * 100
    reg_df = reg_df.sort_values(by='ev', ascending=True)

    b3 = sub_ax3.barh(reg_df['region'], reg_df['ev'] / 1000, color=BLUE_SECONDARY, height=0.55)
    sub_ax3.set_facecolor(CARD_BG)
    sub_ax3.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax3.set_xlabel("EV Registrations (Thousands)", fontsize=8, color=TEXT_MUTED)
    for b, sh, pen in zip(b3, reg_df['sh'], reg_df['pen']):
        sub_ax3.text(b.get_width() + 8, b.get_y() + b.get_height()/2, f"{b.get_width():.0f}k ({sh:.1f}% share | {pen:.1f}% pen)",
                     va='center', fontsize=7, weight='bold', color=TEXT_MAIN)
    sub_ax3.set_xlim(0, 850)
    for spine in sub_ax3.spines.values():
        spine.set_color(BORDER_COLOR)

    save_path = config.SCREENSHOTS_DIR / "page2_state_performance.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path


# -------------------------------------------------------------------------------------------------
# PAGE 3: MANUFACTURER ANALYSIS
# -------------------------------------------------------------------------------------------------
def generate_page3():
    fig = plt.figure(figsize=(16, 9), dpi=200, facecolor=BG_CANVAS)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_CANVAS)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    draw_header_and_nav(ax, active_tab="Manufacturer Analysis")

    # 6 KPI Cards
    draw_card(ax, 0.02, 0.725, 0.145, 0.115, "Total OEMs Tracked", "26", "16 in 2W | 10 in 4W", "Active Market", BLUE_SECONDARY)
    draw_card(ax, 0.18, 0.725, 0.145, 0.115, "Overall OEM Leader", "Ola Electric", "489,473 Units Sold", "23.69% Overall", TEAL_PRIMARY)
    draw_card(ax, 0.34, 0.725, 0.145, 0.115, "Leading 2W Maker", "Ola Electric", "25.58% 2W Share", "2W Champion", TEAL_PRIMARY)
    draw_card(ax, 0.50, 0.725, 0.145, 0.115, "Leading 4W Maker", "Tata Motors", "58.15% 4W Share", "88,935 Units", AMBER_ACCENT)
    draw_card(ax, 0.66, 0.725, 0.145, 0.115, "2W HHI Concentration", "1,482", "Moderate / Competitive", "Healthy", BLUE_SECONDARY)
    draw_card(ax, 0.82, 0.725, 0.155, 0.115, "4W HHI Concentration", "4,211", "Highly Concentrated", "Duopoly", AMBER_ACCENT)

    # Left: Top 10 Manufacturers Market Share
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.02), 0.46, 0.685, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.035, 0.675, "Top 10 Manufacturers Overall (Volume & Market Share)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.035, 0.655, "Cumulative nationwide registrations across all tracked vehicle categories", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax1 = fig.add_axes([0.05, 0.05, 0.41, 0.58])
    df_maker = pd.read_csv(config.PROCESSED_MAKER_SALES)
    top10_m = df_maker.groupby('maker')['electric_vehicles_sold'].sum().sort_values(ascending=False).head(10)
    colors = [TEAL_PRIMARY if m != 'Tata Motors' and m != 'Mahindra & Mahindra' else AMBER_ACCENT for m in top10_m.index[::-1]]
    bars = sub_ax1.barh(top10_m.index[::-1], top10_m.values[::-1] / 1000, color=colors, height=0.6)
    sub_ax1.set_facecolor(CARD_BG)
    sub_ax1.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax1.set_xlabel("EV Registrations (Thousands)", fontsize=8, color=TEXT_MUTED)
    for b, val in zip(bars, top10_m.values[::-1]):
        sh = (val / 2066111) * 100
        sub_ax1.text(b.get_width() + 6, b.get_y() + b.get_height()/2, f"{val:,} ({sh:.1f}%)", va='center', fontsize=7, weight='bold', color=TEXT_MAIN)
    sub_ax1.set_xlim(0, 580)
    for spine in sub_ax1.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right Top: 2W vs 4W Segment Leaders
    ax.add_patch(patches.FancyBboxPatch((0.50, 0.36), 0.48, 0.345, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.515, 0.675, "Segment-Specific OEM Leadership (2W vs 4W)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.515, 0.655, "Market share distribution within each distinct vehicle category", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax2 = fig.add_axes([0.53, 0.40, 0.20, 0.23])
    m2w = df_maker[df_maker['vehicle_category'] == '2-Wheelers'].groupby('maker')['electric_vehicles_sold'].sum().sort_values(ascending=False).head(5)
    sub_ax2.barh(m2w.index[::-1], m2w.values[::-1] / 1000, color=TEAL_PRIMARY, height=0.55)
    sub_ax2.set_title("Top 2W OEMs", fontsize=8.5, weight='bold', color=TEXT_MAIN)
    sub_ax2.set_facecolor(CARD_BG)
    sub_ax2.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=7)
    sub_ax2.set_xlabel("Units (k)", fontsize=7, color=TEXT_MUTED)
    for spine in sub_ax2.spines.values():
        spine.set_color(BORDER_COLOR)

    sub_ax3 = fig.add_axes([0.76, 0.40, 0.20, 0.23])
    m4w = df_maker[df_maker['vehicle_category'] == '4-Wheelers'].groupby('maker')['electric_vehicles_sold'].sum().sort_values(ascending=False).head(5)
    sub_ax3.barh(m4w.index[::-1], m4w.values[::-1] / 1000, color=AMBER_ACCENT, height=0.55)
    sub_ax3.set_title("Top 4W OEMs", fontsize=8.5, weight='bold', color=TEXT_MAIN)
    sub_ax3.set_facecolor(CARD_BG)
    sub_ax3.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax3.tick_params(colors=TEXT_MUTED, labelsize=7)
    sub_ax3.set_xlabel("Units (k)", fontsize=7, color=TEXT_MUTED)
    for spine in sub_ax3.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right Bottom: Concentration Analysis & Analytical Callout
    ax.add_patch(patches.FancyBboxPatch((0.50, 0.02), 0.48, 0.32, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.515, 0.308, "Herfindahl-Hirschman Index (HHI) & Market Structure", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    
    hhi_desc = (
        "• 2-Wheeler Market (HHI = 1,482 - Moderately Concentrated):\n"
        "  Characterized by intense OEM mobility. Early pioneer Hero Electric held 28.2% in FY22 but plummeted to <1.5% by FY24.\n"
        "  Ola Electric captured 25.58% market share, with legacy players (TVS: 14.3%, Bajaj: 7.6%) scaling up rapidly.\n\n"
        "• 4-Wheeler Market (HHI = 4,211 - Highly Concentrated Oligopoly):\n"
        "  Tata Motors commands an overwhelming 58.15% monopoly share, followed by Mahindra & Mahindra (26.93%).\n"
        "  The top 2 players control 85.08% of all passenger EV registrations in India."
    )
    ax.text(0.515, 0.16, hhi_desc, fontsize=7.8, color=TEXT_MAIN, zorder=3, wrap=True, va='center')

    save_path = config.SCREENSHOTS_DIR / "page3_manufacturer_analysis.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path


# -------------------------------------------------------------------------------------------------
# PAGE 4: VEHICLE CATEGORY ANALYSIS
# -------------------------------------------------------------------------------------------------
def generate_page4():
    fig = plt.figure(figsize=(16, 9), dpi=200, facecolor=BG_CANVAS)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_CANVAS)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    draw_header_and_nav(ax, active_tab="Vehicle Category")

    # 6 KPI Cards
    draw_card(ax, 0.02, 0.725, 0.145, 0.115, "2W Registrations", "1,913,168", "Two-Wheeler Volume", "92.60% Total", TEAL_PRIMARY)
    draw_card(ax, 0.18, 0.725, 0.145, 0.115, "2W Penetration Rate", "4.39%", "1.91M / 43.5M Total 2W", "Fastest Segment", TEAL_PRIMARY)
    draw_card(ax, 0.34, 0.725, 0.145, 0.115, "4W Registrations", "152,943", "Passenger Car Volume", "7.40% Total", AMBER_ACCENT)
    draw_card(ax, 0.50, 0.725, 0.145, 0.115, "4W Penetration Rate", "1.12%", "153k / 13.7M Total 4W", "Adoption Gap", AMBER_ACCENT)
    draw_card(ax, 0.66, 0.725, 0.145, 0.115, "2W Market Leader", "Ola Electric", "489,473 Units Sold", "25.58% Share", TEAL_PRIMARY)
    draw_card(ax, 0.82, 0.725, 0.155, 0.115, "4W Market Leader", "Tata Motors", "88,935 Units Sold", "58.15% Share", AMBER_ACCENT)

    # Left: 2W vs 4W Monthly Sales Divergence
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.02), 0.56, 0.685, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.035, 0.675, "2W vs. 4W Monthly Registration Divergence (FY22 – FY24)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.035, 0.655, "Two-wheelers show exponential scaling; four-wheelers maintain steady baseline", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax1 = fig.add_axes([0.05, 0.07, 0.51, 0.55])
    df_state = pd.read_csv(config.PROCESSED_STATE_SALES)
    df_date = pd.read_csv(config.PROCESSED_DATE_DIM)
    m = df_state.merge(df_date, on='date').groupby(['year_month', 'vehicle_category'])['electric_vehicles_sold'].sum().unstack().fillna(0)
    
    sub_ax1.plot(range(len(m)), m['2-Wheelers'] / 1000, color=TEAL_PRIMARY, linewidth=2.5, marker='o', markersize=4, label='2-Wheelers (Peak: 139k/mo)')
    sub_ax1.plot(range(len(m)), m['4-Wheelers'] / 1000, color=AMBER_ACCENT, linewidth=2.2, marker='s', markersize=4, label='4-Wheelers (Peak: 9.5k/mo)')
    sub_ax1.set_facecolor(CARD_BG)
    sub_ax1.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax1.set_xticks(range(0, len(m), 4))
    sub_ax1.set_xticklabels([m.index[i] for i in range(0, len(m), 4)], fontsize=7.5, color=TEXT_MUTED)
    sub_ax1.set_ylabel("Monthly Registrations (Thousands)", fontsize=8, color=TEXT_MUTED)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax1.legend(loc='upper left', frameon=False, fontsize=8.5)
    for spine in sub_ax1.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right: Penetration Rate & Category Insights
    ax.add_patch(patches.FancyBboxPatch((0.60, 0.36), 0.38, 0.345, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.615, 0.675, "Electrification Rate Comparison (%)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    
    sub_ax2 = fig.add_axes([0.63, 0.40, 0.33, 0.23])
    segs = ['2-Wheelers', 'Overall Market', '4-Wheelers']
    pens = [4.39, 3.61, 1.12]
    colors = [TEAL_PRIMARY, BLUE_SECONDARY, AMBER_ACCENT]
    b2 = sub_ax2.bar(segs, pens, color=colors, width=0.45)
    sub_ax2.set_facecolor(CARD_BG)
    sub_ax2.grid(axis='y', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax2.set_ylabel("Penetration %", fontsize=7.5, color=TEXT_MUTED)
    sub_ax2.set_ylim(0, 5.5)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    for b, p in zip(b2, pens):
        sub_ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 0.15, f"{p:.2f}%", ha='center', fontsize=8, weight='bold', color=TEXT_MAIN)
    for spine in sub_ax2.spines.values():
        spine.set_color(BORDER_COLOR)

    ax.add_patch(patches.FancyBboxPatch((0.60, 0.02), 0.38, 0.32, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.615, 0.308, "KEY STRATEGIC TAKEAWAYS", fontsize=9.5, weight='bold', color=TEAL_PRIMARY, zorder=3)
    takeaways = (
        "1. Adoption Asymmetry: 2-Wheelers electrify ~4x faster than passenger cars due to upfront TCO parity, smaller battery capacities (2–4 kWh), and simple home plug-in charging.\n\n"
        "2. Infrastructure Dependency: 4W expansion remains tethered to intercity fast-charging networks and higher vehicle purchase prices ($15k+ vs $1.2k).\n\n"
        "3. Supply Chain Alignment: Commercial investment in battery cell assembly and component localization should prioritize 2W form factors for immediate volume throughput."
    )
    ax.text(0.615, 0.16, takeaways, fontsize=7.6, color=TEXT_MAIN, zorder=3, wrap=True, va='center')

    save_path = config.SCREENSHOTS_DIR / "page4_vehicle_category.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path


# -------------------------------------------------------------------------------------------------
# PAGE 5: TRENDS & CHARGING INFRASTRUCTURE
# -------------------------------------------------------------------------------------------------
def generate_page5():
    fig = plt.figure(figsize=(16, 9), dpi=200, facecolor=BG_CANVAS)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_CANVAS)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    draw_header_and_nav(ax, active_tab="Trends & Infrastructure")

    # 4 KPI Cards
    draw_card(ax, 0.02, 0.725, 0.22, 0.115, "Public Charging Stations", "11,664", "BEE Operational PCS", "32 States/UTs", TEAL_PRIMARY)
    draw_card(ax, 0.26, 0.725, 0.22, 0.115, "National Infrastructure Ratio", "177.1 EVs / PCS", "2.07M EVs / 11,664 PCS", "Network Stress", BLUE_SECONDARY)
    draw_card(ax, 0.50, 0.725, 0.22, 0.115, "Top Infrastructure State", "Maharashtra (3,079 PCS)", "26.40% National PCS", "Leader", TEAL_PRIMARY)
    draw_card(ax, 0.74, 0.725, 0.24, 0.115, "Highest Charger Density", "Delhi (68.1 EVs / PCS)", "1,886 PCS / 128k EVs", "Best Ratio", TEAL_PRIMARY)

    # Left: EV Registrations vs Charging Stations Scatter Plot
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.02), 0.48, 0.685, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.035, 0.675, "EV Registrations vs. Operational Charging Stations by State", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.035, 0.655, "Strong positive correlation (r = 0.77); bubble size represents total automotive volume", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax1 = fig.add_axes([0.05, 0.07, 0.43, 0.55])
    df_state = pd.read_csv(config.PROCESSED_STATE_SALES)
    dim_st = pd.read_csv(config.PROCESSED_STATE_DIM)
    st_ev = df_state.groupby('state')['electric_vehicles_sold'].sum().reset_index()
    m_infra = st_ev.merge(dim_st, left_on='state', right_on='state_name')
    m_infra = m_infra[m_infra['operational_pcs'] > 0]

    sub_ax1.scatter(m_infra['operational_pcs'], m_infra['electric_vehicles_sold'] / 1000,
                    color=TEAL_PRIMARY, s=90, alpha=0.75, edgecolors=BORDER_COLOR, linewidth=1)
    
    # Regression trendline
    z = np.polyfit(m_infra['operational_pcs'], m_infra['electric_vehicles_sold'] / 1000, 1)
    p = np.poly1d(z)
    sub_ax1.plot(m_infra['operational_pcs'], p(m_infra['operational_pcs']), color=BLUE_SECONDARY, linestyle='--', linewidth=1.5, label='Trendline (r = 0.77)')

    # Labels for top states
    for _, r in m_infra.sort_values(by='electric_vehicles_sold', ascending=False).head(7).iterrows():
        sub_ax1.annotate(r['state'], (r['operational_pcs'], r['electric_vehicles_sold'] / 1000),
                         textcoords="offset points", xytext=(4, 4), fontsize=7, weight='bold', color=TEXT_MAIN)

    sub_ax1.set_facecolor(CARD_BG)
    sub_ax1.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax1.set_xlabel("Operational Public Charging Stations (BEE)", fontsize=8, color=TEXT_MUTED)
    sub_ax1.set_ylabel("EV Registrations (Thousands)", fontsize=8, color=TEXT_MUTED)
    sub_ax1.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax1.legend(loc='lower right', frameon=False, fontsize=8)
    for spine in sub_ax1.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right Top: Top 10 Charging Infrastructure States
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.36), 0.46, 0.345, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.535, 0.675, "Top 10 States by Public Charging Stations (PCS)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.535, 0.655, "Top 3 states host over 51.5% of national public charging infrastructure", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax2 = fig.add_axes([0.55, 0.40, 0.41, 0.23])
    top_pcs = dim_st.sort_values(by='operational_pcs', ascending=False).head(10)
    sub_ax2.barh(top_pcs['state_name'][::-1], top_pcs['operational_pcs'][::-1], color=BLUE_SECONDARY, height=0.6)
    sub_ax2.set_facecolor(CARD_BG)
    sub_ax2.grid(axis='x', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax2.tick_params(colors=TEXT_MUTED, labelsize=7.5)
    sub_ax2.set_xlabel("Operational PCS", fontsize=8, color=TEXT_MUTED)
    for spine in sub_ax2.spines.values():
        spine.set_color(BORDER_COLOR)

    # Right Bottom: Infrastructure Stress Ratio (EVs per Charging Station)
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.02), 0.46, 0.32, boxstyle="round,pad=0.006,rounding_size=0.012",
                                       facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.535, 0.308, "Infrastructure Stress Ratio (EVs per Operational Charger)", fontsize=10.5, weight='bold', color=TEXT_MAIN, zorder=3)
    ax.text(0.535, 0.288, "Lower ratio indicates better charger availability relative to vehicle volume", fontsize=8, color=TEXT_MUTED, zorder=3)

    sub_ax3 = fig.add_axes([0.55, 0.05, 0.41, 0.21])
    m_infra['ratio'] = m_infra['electric_vehicles_sold'] / m_infra['operational_pcs']
    stress_sample = m_infra.sort_values(by='electric_vehicles_sold', ascending=False).head(8)
    bars3 = sub_ax3.bar(stress_sample['state'], stress_sample['ratio'], color=TEAL_PRIMARY, width=0.55)
    sub_ax3.axhline(177.1, color=AMBER_ACCENT, linestyle='--', linewidth=1.2, label='National Avg (177.1)')
    sub_ax3.set_facecolor(CARD_BG)
    sub_ax3.grid(axis='y', color=BORDER_COLOR, linestyle='--', linewidth=0.7)
    sub_ax3.tick_params(axis='x', rotation=30, colors=TEXT_MUTED, labelsize=7)
    sub_ax3.tick_params(axis='y', colors=TEXT_MUTED, labelsize=7)
    sub_ax3.set_ylabel("EVs / Charger", fontsize=7.5, color=TEXT_MUTED)
    sub_ax3.legend(loc='upper right', frameon=False, fontsize=7.5)
    for b in bars3:
        sub_ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 8, f"{int(b.get_height())}", ha='center', fontsize=6.8, weight='bold', color=TEXT_MAIN)
    for spine in sub_ax3.spines.values():
        spine.set_color(BORDER_COLOR)

    save_path = config.SCREENSHOTS_DIR / "page5_trends_infrastructure.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path


def generate_all_dashboard_pages():
    print("=== Generating 5 Executive-Level Dashboard Pages (Light Theme) ===")
    p1 = generate_page1()
    print(f" [x] Page 1: {p1.name}")
    p2 = generate_page2()
    print(f" [x] Page 2: {p2.name}")
    p3 = generate_page3()
    print(f" [x] Page 3: {p3.name}")
    p4 = generate_page4()
    print(f" [x] Page 4: {p4.name}")
    p5 = generate_page5()
    print(f" [x] Page 5: {p5.name}")
    print("=== All 5 Executive Dashboard Pages Generated Successfully! ===")


if __name__ == '__main__':
    generate_all_dashboard_pages()
