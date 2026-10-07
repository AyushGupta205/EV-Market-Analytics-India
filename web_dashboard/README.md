# EVPulse India — Executive Full HD Analytics Dashboard (1920×1080 Single-Screen)

An executive-level, single-screen Business Intelligence dashboard implemented in native HTML5, CSS3, and JavaScript, designed specifically for **Full HD 1920×1080 px (16:9) displays / 15.6-inch laptops** with **Zero Vertical or Horizontal Scrolling**.

---

## 1. Primary Design Philosophy
* **Strict Single Viewport Fit**: All critical analytics, KPIs, charts, maps, rankings, and business insights are visible simultaneously inside a single `1920×1080` screen without page scrolling, swiping, or carousel transitions.
* **Information-Dense Executive Report**: Modeled after enterprise Power BI executive reporting standards.
* **Data Integrity**: Derived strictly from the historical EV dataset covering **FY2022–FY2024 (April 2021 – March 2024)** across **34 Indian States & Union Territories**.

---

## 2. Core Project Metrics (Verified Source of Truth)

| Metric | Official Project Value | Business Context |
| :--- | :---: | :--- |
| **Total EV Registrations** | **2,066,111** | Cumulative registrations across FY2022–FY2024 |
| **Total Automotive Registrations** | **57.2M** (`57,233,134`) | Total ICE + EV recorded vehicular registrations |
| **EV Market Share** | **3.61%** | National EV adoption share across all categories |
| **YoY Annual Growth** | **+31.5%** | FY2024 (`1,019,593`) vs FY2023 (`775,368`) |
| **Top EV State** | **Maharashtra** | `396,045` registrations (19.2% national volume share) |
| **Top EV Category** | **2-Wheelers (2W)** | `1,913,168` registrations (92.60% volume share) |
| **Top 5 State Concentration** | **60.06%** | `1,240,857` registrations across Maharashtra, Karnataka, Tamil Nadu, Gujarat, and Rajasthan |
| **2W Market HHI** | **1,335** | 2W market concentration index |
| **4W Market HHI** | **4,194** | 4W market concentration index |
| **Tata + Mahindra 4W Share** | **85.08%** | Tata Motors (`58.15%`) + Mahindra (`26.93%`) = `130,128` registrations |

---

## 3. Executive Business Insights

1. **Adoption Trajectory:** Cumulative EV registrations reached **2.07M units** across FY22–FY24, with FY24 exceeding **1M annual registrations** (+31.5% YoY).
2. **Geographic Concentration:** The top five states — Maharashtra, Karnataka, Tamil Nadu, Gujarat, and Rajasthan — account for **60.06% of recorded EV registrations (1.24M units)**, with Maharashtra leading at 396k.
3. **Category Dynamics:** 2-Wheelers represent **92.60% of recorded EV registrations (1.91M units)**, compared with **7.40% for 4-Wheelers**.
4. **Market Structure:** The 4W segment records an **HHI of 4,194**. Tata Motors and Mahindra & Mahindra account for **85.08% of recorded 4W registrations**.

---

## 4. Professional Data-Source Footer
* **Sources:** MoRTH / Vahan Sewa · BEE
* **Coverage:** FY2022–FY2024 · 36 Months · 34 States & UTs
* **Records:** 3,261 Fact Records · 26 Manufacturers · 2 Categories

---

## 5. File Structure
* [`index.html`](file:///d:/EV_Analytics/EVPulse_India_HTML_Dashboard_FHD/index.html) — Semantically structured single-page HTML5 document.
* [`style.css`](file:///d:/EV_Analytics/EVPulse_India_HTML_Dashboard_FHD/style.css) — Full HD locked CSS rules, flexbox/grid layout, typography clamps, zero-scroll rules.
* [`script.js`](file:///d:/EV_Analytics/EVPulse_India_HTML_Dashboard_FHD/script.js) — Self-contained dataset (3,261 records), SVG path coordinates, Chart.js instances, and cross-filter engine.
