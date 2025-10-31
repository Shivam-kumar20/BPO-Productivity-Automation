# BPO-Productivity-Automation
“A Python automation project for generating and analyzing BPO productivity reports using pandas — combines multiple datasets into one clean, analytics-ready output.”

### 🔍 Overview  
This Python script automates the process of cleaning, transforming, and merging multiple productivity reports into a single, analysis-ready CSV.  
It’s designed to simplify call center performance reporting — combining call details, user hierarchy, and campaign insights into one unified dataset.

---

### ⚠️ Disclaimer  
All datasets used in this project (`dummy_productivity_report.csv`, `dummy_detail_report.csv`, and `Mapping.xlsx`) contain **dummy data** created solely for **educational and learning purposes**.  
They **do not represent any real organization or confidential information**.  
This project is intended for demonstrating data cleaning, aggregation, and automation techniques in Python — **not for commercial or organizational use**.

---

### ⚙️ Key Features
- **Data Cleaning:** Converts raw CSV and Excel files into consistent, readable formats.  
- **Aggregation:** Calculates total dials, connects, talk time, and ringing time per user.  
- **Mapping Integration:** Merges employee hierarchy (TL, AGM, Cluster Head, Role) from a separate mapping file.  
- **Time Conversion:** Converts machine time formats to human-readable HH:MM:SS.  
- **Filtering:** Keeps only relevant sales and support roles.  
- **Final Export:** Generates a polished `Scrubbed_APR.csv` ready for Power BI or Excel analysis.  

---

### 🧮 Tech Stack
- **Language:** Python 🐍  
- **Libraries:** pandas, warnings  

---

### 🧠 Workflow
1. Import raw CSV/Excel files.  
2. Clean and standardize User IDs (lowercase).  
3. Compute aggregate metrics using `groupby()` and custom functions.  
4. Merge all datasets step-by-step into one master file.  
5. Filter by key roles and export results.  

---

### 💾 Output
**File Name:** `Scrubbed_APR.csv`  
**Contains:**  
- Process and Campaign details  
- User hierarchy (Role, TL, Cluster Head, AGM)  
- Call metrics: Total Dials, Total Connects, Talk Time, Ring Time, etc.  

---

### 🧩 Example Use Case
This script can be used for:
- Daily productivity tracking  
- Team performance dashboards  
- Automated data pipelines  
- Power BI or Tableau reporting inputs  

---

### 👨‍💻 Author
**Shivam Kumar** — Data Analyst  
> Focused on automating analytics workflows, optimizing reporting pipelines, and turning raw data into actionable insights.

