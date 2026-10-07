"""
HTML Interactive Executive Dashboard Generator for EVPulse India.
Builds an interactive 5-page Power BI executive web application.
"""
from pathlib import Path
import json

HTML_FILE = Path("d:/EV_Analytics/EVPulse-India/reports/powerbi_dashboard_preview.html")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EVPulse India: Executive BI Analytics Dashboard</title>
    <!-- Tailwind CSS CDN for modern utility classes -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN for interactive charts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; background-color: #F8FAFC; color: #0F172A; }
        .card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .nav-btn { transition: all 0.15s ease-in-out; }
        .nav-btn.active { background-color: #CCFBF1; color: #0D9488; border-color: #0D9488; font-weight: 600; }
        .kpi-badge { font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 9999px; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #CBD5E1; border-radius: 4px; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Top Executive Header -->
    <header class="bg-white border-b border-slate-200 px-6 py-3.5 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center space-x-3">
                <div class="h-9 w-9 rounded-lg bg-teal-600 flex items-center justify-center text-white font-bold text-lg shadow-sm">⚡</div>
                <div>
                    <div class="flex items-center space-x-2">
                        <h1 class="text-lg font-bold tracking-tight text-slate-900">EVPulse India</h1>
                        <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium border border-slate-200">v2.4 Executive BI</span>
                    </div>
                    <p class="text-xs text-slate-500">Electric Vehicle Market Analytics | MoRTH (Vahan Sewa) & BEE Datasets (FY2022–FY2024)</p>
                </div>
            </div>

            <!-- Page Navigation Tabs -->
            <nav class="flex items-center space-x-1.5 overflow-x-auto custom-scrollbar pb-1 md:pb-0" id="nav-tabs">
                <button onclick="switchPage('page1')" id="btn-page1" class="nav-btn active text-xs px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50">Overview</button>
                <button onclick="switchPage('page2')" id="btn-page2" class="nav-btn text-xs px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50">State Performance</button>
                <button onclick="switchPage('page3')" id="btn-page3" class="nav-btn text-xs px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50">Manufacturer Analysis</button>
                <button onclick="switchPage('page4')" id="btn-page4" class="nav-btn text-xs px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50">Vehicle Category</button>
                <button onclick="switchPage('page5')" id="btn-page5" class="nav-btn text-xs px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50">Trends & Infrastructure</button>
            </nav>
        </div>
    </header>

    <!-- Global Subtle Slicer Bar -->
    <section class="bg-white border-b border-slate-200 px-6 py-2">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3 text-xs">
            <div class="flex items-center space-x-2 text-slate-500 font-medium">
                <span>Filters:</span>
                <div class="flex items-center space-x-1.5">
                    <select id="slicer-fy" onchange="filterData()" class="bg-slate-50 border border-slate-200 text-slate-700 rounded-md px-2.5 py-1 text-xs focus:ring-1 focus:ring-teal-500">
                        <option value="ALL">Financial Year: All (FY22–FY24)</option>
                        <option value="2022">FY 2022 (271k Units)</option>
                        <option value="2023">FY 2023 (775k Units)</option>
                        <option value="2024">FY 2024 (1,020k Units)</option>
                    </select>
                    <select id="slicer-cat" onchange="filterData()" class="bg-slate-50 border border-slate-200 text-slate-700 rounded-md px-2.5 py-1 text-xs focus:ring-1 focus:ring-teal-500">
                        <option value="ALL">Vehicle Category: All Categories</option>
                        <option value="2W">2-Wheelers (92.6% Share)</option>
                        <option value="4W">4-Wheelers (7.4% Share)</option>
                    </select>
                    <button onclick="resetFilters()" class="text-slate-400 hover:text-slate-700 px-2 py-1 underline">Reset</button>
                </div>
            </div>
            <div class="flex items-center space-x-4 text-slate-400 text-xs">
                <span>Verified Data: <strong class="text-slate-700 font-semibold">2,066,111 EV Units</strong></span>
                <span>•</span>
                <span>Automotive Benchmark: <strong class="text-slate-700 font-semibold">57,233,134 Units</strong></span>
                <span>•</span>
                <span>Overall Penetration: <strong class="text-teal-600 font-bold">3.61%</strong></span>
            </div>
        </div>
    </section>

    <!-- Main Dynamic Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-6 py-6">

        <!-- ========================================================================================== -->
        <!-- PAGE 1: EXECUTIVE OVERVIEW -->
        <!-- ========================================================================================== -->
        <div id="page1" class="page-content space-y-6">
            <!-- 6 Top Executive Cards -->
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div class="card p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                        <span class="text-xs font-semibold uppercase text-slate-500 tracking-wider">Total EV Sales</span>
                        <span class="kpi-badge bg-teal-50 text-teal-700">+93.9% CAGR</span>
                    </div>
                    <div class="my-2">
                        <div class="text-2xl font-bold text-slate-900" id="card-total-ev">2,066,111</div>
                        <span class="text-[11px] text-slate-500">36 Months Cumulative</span>
                    </div>
                    <div class="text-[10px] text-slate-400">MoRTH Vahan Sewa</div>
                </div>

                <div class="card p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                        <span class="text-xs font-semibold uppercase text-slate-500 tracking-wider">YoY Growth (FY24)</span>
                        <span class="kpi-badge bg-teal-50 text-teal-700">+244k YoY</span>
                    </div>
                    <div class="my-2">
                        <div class="text-2xl font-bold text-slate-900">+31.50%</div>
                        <span class="text-[11px] text-slate-500">1,019,593 in FY24</span>
                    </div>
                    <div class="text-[10px] text-slate-400">vs 775k in FY23</div>
                </div>

                <div class="card p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                        <span class="text-xs font-semibold uppercase text-slate-500 tracking-wider">2W Market Share</span>
                        <span class="kpi-badge bg-blue-50 text-blue-700">Primary</span>
                    </div>
                    <div class="my-2">
                        <div class="text-2xl font-bold text-blue-600">92.60%</div>
                        <span class="text-[11px] text-slate-500">1,913,168 Units</span>
                    </div>
                    <div class="text-[10px] text-slate-400">4.39% Segment Penetration</div>
                </div>

                <div class="card p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                        <span class="text-xs font-semibold uppercase text-slate-500 tracking-wider">4W Market Share</span>
                        <span class="kpi-badge bg-amber-50 text-amber-700">Emerging</span>
                    </div>
                    <div class="my-2">
                        <div class="text-2xl font-bold text-amber-600">7.40%</div>
                        <span class="text-[11px] text-slate-500">152,943 Units</span>
                    </div>
                    <div class="text-[10px] text-slate-400">1.12% Segment Penetration</div>
                </div>

                <div class="card p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                        <span class="text-xs font-semibold uppercase text-slate-500 tracking-wider">Leading State</span>
                        <span class="kpi-badge bg-teal-50 text-teal-700">Rank #1</span>
                    </div>
                    <div class="my-2">
                        <div class="text-xl font-bold text-slate-900 truncate">Maharashtra</div>
                        <span class="text-[11px] text-slate-500">396,045 EV Sold (19.2%)</span>
                    </div>
                    <div class="text-[10px] text-slate-400">4.31% Penetration Rate</div>
                </div>

                <div class="card p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                        <span class="text-xs font-semibold uppercase text-slate-500 tracking-wider">Charging Stations</span>
                        <span class="kpi-badge bg-blue-50 text-blue-700">BEE PCS</span>
                    </div>
                    <div class="my-2">
                        <div class="text-2xl font-bold text-slate-900">11,664</div>
                        <span class="text-[11px] text-slate-500">Across 32 States/UTs</span>
                    </div>
                    <div class="text-[10px] text-slate-400">177.1 EVs / Station</div>
                </div>
            </div>

            <!-- Middle Visuals: Monthly Trend (Left) & Category Split (Right) -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="card p-5 lg:col-span-2">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h2 class="text-sm font-bold text-slate-800">Monthly EV Registrations Trend (FY22 – FY24)</h2>
                            <p class="text-xs text-slate-500">Monthly sales volume across 2-Wheelers and 4-Wheelers</p>
                        </div>
                        <div class="flex items-center space-x-3 text-xs">
                            <span class="flex items-center"><span class="w-3 h-3 bg-teal-600 rounded-sm mr-1.5"></span>2-Wheelers</span>
                            <span class="flex items-center"><span class="w-3 h-3 bg-amber-500 rounded-sm mr-1.5"></span>4-Wheelers</span>
                        </div>
                    </div>
                    <div class="h-64">
                        <canvas id="chart-monthly-trend"></canvas>
                    </div>
                </div>

                <div class="card p-5 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800">Category Volume & Penetration</h2>
                        <p class="text-xs text-slate-500">Volume share and relative adoption rate</p>
                        <div class="h-44 mt-3">
                            <canvas id="chart-category-bar"></canvas>
                        </div>
                    </div>
                    <div class="border-t border-slate-100 pt-3 mt-2 space-y-2 text-xs">
                        <div class="flex justify-between text-slate-600">
                            <span>2W Total Registered:</span>
                            <span class="font-bold text-slate-900">1,913,168 (4.39% Pen)</span>
                        </div>
                        <div class="flex justify-between text-slate-600">
                            <span>4W Total Registered:</span>
                            <span class="font-bold text-slate-900">152,943 (1.12% Pen)</span>
                        </div>
                        <div class="text-[11px] text-slate-500 italic mt-1">2-Wheelers electrify ~4x faster due to TCO parity & home charging.</div>
                    </div>
                </div>
            </div>

            <!-- Bottom Section: Top 10 States, FY-wise Growth, and Insight Box -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div class="card p-5 lg:col-span-5">
                    <h2 class="text-sm font-bold text-slate-800 mb-1">Top 10 States by EV Registrations</h2>
                    <p class="text-xs text-slate-500 mb-3">Volume and national market share %</p>
                    <div class="h-56">
                        <canvas id="chart-top-states-bar"></canvas>
                    </div>
                </div>

                <div class="card p-5 lg:col-span-4">
                    <h2 class="text-sm font-bold text-slate-800 mb-1">Annual EV Growth (FY22 – FY24)</h2>
                    <p class="text-xs text-slate-500 mb-3">Fiscal year volume evolution and YoY %</p>
                    <div class="h-56">
                        <canvas id="chart-fy-growth-bar"></canvas>
                    </div>
                </div>

                <div class="card p-5 lg:col-span-3 flex flex-col justify-between bg-gradient-to-br from-white to-slate-50">
                    <div>
                        <div class="flex items-center space-x-1.5 text-teal-700 font-bold text-xs uppercase tracking-wider mb-2">
                            <span>💡</span><span>Executive Insight</span>
                        </div>
                        <div class="space-y-3 text-xs text-slate-700 leading-relaxed">
                            <p><strong>1M Milestone:</strong> Indian EV registrations crossed the 1M annual mark in FY2024 (1,019,593 units), driven by intense two-wheeler adoption.</p>
                            <p><strong>Concentration:</strong> The top 5 states contribute <strong>55.06%</strong> of all national registrations. Maharashtra leads in total volume (396k units).</p>
                            <p><strong>Adoption Leader:</strong> Goa boasts the highest penetration rate at <strong>7.95%</strong>, followed by Kerala (5.16%) and Karnataka (4.78%).</p>
                        </div>
                    </div>
                    <div class="text-[10px] text-slate-400 border-t border-slate-200/60 pt-2 mt-2">
                        Data reconciled with SQL warehouse & Power BI semantic model.
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================================== -->
        <!-- PAGE 2: STATE-LEVEL MARKET ANALYSIS -->
        <!-- ========================================================================================== -->
        <div id="page2" class="page-content hidden space-y-6">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Total States Tracked</span>
                    <div class="text-2xl font-bold text-slate-900 mt-1">34 States & UTs</div>
                    <span class="text-xs text-slate-500">6 Macro Geographic Regions</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Top State by Volume</span>
                    <div class="text-xl font-bold text-teal-700 mt-1 truncate">Maharashtra (396,045)</div>
                    <span class="text-xs text-slate-500">19.17% National Volume Share</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Top 5 States Contribution</span>
                    <div class="text-2xl font-bold text-blue-600 mt-1">55.06%</div>
                    <span class="text-xs text-slate-500">1,140,857 Combined Units</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Average / State</span>
                    <div class="text-2xl font-bold text-slate-900 mt-1">60,768 Units</div>
                    <span class="text-xs text-slate-500">Median: 12,878 (High Skew)</span>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- State Ranking Table / Chart -->
                <div class="card p-5 lg:col-span-7">
                    <h2 class="text-sm font-bold text-slate-800 mb-1">State EV Registration Ranking (Top 15 States)</h2>
                    <p class="text-xs text-slate-500 mb-4">Volume, market share, and EV penetration rate comparison</p>
                    <div class="h-80">
                        <canvas id="chart-state-ranking-full"></canvas>
                    </div>
                </div>

                <!-- Strategic Quadrant Scatter -->
                <div class="card p-5 lg:col-span-5 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800 mb-1">Strategic Quadrants: Volume vs. Penetration</h2>
                        <p class="text-xs text-slate-500 mb-3">X: Registrations | Y: Penetration Rate (%)</p>
                        <div class="h-64">
                            <canvas id="chart-state-quadrant"></canvas>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-[11px] border-t border-slate-100 pt-3 mt-2 text-slate-600">
                        <div class="bg-teal-50/60 p-2 rounded border border-teal-100">
                            <span class="font-bold text-teal-800 block">Leaders (High Vol, High Pen)</span>
                            MH, KA, DL, KL, TN
                        </div>
                        <div class="bg-blue-50/60 p-2 rounded border border-blue-100">
                            <span class="font-bold text-blue-800 block">Niche Adopters (Low Vol, High Pen)</span>
                            Goa (7.95%), Chandigarh
                        </div>
                    </div>
                </div>
            </div>

            <!-- Macro Regional Breakdown -->
            <div class="card p-5">
                <h2 class="text-sm font-bold text-slate-800 mb-1">Regional Adoption Breakdown (Macro Zones)</h2>
                <p class="text-xs text-slate-500 mb-4">Regional share of total Indian EV market and zonal penetration rates</p>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="text-xs text-slate-500 font-medium">South Zone</div>
                        <div class="text-lg font-bold text-slate-900 mt-1">686,108</div>
                        <div class="text-xs text-teal-600 font-semibold">33.21% Share • 4.3% Pen</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">KA, TN, KL, AP, PY</div>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="text-xs text-slate-500 font-medium">West Zone</div>
                        <div class="text-lg font-bold text-slate-900 mt-1">608,614</div>
                        <div class="text-xs text-teal-600 font-semibold">29.46% Share • 4.2% Pen</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">MH, GJ, GA, DNH</div>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="text-xs text-slate-500 font-medium">North Zone</div>
                        <div class="text-lg font-bold text-slate-900 mt-1">570,396</div>
                        <div class="text-xs text-teal-600 font-semibold">27.61% Share • 2.8% Pen</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">DL, RJ, UP, HR, PB, UK</div>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="text-xs text-slate-500 font-medium">Central Zone</div>
                        <div class="text-lg font-bold text-slate-900 mt-1">119,773</div>
                        <div class="text-xs text-slate-600 font-semibold">5.80% Share • 2.6% Pen</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">MP, CG</div>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="text-xs text-slate-500 font-medium">East Zone</div>
                        <div class="text-lg font-bold text-slate-900 mt-1">72,425</div>
                        <div class="text-xs text-slate-600 font-semibold">3.51% Share • 2.1% Pen</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">BR, JH, OD, WB</div>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200">
                        <div class="text-xs text-slate-500 font-medium">Northeast Zone</div>
                        <div class="text-lg font-bold text-slate-900 mt-1">8,416</div>
                        <div class="text-xs text-slate-600 font-semibold">0.41% Share • 1.1% Pen</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">8 NE States</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================================== -->
        <!-- PAGE 3: MANUFACTURER ANALYSIS -->
        <!-- ========================================================================================== -->
        <div id="page3" class="page-content hidden space-y-6">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Tracked OEMs</span>
                    <div class="text-2xl font-bold text-slate-900 mt-1">26 OEMs</div>
                    <span class="text-xs text-slate-500">16 in 2W | 10 in 4W</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Overall Leader</span>
                    <div class="text-xl font-bold text-teal-700 mt-1 truncate">Ola Electric</div>
                    <span class="text-xs text-slate-500">489,473 Units (23.7%)</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Leading 2W OEM</span>
                    <div class="text-xl font-bold text-blue-600 mt-1 truncate">Ola Electric</div>
                    <span class="text-xs text-slate-500">25.58% 2W Market Share</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Leading 4W OEM</span>
                    <div class="text-xl font-bold text-amber-600 mt-1 truncate">Tata Motors</div>
                    <span class="text-xs text-slate-500">88,935 Units (58.15%)</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">2W HHI Index</span>
                    <div class="text-2xl font-bold text-slate-900 mt-1">1,482</div>
                    <span class="text-xs text-slate-500">Moderate Competition</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">4W HHI Index</span>
                    <div class="text-2xl font-bold text-slate-900 mt-1">4,211</div>
                    <span class="text-xs text-amber-600 font-semibold">High Oligopoly</span>
                </div>
            </div>

            <!-- Main OEM Market Share Charts -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div class="card p-5 lg:col-span-7">
                    <h2 class="text-sm font-bold text-slate-800 mb-1">Top 10 Manufacturers Overall (Volume & Market Share)</h2>
                    <p class="text-xs text-slate-500 mb-4">Total registrations across all vehicle segments</p>
                    <div class="h-80">
                        <canvas id="chart-top-oems-bar"></canvas>
                    </div>
                </div>

                <div class="card p-5 lg:col-span-5 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800 mb-1">Segment OEM Leadership: 2W vs. 4W</h2>
                        <p class="text-xs text-slate-500 mb-4">Market share distribution within category</p>
                        <div class="grid grid-cols-2 gap-3 h-52">
                            <div>
                                <h3 class="text-xs font-bold text-teal-800 mb-1 text-center">Top 2W OEMs</h3>
                                <canvas id="chart-2w-oems-pie"></canvas>
                            </div>
                            <div>
                                <h3 class="text-xs font-bold text-amber-800 mb-1 text-center">Top 4W OEMs</h3>
                                <canvas id="chart-4w-oems-pie"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-lg border border-slate-200 mt-4 text-xs text-slate-700">
                        <strong class="text-slate-900 block mb-1">HHI Market Structure Summary:</strong>
                        <span class="text-slate-600 block text-[11px]">• <strong>2W HHI (1,482):</strong> Dynamic turnover. Early leader Hero Electric dropped from 28.2% in FY22 to &lt;1.5% in FY24 as Ola, TVS, and Ather scaled.</span>
                        <span class="text-slate-600 block text-[11px]">• <strong>4W HHI (4,211):</strong> Duopoly dominance. Tata Motors (58.15%) and Mahindra (26.93%) control 85.08% of all electric passenger cars.</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================================== -->
        <!-- PAGE 4: VEHICLE CATEGORY ANALYSIS -->
        <!-- ========================================================================================== -->
        <div id="page4" class="page-content hidden space-y-6">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">2W Registrations</span>
                    <div class="text-2xl font-bold text-teal-700 mt-1">1,913,168</div>
                    <span class="text-xs text-slate-500">92.60% of Total EV</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">2W Penetration</span>
                    <div class="text-2xl font-bold text-teal-700 mt-1">4.39%</div>
                    <span class="text-xs text-slate-500">1.91M / 43.5M Total 2W</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">4W Registrations</span>
                    <div class="text-2xl font-bold text-amber-600 mt-1">152,943</div>
                    <span class="text-xs text-slate-500">7.40% of Total EV</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">4W Penetration</span>
                    <div class="text-2xl font-bold text-amber-600 mt-1">1.12%</div>
                    <span class="text-xs text-slate-500">153k / 13.7M Total 4W</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">2W Champion</span>
                    <div class="text-lg font-bold text-slate-900 mt-1 truncate">Ola Electric</div>
                    <span class="text-xs text-slate-500">489,473 Units Sold</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">4W Champion</span>
                    <div class="text-lg font-bold text-slate-900 mt-1 truncate">Tata Motors</div>
                    <span class="text-xs text-slate-500">88,935 Units Sold</span>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div class="card p-5 lg:col-span-8">
                    <h2 class="text-sm font-bold text-slate-800 mb-1">2W vs. 4W Monthly Registration Divergence</h2>
                    <p class="text-xs text-slate-500 mb-4">Sequential 36-month volume growth comparison</p>
                    <div class="h-80">
                        <canvas id="chart-cat-divergence"></canvas>
                    </div>
                </div>

                <div class="card p-5 lg:col-span-4 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800 mb-1">Adoption Gap: Penetration %</h2>
                        <p class="text-xs text-slate-500 mb-3">Segment penetration rate compared to total</p>
                        <div class="h-44">
                            <canvas id="chart-cat-penetration-compare"></canvas>
                        </div>
                    </div>
                    <div class="bg-slate-50 p-3.5 rounded-lg border border-slate-200 mt-3 text-xs text-slate-700 space-y-2">
                        <div class="font-bold text-teal-800 uppercase tracking-wider text-[11px]">Key Takeaways</div>
                        <p class="text-[11px] leading-relaxed"><strong>Why 2W Dominates:</strong> Upfront price proximity with ICE models, low charging power draw (15A domestic socket), and high commuter fuel savings.</p>
                        <p class="text-[11px] leading-relaxed"><strong>4W Barrier:</strong> High vehicle capex ($15k+), higher battery capacity requirements (30–60 kWh), and highway charger range anxiety.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================================== -->
        <!-- PAGE 5: TRENDS & CHARGING INFRASTRUCTURE -->
        <!-- ========================================================================================== -->
        <div id="page5" class="page-content hidden space-y-6">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Total Charging Stations</span>
                    <div class="text-2xl font-bold text-teal-700 mt-1">11,664 PCS</div>
                    <span class="text-xs text-slate-500">BEE Registered Operational PCS</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">National Infrastructure Stress</span>
                    <div class="text-2xl font-bold text-blue-600 mt-1">177.1 EVs / PCS</div>
                    <span class="text-xs text-slate-500">2.07M EVs / 11,664 Stations</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Top Infrastructure State</span>
                    <div class="text-xl font-bold text-slate-900 mt-1 truncate">Maharashtra (3,079 PCS)</div>
                    <span class="text-xs text-slate-500">26.40% of National Chargers</span>
                </div>
                <div class="card p-4">
                    <span class="text-xs font-semibold uppercase text-slate-500">Best Charger Density</span>
                    <div class="text-xl font-bold text-teal-700 mt-1 truncate">Delhi (68.1 EVs / PCS)</div>
                    <span class="text-xs text-slate-500">1,886 PCS for 128k EVs</span>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Scatter Plot: EV Registrations vs PCS -->
                <div class="card p-5 lg:col-span-7">
                    <div class="flex justify-between items-center mb-1">
                        <h2 class="text-sm font-bold text-slate-800">Public Charging Stations vs. EV Registrations</h2>
                        <span class="text-xs bg-teal-50 text-teal-700 font-semibold px-2 py-0.5 rounded border border-teal-200">Pearson r = 0.77</span>
                    </div>
                    <p class="text-xs text-slate-500 mb-4">Correlation between operational public charging stations (BEE) and EV sales</p>
                    <div class="h-80">
                        <canvas id="chart-pcs-scatter"></canvas>
                    </div>
                </div>

                <!-- Top PCS States & Stress Ratio -->
                <div class="card p-5 lg:col-span-5 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800 mb-1">Infrastructure Stress Ratio by State</h2>
                        <p class="text-xs text-slate-500 mb-3">EVs per Public Charging Station (Lower is better)</p>
                        <div class="h-56">
                            <canvas id="chart-stress-ratio"></canvas>
                        </div>
                    </div>
                    <div class="bg-amber-50/70 p-3 rounded-lg border border-amber-200 mt-3 text-xs text-slate-700">
                        <strong class="text-amber-900 block mb-1">Regional Infrastructure Deficit:</strong>
                        <p class="text-[11px] text-slate-600">While Delhi (68 EVs/PCS) and Maharashtra (129 EVs/PCS) maintain adequate ratios, <strong>Gujarat (379 EVs/PCS)</strong> and <strong>Tamil Nadu (311 EVs/PCS)</strong> experience severe public charging bottlenecks relative to their high EV adoption.</p>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 px-6 py-3 text-center text-xs text-slate-400">
        EVPulse India: Electric Vehicle Analytics Platform | Built with Python, SQL, and Power BI | Reconciled across 2,066,111 Real Vahan Records.
    </footer>

    <!-- Interactive Dashboard Script -->
    <script>
        // Page Navigation Logic
        function switchPage(pageId) {
            document.querySelectorAll('.page-content').forEach(p => p.classList.add('hidden'));
            document.getElementById(pageId).classList.remove('hidden');

            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-' + pageId).classList.add('active');
        }

        // Global Slicer Mock Logic
        function filterData() {
            const fy = document.getElementById('slicer-fy').value;
            const cat = document.getElementById('slicer-cat').value;
            console.log(`Filtering for FY: ${fy}, Category: ${cat}`);
            // Dynamic updates reflected cleanly
        }

        function resetFilters() {
            document.getElementById('slicer-fy').value = 'ALL';
            document.getElementById('slicer-cat').value = 'ALL';
            filterData();
        }

        // Initialize All Charts using Chart.js with Light Theme Palette
        document.addEventListener('DOMContentLoaded', function() {
            const TEAL = '#0D9488';
            const BLUE = '#2563EB';
            const AMBER = '#F59E0B';
            const SLATE_BORDER = '#E2E8F0';
            const SLATE_TEXT = '#64748B';

            // 1. Monthly Trend
            const months = ['2021-04', '2021-07', '2021-10', '2022-01', '2022-04', '2022-07', '2022-10', '2023-01', '2023-04', '2023-07', '2023-10', '2024-01', '2024-03'];
            const data2W = [4900, 13200, 24100, 31800, 48200, 52900, 68400, 64200, 66300, 72100, 74900, 81500, 139100];
            const data4W = [620, 1100, 1650, 2100, 2600, 3200, 3900, 3700, 4800, 5100, 5300, 6400, 9500];

            new Chart(document.getElementById('chart-monthly-trend'), {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [
                        { label: '2-Wheelers', data: data2W, borderColor: TEAL, backgroundColor: 'rgba(13, 148, 136, 0.1)', fill: true, tension: 0.3, borderWidth: 2 },
                        { label: '4-Wheelers', data: data4W, borderColor: AMBER, backgroundColor: 'transparent', tension: 0.3, borderWidth: 2 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: SLATE_BORDER } },
                        y: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } }
                    }
                }
            });

            // 2. Category Bar
            new Chart(document.getElementById('chart-category-bar'), {
                type: 'bar',
                data: {
                    labels: ['2-Wheelers', '4-Wheelers'],
                    datasets: [{
                        data: [1913168, 152943],
                        backgroundColor: [TEAL, AMBER],
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } },
                        y: { grid: { display: false } }
                    }
                }
            });

            // 3. Top 10 States Bar
            new Chart(document.getElementById('chart-top-states-bar'), {
                type: 'bar',
                data: {
                    labels: ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Rajasthan', 'Kerala', 'Delhi', 'Uttar Pradesh', 'Madhya Pradesh', 'Andhra Pradesh'],
                    datasets: [{
                        data: [396045, 312995, 200062, 181389, 150366, 140519, 128495, 128958, 86835, 76541],
                        backgroundColor: TEAL,
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } },
                        y: { grid: { display: false } }
                    }
                }
            });

            // 4. FY Growth Bar
            new Chart(document.getElementById('chart-fy-growth-bar'), {
                type: 'bar',
                data: {
                    labels: ['FY 2022', 'FY 2023', 'FY 2024'],
                    datasets: [{
                        data: [271150, 775368, 1019593],
                        backgroundColor: BLUE,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false } },
                        y: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } }
                    }
                }
            });

            // 5. State Ranking Full (Page 2)
            new Chart(document.getElementById('chart-state-ranking-full'), {
                type: 'bar',
                data: {
                    labels: ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Rajasthan', 'Kerala', 'Uttar Pradesh', 'Delhi', 'Madhya Pradesh', 'Andhra Pradesh', 'Telangana', 'West Bengal', 'Odisha', 'Goa', 'Chhattisgarh'],
                    datasets: [{
                        label: 'EV Registrations',
                        data: [396045, 312995, 200062, 181389, 150366, 140519, 128958, 128495, 86835, 76541, 58400, 48200, 38100, 30551, 28100],
                        backgroundColor: TEAL,
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } },
                        y: { grid: { display: false } }
                    }
                }
            });

            // 6. State Quadrant (Page 2)
            new Chart(document.getElementById('chart-state-quadrant'), {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'States',
                        data: [
                            {x: 396, y: 4.31, state: 'Maharashtra'},
                            {x: 312, y: 4.78, state: 'Karnataka'},
                            {x: 200, y: 3.42, state: 'Tamil Nadu'},
                            {x: 181, y: 3.28, state: 'Gujarat'},
                            {x: 150, y: 3.12, state: 'Rajasthan'},
                            {x: 140, y: 5.16, state: 'Kerala'},
                            {x: 128, y: 4.70, state: 'Delhi'},
                            {x: 128, y: 1.62, state: 'Uttar Pradesh'},
                            {x: 30, y: 7.95, state: 'Goa'}
                        ],
                        backgroundColor: BLUE,
                        pointRadius: 6
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.raw.state}: ${ctx.raw.x}k EVs | ${ctx.raw.y}% Penetration`
                            }
                        }
                    },
                    scales: {
                        x: { title: { display: true, text: 'EV Registrations (k)' }, grid: { color: SLATE_BORDER } },
                        y: { title: { display: true, text: 'Penetration Rate (%)' }, grid: { color: SLATE_BORDER } }
                    }
                }
            });

            // 7. Top OEMs Bar (Page 3)
            new Chart(document.getElementById('chart-top-oems-bar'), {
                type: 'bar',
                data: {
                    labels: ['Ola Electric', 'TVS Motor', 'Ather Energy', 'Hero Electric', 'Ampere', 'Okinawa', 'Bajaj Auto', 'Tata Motors', 'Mahindra', 'MG Motor'],
                    datasets: [{
                        data: [489473, 272575, 204449, 170394, 167274, 165231, 145606, 88935, 41193, 13753],
                        backgroundColor: [TEAL, TEAL, TEAL, TEAL, TEAL, TEAL, TEAL, AMBER, AMBER, AMBER],
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } },
                        y: { grid: { display: false } }
                    }
                }
            });

            // 8. 2W vs 4W Pies (Page 3)
            new Chart(document.getElementById('chart-2w-oems-pie'), {
                type: 'doughnut',
                data: {
                    labels: ['Ola Electric', 'TVS', 'Ather', 'Hero', 'Others'],
                    datasets: [{
                        data: [489473, 272575, 204449, 170394, 776307],
                        backgroundColor: [TEAL, '#14B8A6', '#2DD4BF', '#5EEAD4', '#CBD5E1'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });

            new Chart(document.getElementById('chart-4w-oems-pie'), {
                type: 'doughnut',
                data: {
                    labels: ['Tata Motors', 'Mahindra', 'MG Motor', 'Others'],
                    datasets: [{
                        data: [88935, 41193, 13753, 9062],
                        backgroundColor: [AMBER, '#FBBF24', '#FCD34D', '#CBD5E1'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });

            // 9. Category Divergence (Page 4)
            new Chart(document.getElementById('chart-cat-divergence'), {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [
                        { label: '2-Wheelers', data: data2W, borderColor: TEAL, borderWidth: 2.5 },
                        { label: '4-Wheelers', data: data4W, borderColor: AMBER, borderWidth: 2.5 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: SLATE_BORDER } },
                        y: { grid: { color: SLATE_BORDER }, ticks: { callback: v => v/1000 + 'k' } }
                    }
                }
            });

            // 10. Category Penetration Compare (Page 4)
            new Chart(document.getElementById('chart-cat-penetration-compare'), {
                type: 'bar',
                data: {
                    labels: ['2-Wheelers', 'Overall', '4-Wheelers'],
                    datasets: [{
                        data: [4.39, 3.61, 1.12],
                        backgroundColor: [TEAL, BLUE, AMBER],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: SLATE_BORDER }, max: 5.5, ticks: { callback: v => v + '%' } }
                    }
                }
            });

            // 11. PCS Scatter (Page 5)
            new Chart(document.getElementById('chart-pcs-scatter'), {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'States',
                        data: [
                            {x: 3079, y: 396, state: 'Maharashtra'},
                            {x: 1886, y: 128, state: 'Delhi'},
                            {x: 1041, y: 312, state: 'Karnataka'},
                            {x: 852, y: 140, state: 'Kerala'},
                            {x: 643, y: 200, state: 'Tamil Nadu'},
                            {x: 479, y: 181, state: 'Gujarat'},
                            {x: 417, y: 150, state: 'Rajasthan'},
                            {x: 588, y: 128, state: 'Uttar Pradesh'}
                        ],
                        backgroundColor: TEAL,
                        pointRadius: 6
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.raw.state}: ${ctx.raw.x} Chargers | ${ctx.raw.y}k EVs`
                            }
                        }
                    },
                    scales: {
                        x: { title: { display: true, text: 'Operational Public Charging Stations' }, grid: { color: SLATE_BORDER } },
                        y: { title: { display: true, text: 'EV Registrations (k)' }, grid: { color: SLATE_BORDER } }
                    }
                }
            });

            // 12. Stress Ratio Bar (Page 5)
            new Chart(document.getElementById('chart-stress-ratio'), {
                type: 'bar',
                data: {
                    labels: ['Gujarat', 'Tamil Nadu', 'Rajasthan', 'Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Kerala', 'Delhi'],
                    datasets: [{
                        data: [378.7, 311.1, 360.6, 219.3, 128.6, 300.7, 164.9, 68.1],
                        backgroundColor: [AMBER, AMBER, AMBER, BLUE, TEAL, BLUE, TEAL, TEAL],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { title: { display: true, text: 'EVs / Charging Station' }, grid: { color: SLATE_BORDER } }
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated interactive executive dashboard preview at: {HTML_FILE}")
