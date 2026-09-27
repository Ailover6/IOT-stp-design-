# EcoSmart: Industrial Sewage Treatment Plant (STP) Digital Twin & SCADA Suite

EcoSmart is an integrated, web-based digital twin and supervisory control platform designed to bridge the gap between static environmental engineering design and real-time operational monitoring for Industrial Sewage Treatment Plants (STPs).

## 🚀 Key Features

* **Automated Process Design & Sizing:** Computes daily BOD load, aeration tank volume, hydraulic retention time (HRT), clarifier dimensions, and sludge age (SRT) using standard activated-sludge kinetics.
* **Energy & Carbon Audit:** Estimates daily blower power consumption, power costs, coagulant (alum) requirements, and carbon emissions.
* **Regulatory Compliance Auditor:** Automatically audits plant performance against CPCB/EPA inland disposal norms.
* **Hydraulic Surge Stress-Tester:** Simulates monsoon-scale hydraulic shock loads to evaluate safety margins against washout risks.
* **Real-Time SCADA Control Center:** Features an auto-refreshing telemetry dashboard simulating live sensor streams for pH, dissolved oxygen (DO), turbidity, and inflow velocity with threshold-based alerting.
* **SQLite Persistence:** Allows engineers to save, load, and manage named plant configurations.

## 🛠️ Tech Stack

* **Frontend & Framework:** Streamlit (Python)
* **Data Processing:** Pandas, NumPy
* **Database:** SQLite3
* **Document Generation:** Python-Docx / Custom reporting pipeline

## 📦 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Ailover6/IOT-stp-design-.git](https://github.com/Ailover6/IOT-stp-design-.git)
   cd IOT-stp-design-
