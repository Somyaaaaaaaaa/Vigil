# VIGIL 
**Status: Operational** 
**Classification: Personal Command & Intelligence Dashboard**

VIGIL is a high-fidelity tactical management system built with a dark, sophisticated, and mission-oriented interface. It is designed for absolute oversight of daily operations, combining behavioral tracking with strategic analysis.

---
## 1. Code Architecture

- app.py → entry point, routing, auth
- database.py → all DB logic

### Modules
- home.py → dashboard + streak + overview
- analytics.py → scores, trends, insights
- habits.py → logging system
- tasks.py → task execution
- goals.py → direction layer
- routines.py → structure layer
- checklist.py → quick execution

### Flow
app.py → route → module → database.py → SQLite

## 2. Logical Architecture 

Layers:
Execution → tasks, checklist
Consistency → habits, streaks
Structure → routines
Direction → goals
Reflection → notes
Analysis → analytics and insights

---

## OPERATIONAL MODULES

### **I. COMMAND (Dashboard)**
The central node. A high-level overview of active sectors, providing immediate situational awareness of your daily objectives.

### **II. DATA ACQUISITION (Tracking)**
* **Tasks:** Objective-based daily execution. 
* **Habits:** Long-term behavioral consistency monitoring.

### **III. STRATEGY (Planning)**
* **Goals:** Long-range trajectory alignment.
* **Routines:** Standard Operating Procedures (SOPs) for daily stability.
* **Checklist:** A repository for non-time-sensitive maintenance. These are objectives without a tactical deadline—tasks that require execution only when primary operational windows are clear.

### **IV. INTELLIGENCE (Insights)**
The system's star feature. A dedicated analysis window that processes raw behavioral data into visual intelligence, identifying vulnerabilities in performance and optimizing output.

---

## ACCESS PROTOCOL
The system is protected by an encrypted access layer.
1. Ensure your `.env` file is configured with `APP_PASSWORD`.
2. Unauthorized entry attempts will result in **ACCESS DENIED** status.

---

## DEPLOYMENT INSTRUCTIONS

1.  **Clone the Core:**
    git clone https://github.com/yourusername/vigil.git
2.  **Environment Setup:**
    pip install streamlit os-sys datetime
3.  **Initialize System:**
    streamlit run app.py

---

## INTELLECTUAL PROPERTY NOTICE
**© 2026 VIGIL CORE. ALL RIGHTS RESERVED.**

Vigil is provided for personal use. The visual identity, logo, and "Military-Elegant" aesthetic are the proprietary property of the developer. 
* **Non-Commercial:** You may not use this system for commercial purposes or monetization.
* **Attribution:** If shared, credit to the original architect is mandatory.
* **Integrity:** No unauthorized "re-skinning" or rebranding of the Vigil Core identity.

---
